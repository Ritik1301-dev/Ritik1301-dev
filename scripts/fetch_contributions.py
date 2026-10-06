import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

USERNAME = "Ritik1301-dev"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for rect in soup.select("td.ContributionCalendar-day"):
    date = rect.get("data-date")
    count = rect.get("data-level")

    if date:
        days.append({
            "date": date,
            "level": int(count or 0)
        })

output = Path("data/contributions.json")
output.parent.mkdir(exist_ok=True)

with open(output, "w", encoding="utf-8") as f:
    json.dump(days, f, indent=2)

print(f"Saved {len(days)} contribution days.")