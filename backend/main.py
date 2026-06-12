import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="backend/templates")

@app.get("/")
def home(request: Request):

    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, description, image_url
        FROM events
        WHERE approved = 0
    """)

    rows = cursor.fetchall()

    connection.close()

    events = []

    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "link": row[2],
            "description": row[3],
            "image_url": row[4]
        })

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "events": events
        }
    )


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

@app.post("/events/{event_id}/approve")
def approve_event(event_id: int):
    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE events SET approved = 1 WHERE id = ?",
        (event_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)

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

@app.get("/approved")
def approved_page(request: Request):

    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, description, image_url
        FROM events
        WHERE approved = 1
    """)

    rows = cursor.fetchall()

    connection.close()

    events = []

    for row in rows:
       events.append({
        "id": row[0],
        "title": row[1],
        "link": row[2],
        "description": row[3],
        "image_url": row[4]
    })

    return templates.TemplateResponse(
        request=request,
        name="approved.html",
        context={
            "events": events
        }
    )

from backend.post_generator import generate_post

@app.get("/events/{event_id}/preview")
def preview_event(request: Request, event_id: int):

    connection = sqlite3.connect("finbiz.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, description, link
        FROM events
        WHERE id = ?
    """, (event_id,))

    row = cursor.fetchone()

    connection.close()

    if not row:
        return {"error": "Event not found"}

    post = generate_post(
        row[0],
        row[1],
        row[2]
    )

    return templates.TemplateResponse(
        request=request,
        name="preview.html",
        context={
            "title": row[0],
            "post": post,
            "link": row[2]
        }
    )