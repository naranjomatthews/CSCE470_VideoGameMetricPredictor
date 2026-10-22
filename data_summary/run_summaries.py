
import json
import ijson
from pathlib import Path
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


DATA_PATH = Path(__file__).parent.parent / "Data" / "games.json"
PLOT_DIR = Path(__file__).parent / "plots"


def word_count(text):
    return len(text.split()) if isinstance(text, str) else 0


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


def save_bar_chart(name, counter, top_n=50):
    most_common = counter.most_common(top_n)

    if not most_common:
        print(f"\n{name}: No data available.")
        return

    labels, counts = zip(*most_common)

    plt.figure(figsize=(14, 9))
    plt.barh(labels[::-1], counts[::-1])
    plt.title(name)
    plt.xlabel("Number of Games")
    plt.ylabel(name.split(" ")[-1])
    plt.tight_layout()

    PLOT_DIR.mkdir(exist_ok=True)
    filename = name.lower().replace(" ", "_")
    plt.savefig(PLOT_DIR / f"{filename}.png", dpi=150)
    plt.close()

    print(f"\n--- {name}: Top {len(most_common)} ---")
    for label, count in most_common:
        print(f"{label}: {count}")

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
    total = 0

    for game in iter_games():
        total += 1
        title_lengths.append(word_count(game.get("name", "")))
        description_lengths.append(word_count(game.get("about_the_game", "")))
        all_tags.update(get_list(game.get("tags")))
        all_categories.update(get_list(game.get("categories")))

        if total % 1000 == 0:
            print("finished " + str(total))

    print(f"Loaded {total} games.")

    print_distribution("Game Title Word Count", title_lengths)

    print_distribution("Game Description Word Count", description_lengths)

    save_bar_chart("Top 50 Tags", all_tags)
    save_bar_chart("Top 50 Categories", all_categories)

    save_histogram("Game Title Word Count", title_lengths)
    save_histogram("Game Description Word Count", description_lengths, max_words=2000)

    print(f"\nPlots saved to: {PLOT_DIR}")



if __name__ == "__main__":
    main()