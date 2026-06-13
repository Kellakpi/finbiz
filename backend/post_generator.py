def generate_post(title, description, link, event_date=None, event_location=None):
    date_line = f"📅 {event_date}\n" if event_date else ""
    location_line = f"📍 {event_location}\n" if event_location else ""

    return f"""
📌 {title}

{date_line}{location_line}
{description}

🔗 Register here:
{link}
"""