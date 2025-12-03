import pandas as pd
from user_handling.db import connect_database
from datetime import date

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb, created_at):
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


def update_dataset_record_count(conn, dataset_id, new_record_count):
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


def delete_dataset(conn, dataset_id):
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


def get_datasets_by_category_count(conn):
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
    df = pd.read_sql_query(query, conn)
    return df


def get_repeating_dataset_categories(conn, min_count=5):
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
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df