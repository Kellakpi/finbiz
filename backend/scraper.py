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
    save_event(
        event["title"],
        event["link"],
        event["source"]
    )