import pandas as pd
from user_handling.db import connect_database
from datetime import date
from pathlib import Path

def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb, created_at):
    """Insert a new dataset into the database."""
    # TODO: Get cursor
    conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write INSERT SQL with parameterized query
    # TODO: Execute and commit
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb, created_at)
    )
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    # TODO: Return cursor.lastrowid
    return dataset_id


def get_all_datasets():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC", conn
    )
    conn.close()
    return df


def update_dataset_record_count(dataset_id, new_record_count):
    """Update the status of a dataset."""
    """
    TODO: Implement UPDATE operation.
    """
    last_updated = date.today()

    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write UPDATE SQL: UPDATE datasets_metadata SET status = ? WHERE id = ?
    cur.execute(
                """UPDATE datasets_metadata SET record_count = ?, last_updated = ? WHERE id = ?""",
                (new_record_count, last_updated, dataset_id)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return cur.rowcount


def delete_dataset(dataset_id):
    """Delete a dataset from the database."""
    """
    TODO: Implement DELETE operation.
    """
    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write DELETE SQL: DELETE FROM datasets_metadata WHERE id = ?
    cur.execute(
                """DELETE FROM datasets_metadata WHERE id = ?""",
                (dataset_id,)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return rowcount


def get_datasets_by_category_count():
    """
    Count categories by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn)
    return df


def get_repeating_dataset_categories(min_count=5):
    """
    Find datasets with more than min_count same category type.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df


def migrate_datasets():
    """Migrates all datasets info from the CSV file."""
    #getting the path
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "database"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DATA_DIR / "datasets_metadata.csv"

    df = pd.read_csv(DB_PATH)

    if not df.empty:
        for index, row in df.iterrows():
            insert_dataset(
                dataset_name=row["dataset_name"],
                category=row["category"],
                source=row["source"],
                last_updated=str(row["last_updated"]),
                record_count=int(row["record_count"]),
                file_size_mb=float(row["file_size_mb"]),
                created_at=str(row["created_at"])
            )
        return True
    return False


