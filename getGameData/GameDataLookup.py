import json

# features to retrieve from the preprocessedJSON.
GAME_FIELDS = [
    "title",
    "description",
    "tags",
    "genres",
    "rating",
    "positive",
    "negative",
    "recommendations",
    "downloads"
]


def loadGameData(filePath):
    with open(filePath, "r", encoding="utf-8") as file:

        # convert JSON data into a dictionary using appid as keys
        gameData = json.load(file)

    return gameData


def getGameData(docIDs, gameData):
    results = []

    for docID in docIDs:
        docID = str(docID)
        if docID not in gameData:
            continue

        # retrieve game information using given ID.
        game = gameData[docID]

        # create a dictionary for the current game's information.
        selectedGame = {"docID": docID}

        # retrieve the features of the current game and add them to the selectedGame dictionary.
        for field in GAME_FIELDS:
            selectedGame[field] = game.get(field)

        # add the current game to the results list
        results.append(selectedGame)

    return results


# test code
if __name__ == "__main__":

    # load game data from preprocessed JSON
    gameData = loadGameData("game_data.json")

    docIDs = ["688420", "496350", "1025440"]

    # retrieve features of the given games using their ids and JSON data
    results = getGameData(docIDs, gameData)

    for game in results:
        print(game)