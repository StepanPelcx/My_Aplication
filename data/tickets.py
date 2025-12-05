import pandas as pd
from user_handling.db import connect_database
from pathlib import Path

def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at):
    """Insert a new dataset into the database."""
    # TODO: Get cursor
    conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write INSERT SQL with parameterized query
    # TODO: Execute and commit
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at)
    )
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    # TODO: Return cursor.lastrowid
    return ticket_id


def get_all_tickets():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC", conn
    )
    conn.close()
    return df


def update_ticket_status(ticket_id, new_status):
    """Update the status of a ticket."""
    """
    TODO: Implement UPDATE operation.
    """
    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write UPDATE SQL: UPDATE it_tickets SET status = ? WHERE id = ?
    cur.execute(
                """UPDATE it_tickets SET status = ? WHERE id = ?""",
                (new_status, ticket_id)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return cur.rowcount


def delete_ticket(ticket_id):
    """Delete a ticket from the database."""
    """
    TODO: Implement DELETE operation.
    """
    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write DELETE SQL: DELETE FROM it_tickets WHERE id = ?
    cur.execute(
                """DELETE FROM it_tickets WHERE id = ?""",
                (ticket_id,)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return rowcount


def get_tickets_by_category_count():
    """
    Count categories by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM it_tickets
    GROUP BY category
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn)
    return df


def get_tickets_by_status(status="Open"):
    """Returns tickets with given status."""

    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets WHERE status = ?", 
        conn,
        params=(status,)
    )
    conn.close()
    return df   


def migrate_datasets():
    """Migrates all tickets info from the CSV file."""
    #getting the path
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "database"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DATA_DIR / "it_tickets.csv"

    df = pd.read_csv(DB_PATH)

    if not df.empty:
        for index, row in df.iterrows():
            insert_ticket(
                ticket_id=row["ticket_id"],
                priority=row["priority"],
                status=row["status"],
                category=row["category"],
                subject=row["subject"],
                description=row["description"],
                created_date=str(row["created_date"]),
                resolved_date=str(row["resolved_date"]) if not pd.isna(row["resolved_date"]) else None,
                assigned_to=row["assigned_to"],
                created_at=str(row["created_at"])
            )
        return True
    return False