from pathlib import Path
import re
import html 
import ijson 

DATA_PATH = Path(__file__).parent.parent / "Preprocessing" / "miniDataSet.json"

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


def tokenize_labels(values):
    """Tokenize labels from a tags dictionary or genres list."""
    if isinstance(values, dict):
        values = values.keys()
    elif not isinstance(values, list):
        return []

    tokens = []
    for value in values:
        tokens.extend(tokenize(value))
    return tokens


def iter_games():
    with open(DATA_PATH, "rb") as f:
        # Yields (app_id, game_dict) one at a time, never the whole file
        for _, game in ijson.kvitems(f, "games"):
            if isinstance(game, dict):
                yield game


def main():

    total = 0
    for game in iter_games():

        total += 1
        title = game.get("name", "")
        description = game.get("about_the_game", "")
        tags = game.get("tags")
        genres = game.get("genres")

        title_tokens = tokenize(title)
        desc_tokens = tokenize(description)
        tag_tokens = tokenize_labels(tags)
        genre_tokens = tokenize_labels(genres)
        print("words in title: " + str(title_tokens)) 
        print("words in description: " + str(desc_tokens))
        print("words in tags: " + str(tag_tokens))
        print("words in genres: " + str(genre_tokens))

        if total % 1000 == 0:
            print("finished " + str(total))

    


if __name__ == "__main__":
    main()