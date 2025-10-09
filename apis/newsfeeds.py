"""
News feed aggregator for all categories using NewsData.io API.
Provides unified article structure with caching support.
"""

import requests
import os
from utils.cache import get_cache, set_cache

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")

# Query mappings per category
CATEGORY_QUERIES = {
    "crypto": "cryptocurrency OR bitcoin OR blockchain OR ethereum",
    "stocks": "stock market OR finance OR earnings OR trading",
    "ecommerce": "e-commerce OR shopping OR retail OR amazon",
    "entertainment": "music OR movies OR celebrity OR hollywood",
    "sports": "sports OR football OR basketball OR nba OR f1",
    "home": "trending OR technology OR business OR world news"
}


def get_articles(category, limit=10):
    """
    Fetch news articles for a specific category with caching.

    Args:
        category: Category name (crypto, stocks, ecommerce, entertainment, sports)
        limit: Maximum number of articles to return (default: 10)

    Returns:
        List of article dictionaries with unified structure
    """
    cache_key = f"news_{category}"

    # Check cache first (15 minute TTL)
    cached = get_cache(cache_key)
    if cached:
        return cached[:limit]

    # Fallback if no API key
    if not NEWS_API_KEY:
        print(f"[NEWSFEEDS] No API key, using mockdata for {category}")
        return _load_fallback(category, limit)

    # Build API request
    query = CATEGORY_QUERIES.get(category, "trending")
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "q": query,
        "language": "en",
        "size": limit
    }

    try:
        print(f"[NEWSFEEDS] Fetching {category} articles from NewsData.io...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "success":
            raise Exception(f"API returned status: {data.get('status')}")

        # Transform to unified structure
        articles = [
            {
                "title": article["title"],
                "description": article.get("description", "")[:200],  # Limit description length
                "source": article.get("source_id", "Unknown"),
                "url": article["link"],
                "image": article.get("image_url") or "/static/placeholder.svg",
                "published": article.get("pubDate", "")
            }
            for article in data.get("results", [])
        ]

        # Cache for 15 minutes (900 seconds)
        set_cache(cache_key, articles, ttl=900)

        print(f"[NEWSFEEDS] Fetched {len(articles)} articles for {category}")
        return articles[:limit]

    except Exception as e:
        print(f"[NEWSFEEDS ERROR] {category}: {e}")
        return _load_fallback(category, limit)


def _load_fallback(category, limit=10):
    """
    Load mockdata as fallback when API fails.
    Transforms mockdata to match news article structure.

    Args:
        category: Category name
        limit: Maximum number of items to return

    Returns:
        List of articles from mockdata with unified structure
    """
    import json
    mockdata_path = f"static/mockdata/{category}.json"

    try:
        with open(mockdata_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Transform mockdata to news article format
            articles = []
            for item in data[:limit]:
                article = {
                    "title": item.get("title") or item.get("name") or item.get("keyword") or "Untitled",
                    "description": item.get("description", "")[:200],
                    "source": item.get("source", "TrendWatcher"),
                    "url": item.get("url", "#"),  # Mockdata has no URL
                    "image": item.get("image") or item.get("thumb") or "/static/placeholder.svg",
                    "published": ""
                }
                articles.append(article)

            print(f"[NEWSFEEDS] Loaded {len(articles)} articles from {mockdata_path}")
            return articles
    except Exception as e:
        print(f"[NEWSFEEDS ERROR] Failed to load fallback: {e}")
        return []
