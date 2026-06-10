import sqlite3
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FinBiz API is running"}


@app.get("/events")
def get_events():
    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, link, source, approved FROM events")
    rows = cursor.fetchall()

    connection.close()

    events = []

    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "link": row[2],
            "source": row[3],
            "approved": row[4]
        })

    return events

@app.put("/events/{event_id}/approve")
def approve_event(event_id: int):
    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE events SET approved = 1 WHERE id = ?",
        (event_id,)
    )

    connection.commit()
    connection.close()

    return {"message": f"Event {event_id} approved"}

@app.get("/approved-events")
def approved_events():
    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, source
        FROM events
        WHERE approved = 1
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "link": row[2],
            "source": row[3]
        }
        for row in rows
    ]