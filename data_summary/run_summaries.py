import html
import json
import re
import ijson
from pathlib import Path
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


DATA_PATH = Path(__file__).parent.parent / "Data" / "games.json"
PLOT_DIR = Path(__file__).parent / "summaries" / "plots"
OUT_DIR = Path(__file__).parent / "summaries" / "text_summaries" # NEW: where the top-words text files go

# NEW: set to True to drop common filler words ("the", "and", ...) from the counts
REMOVE_STOPWORDS = False
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "has", "have", "he", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "their", "they", "this", "to", "was", "were", "will", "with",
    "you", "your", "can", "all", "not", "more", "one", "if", "so", "s",
}

# NEW: tokenizer pieces
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def word_count(text):
    return len(text.split()) if isinstance(text, str) else 0


# NEW
def tokenize(text):
    """Lowercase, unescape HTML entities, strip tags, return a list of words."""
    if not isinstance(text, str):
        return []
    text = TAG_RE.sub(" ", html.unescape(text).lower())
    tokens = WORD_RE.findall(text)
    if REMOVE_STOPWORDS:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens


def get_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, dict):
        return list(value.keys())
    return []


def print_distribution(name, values):
    values = np.array(values, dtype=int)

    print(f"\n--- {name} ---")
    print(f"Games counted: {len(values)}")
    print(f"Minimum: {np.min(values)} words")
    print(f"Maximum: {np.max(values)} words")
    print(f"Mean: {np.mean(values):.2f} words")
    print(f"Median: {np.median(values):.2f} words")


def save_histogram(name, values, bins=50, max_words=None):
    values = np.array(values, dtype=int)

    plt.figure(figsize=(10, 6))

    if max_words is not None:
        hist_range = (0, max_words)
        excluded = np.sum(values > max_words)
        plt.hist(values, bins=bins, range=hist_range, edgecolor="black")
        plt.title(f"{name} (up to {max_words} words; {excluded} games above not shown)")
    else:
        plt.hist(values, bins=bins, edgecolor="black")
        plt.title(name)

    plt.xlabel("Number of Words")
    plt.ylabel("Number of Games")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    PLOT_DIR.mkdir(exist_ok=True)
    filename = name.lower().replace(" ", "_")
    plt.savefig(PLOT_DIR / f"{filename}.png", dpi=150)
    plt.close()


# CHANGED: added xlabel and print_top so it works for word counts too
def save_bar_chart(name, counter, top_n=50, xlabel="Number of Games", print_top=True):
    most_common = counter.most_common(top_n)

    if not most_common:
        print(f"\n{name}: No data available.")
        return

    labels, counts = zip(*most_common)

    plt.figure(figsize=(14, 9))
    plt.barh(labels[::-1], counts[::-1])
    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(name.split(" ")[-1])
    plt.tight_layout()

    PLOT_DIR.mkdir(exist_ok=True)
    filename = name.lower().replace(" ", "_")
    plt.savefig(PLOT_DIR / f"{filename}.png", dpi=150)
    plt.close()

    if print_top:
        print(f"\n--- {name}: Top {len(most_common)} ---")
        for label, count in most_common:
            print(f"{label}: {count}")


# NEW
def save_top_words(filename, word_counter, doc_counter, top_n=200):
    """Write the top_n words to a tab-separated text file: rank, word, total count, games containing it."""
    path = OUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write("rank\tword\tcount\tgames\n")
        for rank, (word, count) in enumerate(word_counter.most_common(top_n), start=1):
            f.write(f"{rank}\t{word}\t{count}\t{doc_counter[word]}\n")
    print(f"Saved top {top_n} words to: {path}")


def iter_games():
    with open(DATA_PATH, "rb") as f:
        # Yields (app_id, game_dict) one at a time, never the whole file
        for _, game in ijson.kvitems(f, ""):
            if isinstance(game, dict):
                yield game


def main():
    title_lengths = []
    description_lengths = []
    all_tags = Counter()
    all_categories = Counter()

    # NEW: total occurrences of each word, and number of games containing it
    title_words = Counter()
    title_doc_freq = Counter()
    desc_words = Counter()
    desc_doc_freq = Counter()

    total = 0

    for game in iter_games():
        total += 1
        title = game.get("name", "")
        description = game.get("about_the_game", "")

        title_lengths.append(word_count(title))
        description_lengths.append(word_count(description))
        all_tags.update(get_list(game.get("tags")))
        all_categories.update(get_list(game.get("categories")))

        # NEW: individual word counts
        title_tokens = tokenize(title)
        desc_tokens = tokenize(description)
        title_words.update(title_tokens)
        title_doc_freq.update(set(title_tokens))
        desc_words.update(desc_tokens)
        desc_doc_freq.update(set(desc_tokens))

        if total % 1000 == 0:
            print("finished " + str(total))

    print(f"Loaded {total} games.")

    print_distribution("Game Title Word Count", title_lengths)

    print_distribution("Game Description Word Count", description_lengths)

    save_bar_chart("Top 50 Tags", all_tags)
    save_bar_chart("Top 50 Categories", all_categories)

    # NEW: top 50 word charts + top 200 word files
    save_bar_chart("Top 50 Title Words", title_words, xlabel="Total Occurrences", print_top=False)
    save_bar_chart("Top 50 Description Words", desc_words, xlabel="Total Occurrences", print_top=False)
    save_top_words("top_200_title_words.txt", title_words, title_doc_freq)
    save_top_words("top_200_description_words.txt", desc_words, desc_doc_freq)

    save_histogram("Game Title Word Count", title_lengths)
    save_histogram("Game Description Word Count", description_lengths, max_words=2000)

    print(f"\nPlots saved to: {PLOT_DIR}")


if __name__ == "__main__":
    main()