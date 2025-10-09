"""
Affiliate link generator for monetization.
Supports Amazon, eToro, and other affiliate programs.
"""

import os
from urllib.parse import quote_plus

# Affiliate tags from environment variables
AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "trendwatcher-21")
ETORO_SOURCE = os.getenv("ETORO_SOURCE", "trendwatcher")
BOL_COM_AFFILIATE_ID = os.getenv("BOL_COM_AFFILIATE_ID", "")


def generate_amazon_link(product_name):
    """
    Generate Amazon affiliate link for a product.

    Args:
        product_name: Product name or keyword

    Returns:
        Amazon search URL with affiliate tag
    """
    encoded_name = quote_plus(product_name)
    return f"https://www.amazon.com/s?k={encoded_name}&tag={AMAZON_AFFILIATE_TAG}"


def generate_etoro_link(symbol):
    """
    Generate eToro broker affiliate link for a stock symbol.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "TSLA")

    Returns:
        eToro market URL with UTM tracking
    """
    symbol_lower = symbol.lower()
    return f"https://www.etoro.com/markets/{symbol_lower}?utm_source={ETORO_SOURCE}"


def generate_bolcom_link(product_name):
    """
    Generate Bol.com affiliate link (Dutch market).

    Args:
        product_name: Product name

    Returns:
        Bol.com partner link or regular search link
    """
    if not BOL_COM_AFFILIATE_ID:
        # Fallback to regular search if no affiliate ID
        encoded_name = quote_plus(product_name)
        return f"https://www.bol.com/nl/nl/s/?searchtext={encoded_name}"

    encoded_name = quote_plus(product_name)
    return f"https://partner.bol.com/click/click?p=1&t=url&s={BOL_COM_AFFILIATE_ID}&name={encoded_name}"


def add_affiliate_to_article(article, category):
    """
    Add affiliate URL to article based on category.

    Args:
        article: Article dictionary
        category: Category name (crypto, stocks, ecommerce, etc.)

    Returns:
        Article with affiliate_url added
    """
    if category == "ecommerce":
        # E-commerce gets Amazon affiliate links
        product_name = article.get("title") or article.get("name") or article.get("keyword", "")
        article["affiliate_url"] = generate_amazon_link(product_name)
        article["affiliate_label"] = "Shop on Amazon"

    elif category == "stocks":
        # Stocks get eToro broker links
        symbol = article.get("symbol", "")
        if symbol:
            article["affiliate_url"] = generate_etoro_link(symbol)
            article["affiliate_label"] = "Trade on eToro"

    return article


def add_affiliate_to_articles(articles, category):
    """
    Bulk add affiliate URLs to list of articles.

    Args:
        articles: List of article dictionaries
        category: Category name

    Returns:
        Articles with affiliate URLs added
    """
    return [add_affiliate_to_article(article, category) for article in articles]
