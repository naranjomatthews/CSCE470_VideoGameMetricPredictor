# CSCE470_VideoGameMetricPredictor

## Programs
1. process_data.py: handles both creation of inverse index and processing of games to retrieve relevant fields' bag-of-words, their lengths, and non-textual features
    - results in Data/preprocessed_games.json and Data/inverted_index.json
    - test data has already been provided and preprocessed for you 
2. bm25ranker.py: runs BM25F and returns details of the top X games by score
    - results in Data/search_results.json

## Dependencies
To run the BM25 demonstration program, you will need:
1. Python (preferably newer versions like 3.15)
2. ijson (installable with pip)

Other programs in this project require numpy and matplotlib as mentioned in requirements.txt

## Brief Remarks on File Structure
- The presence of a Data folder is crucial to run the indexing and ranking. Again, a test set is provided for demonstrative purposes. 

## Commands to run system

Test data and its preprocessed indexes have already been provided. To test the ranker, run the following from the project root:

```py -m ranking.bm25ranker```

Once ran, the user will be prompted for query in the terminal. Once the query is provided, successful execution records resulting rankings in search_results.json under the test_data directory.

FYI, the preprocessing program can be ran with:

```py -m Preprocessing.process_data```

But again, this has already been ran on test data and provided to you. 
