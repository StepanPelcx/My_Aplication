import pandas as pd
from user_handling.db import connect_database
from pathlib import Path


def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.
    
    TODO: Implement this function following the register_user() pattern.
    
    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)
        
    Returns:
        int: ID of the inserted incident
    """
    # TODO: Get cursor
    conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write INSERT SQL with parameterized query
    # TODO: Execute and commit
    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by)
    )
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    # TODO: Return cursor.lastrowid
    return incident_id


def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC", conn
    )
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    """Update the status of an incident."""
    """
    TODO: Implement UPDATE operation.
    """
    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    cur.execute(
                """UPDATE cyber_incidents SET status = ? WHERE id = ?""",
                (new_status, incident_id)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return cur.rowcount


def delete_incident(incident_id):
    """Delete an incident from the database."""
    """
    TODO: Implement DELETE operation.
    """
    conn = connect_database()
    cur = conn.cursor()
    # TODO: Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    cur.execute(
                """DELETE FROM cyber_incidents WHERE id = ?""",
                (incident_id,)
                )
    # TODO: Execute and commit
    conn.commit()
    rowcount = cur.rowcount
    conn.close()
    # TODO: Return cursor.rowcount
    return rowcount



def get_incidents_by_type_count():
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn)
    return df


def get_high_severity_by_status():
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    conn = connect_database()
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df


def migrate_incidents():
    """Migrates all the incidents from csv file"""
    #getting the path
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "database"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DATA_DIR / "cyber_incidents.csv"

    df = pd.read_csv(DB_PATH)

    if not df.empty:
        for index, row in df.iterrows():
            insert_incident(
                date=str(row["date"]),
                incident_type=row["incident_type"],
                severity=row["severity"],
                status=row["status"],
                description=row["description"],
                reported_by=row.get("reported_by")
            )
        return True
    return False


