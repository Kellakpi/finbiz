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
create_table()


def get_event_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    description_tag = soup.find("meta", attrs={"name": "description"})
    image_tag = soup.find("meta", property="og:image")

    description = description_tag["content"] if description_tag else None
    image_url = image_tag["content"] if image_tag else None

    return description, image_url


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
for event in events:
    description, image_url = get_event_details(event["link"])

    save_event(
        event["title"],
        event["link"],
        event["source"],
        description,
        image_url
    )