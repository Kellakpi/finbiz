import requests
from bs4 import BeautifulSoup
from database import create_table, save_event

url = "https://www.eventbrite.co.uk/d/united-kingdom--london/finance/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

seen = set()
events = []

# Ensure the database table exists before scraping
create_table()


# Extract additional event information from an Eventbrite event page
def get_event_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("title")
    page_title = title_tag.text.strip() if title_tag else ""

    if title_tag:
        print("PAGE TITLE:", title_tag.text.strip())

    description_tag = soup.find("meta", attrs={"name": "description"})
    image_tag = soup.find("meta", property="og:image")

    description = description_tag["content"] if description_tag else None
    image_url = image_tag["content"] if image_tag else None

    # Extract event date from the Eventbrite page title
    event_date = None

    if "Tickets," in page_title:
        try:
            event_date = page_title.split("Tickets,")[1].split("•")[0].strip()
        except Exception:
            pass

    # Extract location from the event description
    event_location = None

    if description and " at " in description:
        try:
            event_location = description.split(" at ")[1]
            event_location = event_location.split(". Find event")[0]
        except Exception:
            pass

    return description, image_url, event_date, event_location


# Collect unique event links from the Eventbrite search page
for link in soup.find_all("a"):
    href = link.get("href")
    title = link.get_text(strip=True)

    if href and "/e/" in href and title and href not in seen:
        seen.add(href)

        events.append({
            "title": title,
            "link": href,
            "source": "Eventbrite"
        })

print(events)
print(f"Found {len(events)} events")

# Save each discovered event to the database
for event in events:
    description, image_url, event_date, event_location = get_event_details(event["link"])

    save_event(
        event["title"],
        event["link"],
        event["source"],
        description,
        image_url,
        event_date,
        event_location
    )