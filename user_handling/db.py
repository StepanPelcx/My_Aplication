from pathlib import Path
import sqlite3

#CONNECTING FUNCTION
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "database"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "intelligent_platform.db"


def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    conn = sqlite3.connect(str(db_path))
    return conn