import requests
from bs4 import BeautifulSoup

url = "https://www.eventbrite.com/e/world-finance-forum-london-tickets-1990098948527?aff=ebdssbdestsearch"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("h1")

print("TITLE:")
print(title.get_text(strip=True) if title else "No title found")

print("\nPAGE TITLE:")
print(soup.title.get_text(strip=True) if soup.title else "No page title found")

print("\nMETA DESCRIPTION:")
description = soup.find("meta", attrs={"name": "description"})
print(description["content"] if description else "No description found")

print("\nIMAGE:")
image = soup.find("meta", property="og:image")
print(image["content"] if image else "No image found")

#Functions

print("\nWHATSAPP POST:")
print(f"""
📌 {title.get_text(strip=True) if title else "No title found"}

{description["content"] if description else "No description found"}

🔗 Register here:
{url}
""")

