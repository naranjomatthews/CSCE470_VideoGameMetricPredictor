from pathlib import Path
import math
import ijson
import json

#how many games will be output in final ranking
topX = 10

#paths to access game and inverted index data
DATA_FOLDER = DATA_PATH = Path(__file__).parent.parent / "Data" 
GAMES_PATH = DATA_FOLDER / "preprocessed_games.json"
INVERTED_INDEX_PATH = DATA_FOLDER / "inverted_index.json"

class bm25ranker:

    def __init__(self):
        
        self.k1 = 1.0
        self.gameCount = 0.0 

        """
        collection of fields and their relevant data, can be manually adjusted to
        incorporate
            -lengthKey - allows retrieval of field length from preprocessed game data
            -bowKey - allows retrieval of field bow from preprocessed game data
            -weight - the general weight of the given field
            -bWeight - the BM25 specific weight of the given field
            -avgLength - average length of the field
        """
        self.fieldData = {
            "title" : {
                "lengthKey" : "title_length",
                "bowKey" : "title_bow",
                "weight" : 0.9,
                "bWeight" : 0.5,
                "avgLength" : 0.0
            },
            "description" : {
                "lengthKey" : "description_length",
                "bowKey" : "description_bow",
                "weight" : 0.1,
                "bWeight" : 0.5,
                "avgLength" : 0.0
            },
            "tags" : {
                "lengthKey" : "tags_length",
                "bowKey" : "tags_bow",
                "weight" : 0.9,
                "bWeight" : 0.5,
                "avgLength" : 0.0
            },
            "genres" : {
                "lengthKey" : "genres_length",
                "bowKey" : "genres_bow",
                "weight" : 0.9,
                "bWeight" : 0.5,
                "avgLength" : 0.0
            }
        }

        
        #collection of non-textual features, includes lambda and lambda prime of each
        #can be manually adjusted
        self.ntfs = {
            "rating" :{
                "lambda" : 0.1,
                "lambdaPrime" : 1.0
            },
            "positive" :{
                "lambda" : 0.1,
                "lambdaPrime" : 1.0
            },
            "negative" :{
                "lambda" : 0.1,
                "lambdaPrime" : 1.0
            },
            "recommendations" :{
                "lambda" : 0.1,
                "lambdaPrime" : 1.0
            },
            "downloads" :{
                "lambda" : 0.05,
                "lambdaPrime" : 1.0
            }
        }
        
        #dictionary of top X games and their scores: Game ID -> score
        self.topScores = {}

        #dictionary of non-textual feature scores
        self.ntfScores = {}


    def calculateScore(self,queryBow):
        with open(INVERTED_INDEX_PATH, "rb") as indexFile:
                index = json.load(indexFile)
                with open(GAMES_PATH, "rb") as gamesFile:
                    games = ijson.kvitems(gamesFile,'')
                    self.topScores= {}
                    count = 0
                    for gameID, game in games:
                        score = 0.0
                        fieldDenominators = {}
                        for field in self.fieldData.keys():
                            if(game[self.fieldData[field]["lengthKey"]] == 0):
                                continue
                            fieldDenominators[field] = ((1.0 - self.fieldData[field]["bWeight"]) + (self.fieldData[field]["bWeight"] * (game[self.fieldData[field]["lengthKey"]] / self.fieldData[field]["avgLength"])))

                        for term in queryBow.keys():
                            termWeight = 0.0
                            for field in self.fieldData.keys():
                                if((game[self.fieldData[field]["lengthKey"]] == 0) or (term not in game[self.fieldData[field]["bowKey"]])):
                                    continue
                                #print(str(gameID) + ": " + field + " denominator: " + str(fieldDenominators[field]))
                                normalizedTF = game[self.fieldData[field]["bowKey"]][term] / fieldDenominators[field]
                                termWeight += (self.fieldData[field]["weight"] * normalizedTF)
                                #print(str(gameID) + ": " + term + " frequency: " + str(game[self.fieldData[field]["bowKey"]][term]))
                                #print(str(gameID) + ": " + term + " normalized frequency: " + str(normalizedTF))
                                

                            
                            if(termWeight == 0.0):
                                continue
                            termIDF = math.log(self.gameCount / len(index[term]["docList"]))
                            adjWeight = (termWeight / (termWeight + self.k1))
                            score += (adjWeight * termIDF)

                        for ntf in self.ntfScores[gameID].keys():
                            score += self.ntfScores[gameID][ntf]

                        if(len(self.topScores) < topX):
                            #print(str(gameID) + " was added with score " + str(score))
                            self.topScores[gameID] = score
                        else:
                            self.updateTopScores(gameID,score)
                        #print()
                        #count += 1
                        #print("Check")
                        #if(count == 100):    
                        #    break
        return self.topScores 
        
        

    def updateTopScores(self,gameID,score):
        lowestScore = score
        lowestID = gameID
        for game in self.topScores.keys():
            if(self.topScores[game] < lowestScore):
                lowestScore = self.topScores[game]
                lowestID = game
        if(lowestID != gameID):
            #print(str(lowestID) + " was removed in update with score " + str(lowestScore))
            self.topScores.pop(lowestID)
            #print(str(gameID) + " was added in update with score " + str(score))
            self.topScores[gameID] = score


    def calcAverageFieldLengths(self):
        with open(GAMES_PATH, "rb") as gamesFile:
            games = ijson.kvitems(gamesFile,'')
            for gameID, game in games:
                self.gameCount += 1
                for key in self.fieldData.keys():
                    self.fieldData[key]["avgLength"] += game[self.fieldData[key]["lengthKey"]]

                self.ntfScores[gameID] = {}
                for ntf in self.ntfs.keys():
                    if((ntf == "negative") and (float(game[ntf]) > 0.0)):
                        self.ntfScores[gameID][ntf] = -(self.ntfs[ntf]["lambda"] * (math.log(self.ntfs[ntf]["lambdaPrime"] + float(game[ntf]))))
                    else:
                        self.ntfScores[gameID][ntf] = (self.ntfs[ntf]["lambda"] * (math.log(self.ntfs[ntf]["lambdaPrime"] + float(game[ntf]))))

                    #print(str(gameID) + " : " + str(ntf) + " : " + str(float(game[ntf])) + " : " + str(math.log(self.ntfs[ntf]["lambdaPrime"])) + " : " + str(self.ntfScores[gameID][ntf]))
                #print()
                #if(totalGames == 10):
                    #break
                #break
            
            for key in self.fieldData.keys():
                self.fieldData[key]["avgLength"] /= self.gameCount 


def main():
    bm25f = bm25ranker()
    
    #get the games and inverted index
    #games = ijson.kvitems(open(GAMES_PATH, "rb"),'')
    #invertedIndex = ijson.kvitems(open(INVERTED_INDEX_PATH, "rb"),'')
    
    bm25f.calcAverageFieldLengths()
    #for now, the ranker will take in queries by command line, this will change with the UI
    while(True):
        query = input("Enter query to search(leave blank to exit): ")
        if(query == ""):
            break
    
        #construct bag of words for query
        queryBow= {}
        queryWords = query.lower().split()
        for word in queryWords:
            if(word not in queryBow.keys()):
                queryBow[word] = 1
            else:
                queryBow[word] += 1
        
        topGames = bm25f.calculateScore(queryBow)
        for game in topGames.keys():
             print(str(game) + ": " + str(topGames[game]))

if __name__ == "__main__":
    main()