

from bs4 import BeautifulSoup
import requests

dateHeaders = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def findDatesOnePlayer(link: str):
    try:
        page = requests.get(link, headers=dateHeaders, timeout=20)
        page.raise_for_status()
    except requests.RequestException as e:
        raise
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.prettify())

# findDatesOnePlayer("https://www.sofascore.com/basketball/player/daniel-saylor/2286273")


url = "https://api.sofascore.com/api/v1/player/2286273"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}

response = requests.get(url, headers=headers, timeout=20)

print("Status:", response.status_code)
print("Headers:", dict(response.headers))
print("Body:", response.text[:500])
