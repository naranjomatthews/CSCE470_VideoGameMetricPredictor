# CSCE470_VideoGameMetricPredictor

## Programs
1. process_data.py: handles both creation of inverse index and processing of games to retrieve relevant fields' bag-of-words, their lengths, and non-textual features
    - results in Data/preprocessed_games.json and Data/inverted_index.json
2. bm25ranker.py: runs BM25F and returns details of the top X games by score
    - results in Data/rankings.json

## Dependencies
Ensure the following are installed:
1. Python (preferably newer versions like 3.15)
2. Packages like ijson, numpy, and matplotlib as mentioned in requirements.txt

As long as the aforementioned packages are installed, there should be no issues

## Brief Remarks on File Structure
- The presence of the Data folder is crucial to run the indexing and ranking. Programs WILL fail without it
- Preferable to navigate into Preprocessing folder when running preprocessor
- Preferable to navigate into ranking folder when running preprocessor

## Commands to run system

To run the preprocessing, use the following command:

```python process_data.py```

Successful executiion should show writing of 200 games to preprocessed_games.json

To run the ranking, use the following command:

```python bm25ranker.py```

User is prompted for query. Once query is provided, successful execution records resultant ranking and provided query in rankings.json