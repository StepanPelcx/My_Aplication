from user_handling.db import connect_database


def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    return print("✅ Users table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    return print("✅ All tables created successfully!")

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    
    TODO: Implement this function following the users table example above.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - date: TEXT (format: YYYY-MM-DD)
    - incident_type: TEXT (e.g., 'Phishing', 'Malware', 'DDoS')
    - severity: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'Investigating', 'Resolved', 'Closed')
    - description: TEXT
    - reported_by: TEXT (username of reporter)
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Get a cursor from the connection
    #conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write CREATE TABLE IF NOT EXISTS SQL statement
    # Follow the pattern from create_users_table()
    statement = ("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # TODO: Execute the SQL statement
    cursor.execute(statement)
    # TODO: Commit the changes
    conn.commit()
    # TODO: Print success message
    return print("✅ Cyber incidents table created successfully!")
    pass


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    
    TODO: Implement this function following the users table example.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - dataset_name: TEXT NOT NULL
    - category: TEXT (e.g., 'Threat Intelligence', 'Network Logs')
    - source: TEXT (origin of the dataset)
    - last_updated: TEXT (format: YYYY-MM-DD)
    - record_count: INTEGER
    - file_size_mb: REAL
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Implement following the users table pattern
    # TODO: Get a cursor from the connection
    #conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write CREATE TABLE IF NOT EXISTS SQL statement
    # Follow the pattern from create_users_table()
    statement = ("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # TODO: Execute the SQL statement
    cursor.execute(statement)
    # TODO: Commit the changes
    conn.commit()
    # TODO: Print success message
    return print("✅ Datasets metadata table created successfully!")
    pass


def create_it_tickets_table(conn):
    """
    Create the it_tickets table.
    
    TODO: Implement this function following the users table example.
    
    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - ticket_id: TEXT UNIQUE NOT NULL
    - priority: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed')
    - category: TEXT (e.g., 'Hardware', 'Software', 'Network')
    - subject: TEXT NOT NULL
    - description: TEXT
    - created_date: TEXT (format: YYYY-MM-DD)
    - resolved_date: TEXT
    - assigned_to: TEXT
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Implement following the users table pattern
    # TODO: Get a cursor from the connection
    #conn = connect_database()
    cursor = conn.cursor()
    # TODO: Write CREATE TABLE IF NOT EXISTS SQL statement
    # Follow the pattern from create_users_table()
    statement = ("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            status TEXT,
            category TEXT,
            subject TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            resolved_date TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # TODO: Execute the SQL statement
    cursor.execute(statement)
    # TODO: Commit the changes
    conn.commit()
    # TODO: Print success message
    return print("✅ It tickets table created successfully!")
    pass
