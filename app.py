"""
TrendWatcher - Multi-Theme Flask Webapp
========================================
Multi-market trending data met per-category themes.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from apis.coingecko import get_trending_crypto
from apis.stocks import get_trending_stocks
from apis.ecommerce import get_trending_ecommerce
from apis.entertainment import get_trending_entertainment
from apis.sports import get_trending_sports
from apis.newsfeeds import get_articles
from utils.affiliates import add_affiliate_to_articles
from datetime import datetime
import os
import json
import threading

app = Flask(__name__)

# Google Analytics tracking ID
GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID', 'G-HP85ZJG199')

# Vote storage
VOTES_FILE = "data/votes.json"
_vote_lock = threading.Lock()

# ========== MOCKDATA HELPER ==========

def load_mock(category):
    """
    Load mock data from JSON file as fallback.

    Args:
        category (str): Category name (crypto, stocks, ecommerce, entertainment, sports)

    Returns:
        list: Mock data or empty list if file not found
    """
    path = f"static/mockdata/{category}.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading mock data for {category}: {e}")
            return []
    return []

# Helper functions voor demo data
def get_demo_gainers():
    """Top gainers voor sidebar"""
    stocks = get_trending_stocks()
    if stocks:
        return [{"symbol": s['symbol'], "change": s['change_percentage']}
                for s in stocks if s.get('trend_type') == 'gainer'][:5]
    return [
        {"symbol": "SPRB", "change": "+1434%"},
        {"symbol": "SOPA", "change": "+275%"},
        {"symbol": "TSLA", "change": "+12%"}
    ]

def get_demo_losers():
    """Top losers voor sidebar"""
    stocks = get_trending_stocks()
    if stocks:
        return [{"symbol": s['symbol'], "change": s['change_percentage']}
                for s in stocks if s.get('trend_type') == 'loser'][:5]
    return [
        {"symbol": "DOGE", "change": "-15%"},
        {"symbol": "META", "change": "-8%"}
    ]

def get_demo_articles():
    """Demo articles voor homepage"""
    return [
        {"title": "Bitcoin surge breekt records", "teaser": "Crypto markt ziet unprecedented groei."},
        {"title": "AI Gadgets domineren e-commerce", "teaser": "Nieuwe tech trends in shopping."},
        {"title": "Premier League dramatiek", "teaser": "Laatste matchday highlights."},
        {"title": "Stock market volatiliteit", "teaser": "Analyse van huidige bewegingen."},
        {"title": "YouTube trending explodeert", "teaser": "Nieuwe viral content trends."},
    ]

# ========== VOTE FUNCTIONS ==========

def _read_votes():
    """Read votes from JSON file"""
    if not os.path.exists(VOTES_FILE):
        return {}
    try:
        with open(VOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _write_votes(votes_dict):
    """Write votes to JSON file (atomic)"""
    tmp_file = VOTES_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(votes_dict, f, indent=2)
    os.replace(tmp_file, VOTES_FILE)

# ========== PAGE ROUTES ==========

@app.route('/')
def home():
    """Homepage - Newspaper style"""
    # Get news articles for homepage
    articles_data = get_articles("home", limit=10)

    # Fallback to mockdata if no articles
    if not articles_data or len(articles_data) == 0:
        articles_data = load_mock('home')

    # Ensure we have at least one article
    if not articles_data or len(articles_data) == 0:
        articles_data = [{"title": "Welcome to TrendWatcher", "description": "Your source for trending news", "image": "", "source": "TrendWatcher"}]

    return render_template(
        'home.html',
        theme='newspaper',
        featured=articles_data[0] if articles_data else {},
        articles=articles_data[1:] if len(articles_data) > 1 else [],
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/crypto')
def crypto():
    """Crypto page - Cyberpunk theme"""
    # Get news articles for main feed
    articles = get_articles("crypto", limit=10)

    # Get crypto coins for sidebar (gainers/losers)
    coins = get_trending_crypto()
    if not coins or len(coins) == 0:
        coins = load_mock('crypto')

    # Calculate gainers, losers, trending from coins data for sidebar
    gainers = sorted(coins, key=lambda x: x.get('change', 0), reverse=True)[:5] if coins else get_demo_gainers()
    losers = sorted(coins, key=lambda x: x.get('change', 0))[:5] if coins else get_demo_losers()
    trending = articles[:5] if articles else []

    return render_template(
        'crypto.html',
        category='crypto',
        theme='cyberpunk',
        articles=articles,  # News articles in main feed
        gainers=gainers,    # Crypto coins in sidebar
        losers=losers,
        trending=trending,
        GA_ID=GA_TRACKING_ID
    )

@app.route('/stocks')
def stocks():
    """Stocks page - Finance theme"""
    # Get news articles for main feed
    articles = get_articles("stocks", limit=10)

    # Get stock data for sidebar (gainers/losers)
    stocks_data = get_trending_stocks()
    if not stocks_data or len(stocks_data) == 0:
        stocks_data = load_mock('stocks')

    # Add affiliate links to stocks
    stocks_data = add_affiliate_to_articles(stocks_data, "stocks")

    # Calculate gainers, losers from stocks data for sidebar
    gainers = sorted(stocks_data, key=lambda x: float(x.get('change', 0)), reverse=True)[:5] if stocks_data else get_demo_gainers()
    losers = sorted(stocks_data, key=lambda x: float(x.get('change', 0)))[:5] if stocks_data else get_demo_losers()
    trending = articles[:5] if articles else []

    return render_template(
        'stocks.html',
        category='stocks',
        theme='finance',
        articles=articles,  # News articles in main feed
        gainers=gainers,    # Stock data in sidebar (with eToro affiliate links)
        losers=losers,
        trending=trending,
        GA_ID=GA_TRACKING_ID
    )

@app.route('/ecommerce')
def ecommerce():
    """E-commerce page - Shop theme"""
    # Get news articles for main feed
    articles = get_articles("ecommerce", limit=10)

    # Add affiliate links to articles
    articles = add_affiliate_to_articles(articles, "ecommerce")

    # Get product data for sidebar
    products = get_trending_ecommerce()
    if not products or len(products) == 0:
        products = load_mock('ecommerce')

    # Add affiliate links to products
    products = add_affiliate_to_articles(products, "ecommerce")

    # Calculate gainers (by growth %)
    gainers = sorted(products, key=lambda x: int(x.get('growth', '0%').replace('%', '').replace('+', '')), reverse=True)[:5] if products else get_demo_gainers()
    losers = get_demo_losers()  # E-commerce doesn't have losers typically
    trending = articles[:5] if articles else []

    return render_template(
        'ecommerce.html',
        category='ecommerce',
        theme='shop',
        articles=articles,  # News articles in main feed (with affiliate links)
        gainers=gainers,    # Product data in sidebar (with affiliate links)
        losers=losers,
        trending=trending,
        GA_ID=GA_TRACKING_ID
    )

@app.route('/entertainment')
def entertainment():
    """Entertainment page - Magazine theme"""
    # Get news articles for main feed
    articles = get_articles("entertainment", limit=10)

    # Get entertainment items for sidebar
    items = get_trending_entertainment()
    if not items or len(items) == 0:
        items = load_mock('entertainment')

    # Prep data for sidebar
    trending_items = sorted(items, key=lambda x: x.get('popularity', 0), reverse=True)[:5] if items else []
    top_rated_items = sorted(items, key=lambda x: x.get('rating', 0), reverse=True)[:5] if items else []
    gainers = trending_items  # Use popularity as "gainers"
    losers = get_demo_losers()

    return render_template(
        'entertainment.html',
        category='entertainment',
        theme='magazine',
        articles=articles,  # News articles in main feed
        gainers=gainers,    # Entertainment items in sidebar
        losers=losers,
        trending=trending_items,
        GA_ID=GA_TRACKING_ID
    )

@app.route('/sports')
def sports():
    """Sports page - Sports theme"""
    # Get news articles for main feed
    articles = get_articles("sports", limit=10)

    # Get sports matches for sidebar
    matches = get_trending_sports()
    if not matches or len(matches) == 0:
        matches = load_mock('sports')

    # Calculate trending and gainers (by popularity)
    trending_matches = sorted(matches, key=lambda x: x.get('popularity', 0), reverse=True)[:5] if matches else []
    gainers = trending_matches  # Use popularity as "gainers"
    losers = get_demo_losers()

    return render_template(
        'sports.html',
        category='sports',
        theme='sports',
        articles=articles,  # News articles in main feed
        gainers=gainers,    # Sports matches in sidebar
        losers=losers,
        trending=trending_matches,
        GA_ID=GA_TRACKING_ID
    )

# ========== API ROUTES (behouden voor backwards compatibility) ==========

@app.route('/crypto/trending')
@app.route('/api/crypto/trending')
def crypto_api():
    """API endpoint voor crypto data"""
    try:
        data = get_trending_crypto()
        if data is None:
            return jsonify({'error': 'Kon geen data ophalen'}), 500
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks/trending')
def stocks_api():
    """API endpoint voor stocks data"""
    try:
        data = get_trending_stocks()
        if data is None:
            return jsonify({'error': 'Kon geen data ophalen'}), 500
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecommerce/trending')
def ecommerce_api():
    """API endpoint voor e-commerce data"""
    try:
        data = get_trending_ecommerce()
        if data is None:
            return jsonify({'error': 'Kon geen data ophalen'}), 500
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entertainment/trending')
def entertainment_api():
    """API endpoint voor entertainment data"""
    try:
        data = get_trending_entertainment()
        if data is None:
            return jsonify({'error': 'Kon geen data ophalen'}), 500
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sports/trending')
def sports_api():
    """API endpoint voor sports data"""
    try:
        data = get_trending_sports()
        if data is None:
            return jsonify({'error': 'Kon geen data ophalen'}), 500
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def api_vote():
    """API endpoint voor upvote/downvote"""
    try:
        payload = request.get_json(force=True)
        category = payload.get('category')
        item_id = payload.get('id')
        direction = payload.get('direction')

        if not (category and item_id and direction in ('up', 'down')):
            return jsonify({'ok': False, 'error': 'bad_request'}), 400

        key = f"{category}:{item_id}"

        with _vote_lock:
            votes = _read_votes()
            votes[key] = votes.get(key, 0) + (1 if direction == 'up' else -1)
            _write_votes(votes)

        return jsonify({'ok': True, 'score': votes[key]})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html', GA_ID=GA_TRACKING_ID), 404

@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html', GA_ID=GA_TRACKING_ID), 500

# ========== NEWSLETTER SUBSCRIPTION ==========

@app.route("/subscribe", methods=["POST"])
def subscribe():
    """Newsletter subscription endpoint"""
    email = request.form.get("email")

    if email and "@" in email:
        # Save to CSV file
        subscribers_file = "data/subscribers.csv"
        os.makedirs("data", exist_ok=True)

        # Append email to CSV
        with _vote_lock:  # Reuse vote lock for thread safety
            file_exists = os.path.exists(subscribers_file)
            with open(subscribers_file, "a", encoding="utf-8") as f:
                if not file_exists:
                    f.write("email,timestamp\n")  # CSV header
                f.write(f"{email},{datetime.now().isoformat()}\n")

        print(f"[NEWSLETTER] New subscriber: {email}")

    # Redirect back to homepage
    return redirect(url_for("home"))

# ========== CLICK TRACKING ==========

@app.route("/track_click", methods=["POST"])
def track_click():
    """Track affiliate and newsletter clicks"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"ok": False, "error": "No data"}), 400

        # Log click to CSV
        clicks_file = "data/clicks.csv"
        os.makedirs("data", exist_ok=True)

        with _vote_lock:
            file_exists = os.path.exists(clicks_file)
            with open(clicks_file, "a", encoding="utf-8") as f:
                if not file_exists:
                    f.write("url,label,timestamp\n")
                f.write(f"{data.get('url', '')},{data.get('label', '')},{data.get('timestamp', '')}\n")

        print(f"[CLICK] {data.get('label', 'Unknown')} -> {data.get('url', 'Unknown')}")
        return jsonify({"ok": True})

    except Exception as e:
        print(f"[CLICK ERROR] {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# ========== LEGAL PAGES ==========

@app.route("/privacy")
def privacy():
    """Privacy policy page"""
    return render_template("legal/privacy.html", GA_ID=GA_TRACKING_ID)

@app.route("/terms")
def terms():
    """Terms of use page"""
    return render_template("legal/terms.html", GA_ID=GA_TRACKING_ID)

@app.route("/cookies")
def cookies_policy():
    """Cookie policy page"""
    return render_template("legal/cookies.html", GA_ID=GA_TRACKING_ID)

# Start development server
if __name__ == '__main__':
    print("TrendWatcher Multi-Theme is gestart!")
    print("Homepage: http://127.0.0.1:5000/")
    print("Crypto (Cyberpunk): http://127.0.0.1:5000/crypto")
    print("Stocks (Finance): http://127.0.0.1:5000/stocks")
    print("E-commerce (Shop): http://127.0.0.1:5000/ecommerce")
    print("Entertainment (Magazine): http://127.0.0.1:5000/entertainment")
    print("Sports (Betting): http://127.0.0.1:5000/sports")
    app.run(debug=True, host='0.0.0.0', port=5000)
