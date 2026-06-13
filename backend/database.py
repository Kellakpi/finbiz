import sqlite3

DB_NAME = "finbiz.db"

# Create the events table if it does not already exist
def create_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        source TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        description TEXT,
        image_url TEXT,
        event_date TEXT,
        event_location TEXT
        )
    """)

    connection.commit()
    connection.close()


# Save a newly discovered event to the database
def save_event(title, link, source, description=None, image_url=None, event_date=None, event_location=None):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO events (
                title, link, source, description, image_url, event_date, event_location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, link, source, description, image_url, event_date, event_location))

        connection.commit()
        print(f"Saved: {title}")

    # Prevent duplicate events from being added
    except sqlite3.IntegrityError:
        print(f"Already exists: {title}")

    connection.close()