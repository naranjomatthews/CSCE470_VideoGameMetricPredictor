from pathlib import Path

TESTING = True
PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / ("test_data" if TESTING else "Data")
DATA_PATH = DATA_DIR / "games.json"

SUMMARIES_DIR = PROJECT_ROOT / "summaries"
PLOT_DIR = SUMMARIES_DIR / "plots"
TEXT_SUMMARIES_DIR = SUMMARIES_DIR / "text_summaries"