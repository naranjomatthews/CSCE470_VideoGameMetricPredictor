import json, re

class GameData:

    # features to retrieve from the preprocessedJSON.
    GAME_FIELDS = [
        "name", # title
        "about_the_game", # shorter description
        "tags",
        "genres",
        "rating",
        "positive",
        "negative",
        "recommendations",
        "metacritic_score"
    ]

    def __init__(self, data_dir):

        self.data_dir = data_dir
        self.RAW_GAMES_PATH = data_dir / "games.json"
        
        with open(self.RAW_GAMES_PATH, "r", encoding="utf-8") as file:
            self.gameData = json.load(file)


    def loadGameData(self, filePath):
        with open(filePath, "r", encoding="utf-8") as file:

            # convert JSON data into a dictionary using appid as keys
            gameData = json.load(file)

        return gameData


    def getGameData(self, docIDs):
        results = []

        for docID in docIDs:
            docID = str(docID)
            if docID not in self.gameData:
                continue

            # retrieve game information using given ID.
            game = self.gameData[docID]

            # create a dictionary for the current game's information.
            selectedGame = {"docID": docID}

            tags = game.get("tags", [])
            if isinstance(tags, dict):
                tags = list(tags.keys())

            # retrieve review counts
            positive = int(game.get("positive") or 0)
            negative = int(game.get("negative") or 0)
            votes = positive + negative

            #retrieve number of estimated owners
            owner_numbers = re.findall(r"\d+", str(game.get("estimated_owners", "")).replace(",", ""))

            #retrieve download estimates
            downloads = (sum(int(n) for n in owner_numbers) if owner_numbers else 0)

            # store the relevant game info in the dict
            selectedGame.update({
                "title": game.get("name", ""),
                "description": game.get("about_the_game", "") or game.get("short_description", ""),
                "tags": tags,
                "genres": game.get("genres", []),
                "rating": round(positive / votes, 4) if votes else 0.0,
                "positive": positive,
                "negative": negative,
                "recommendations": int(game.get("recommendations") or 0),
                "downloads": downloads
            })

            # add the current game to the results list
            results.append(selectedGame)
        
        return results

# test code
if __name__ == "__main__":

    pass 

    # # load game data from preprocessed JSON
    # gameData = loadGameData("game_data.json")

    # docIDs = ["688420", "496350", "1025440"]

    # # retrieve features of the given games using their ids and JSON data
    # results = getGameData(docIDs, gameData)

    # for game in results:
    #     print(game)