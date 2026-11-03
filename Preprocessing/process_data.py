from pathlib import Path
import re
import html 
import ijson 

DATA_PATH = Path(__file__).parent.parent / "Data" / "games.json"

# tokenizer pieces
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

REMOVE_STOPWORDS = False
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


def iter_games():
    with open(DATA_PATH, "rb") as f:
        # Yields (app_id, game_dict) one at a time, never the whole file
        for _, game in ijson.kvitems(f, ""):
            if isinstance(game, dict):
                yield game


def main():

    for game in iter_games():

        total += 1
        title = game.get("name", "")
        description = game.get("about_the_game", "")

        tags = game.get("tags")
        categories = game.get("categories")

        title_tokens = tokenize(title)
        desc_tokens = tokenize(description)


        if total % 1000 == 0:
            print("finished " + str(total))

    pass 


if __name__ == "__main__":
    main()