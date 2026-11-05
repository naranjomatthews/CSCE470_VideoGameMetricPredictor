from pathlib import Path
import re
import html 
import ijson 
import json
from collections import Counter

DATA_PATH = Path(__file__).parent / "miniDataSet.json"
PREPROCESSED_OUT_PATH = Path(__file__).parent / "preprocessed_mini_data.json"

# tokenizer pieces
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

REMOVE_STOPWORDS = True
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "has", "have", "he", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "their", "they", "this", "to", "was", "were", "will", "with",
    "you", "your", "can", "all", "not", "more", "one", "if", "so", "s",
}

def tokenize(text):
    """Lowercase, unescape HTML entities, strip tags, return a list of words."""
    if not isinstance(text, str):
        return []
    text = TAG_RE.sub(" ", html.unescape(text).lower())
    tokens = WORD_RE.findall(text)
    if REMOVE_STOPWORDS:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens

def names_to_tokens(value):
    """Tokenize a list of names (genres) or a dict keyed by name (tags)."""
    if isinstance(value, dict):
        names = value.keys()
    elif isinstance(value, list):
        names = value
    elif isinstance(value, str):
        names = [value]
    else:
        names = []
    tokens = []
    for name in names:
        tokens.extend(tokenize(name))
    return tokens

def parse_owners(s):
    """'0 - 20000' -> midpoint (10000). Returns 0 if unparseable."""
    nums = [int(n) for n in re.findall(r"\d+", str(s).replace(",", ""))]
    return sum(nums) // len(nums) if nums else 0

def to_int(x):
    try:
        return int(x or 0)
    except (TypeError, ValueError):
        return 0


def build_record(game):
    positive = to_int(game.get("positive"))
    negative = to_int(game.get("negative"))
    votes = positive + negative

    title_tokens = tokenize(game.get("name", ""))
    description_tokens = tokenize(game.get("about_the_game", ""))
    tags_tokens = names_to_tokens(game.get("tags"))
    genres_tokens = names_to_tokens(game.get("genres"))

    return {
        "title_bow": dict(Counter(title_tokens)),
        "description_bow": dict(Counter(description_tokens)),
        "tags_bow": dict(Counter(tags_tokens)),
        "genres_bow": dict(Counter(genres_tokens)),

        # lengths
        "title_length": len(title_tokens),
        "description_length" : len(description_tokens),
        "tags_length" : len(tags_tokens),
        "genres_length" :len(genres_tokens),

        # non-textual features
        "rating": round(positive / votes, 4) if votes else 0.0,
        "positive": positive,
        "negative": negative,
        "recommendations": to_int(game.get("recommendations")),
        "downloads": parse_owners(game.get("estimated_owners", "")),
    }

def build_inverted_index(games):
    """Build a term index with field frequencies and matching document IDs."""
    postings = {}
    fields = ("title_bow", "description_bow", "tags_bow", "genres_bow")

    for app_id, game in games:
        document_id = str(app_id)
        record = build_record(game)
        field_bows = [
            record["title_bow"],
            record["description_bow"],
            record["tags_bow"],
            record["genres_bow"],
        ]

        for field_index, field_bow in enumerate(field_bows):
            for term, frequency in field_bow.items():
                entry = postings.setdefault(
                    term,
                    {"frequency": [0, 0, 0, 0], "docList": []},
                )
                entry["frequency"][field_index] += frequency
                if document_id not in entry["docList"]:
                    entry["docList"].append(document_id)

    return postings


def iter_games(data_path=DATA_PATH, items_prefix="games"):
    with open(data_path, "rb") as f:
        # use_float=True: otherwise ijson returns Decimal, which json can't write
        for app_id, game in ijson.kvitems(f, items_prefix, use_float=True):
            if isinstance(game, dict):
                yield app_id, game


def test_inverted_index():
    """Print the inverted index generated from the mini dataset."""
    inverted_index = build_inverted_index(iter_games())
    print("Inverted index for miniDataSet.json:")
    print(json.dumps(inverted_index, indent=2))


def main():
    total = 0
    with open(PREPROCESSED_OUT_PATH, "w", encoding="utf-8") as out:
        out.write("{\n")
        for app_id, game in iter_games():
            if total:
                out.write(",\n")
            out.write(json.dumps(app_id) + ":" + json.dumps(build_record(game), separators=(",", ":")))

            total += 1
            if total % 1000 == 0:
                print("finished " + str(total))
        out.write("\n}\n")

    print(f"done: wrote {total} games to {PREPROCESSED_OUT_PATH}")


if __name__ == "__main__":
    main()
    test_inverted_index()