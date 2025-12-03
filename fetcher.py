import os
import requests
from dotenv import load_dotenv
from config import NICHE_KEYWORDS, MAX_ARTICLES

load_dotenv()

def fetch_news():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("ERROR: NEWS_API_KEY not set in .env")
        return []

    query = " OR ".join([f'"{kw}"' if " " in kw else kw for kw in NICHE_KEYWORDS])

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"language=en&"
        # f"sortBy=publishedAt&"
        f"sortBy=relevancy&"
        f"pageSize={MAX_ARTICLES}&"
        f"apiKey={api_key}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])
    return [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
        }
        for a in articles
    ]
