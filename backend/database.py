import sqlite3

DB_NAME = "finbiz.db"

def create_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            source TEXT NOT NULL,
            approved INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def save_event(title, link, source):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO events (title, link, source)
            VALUES (?, ?, ?)
        """, (title, link, source))

        connection.commit()
        print(f"Saved: {title}")

    except sqlite3.IntegrityError:
        print(f"Already exists: {title}")

    connection.close()