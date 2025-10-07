"""
TrendWatcher - Multi-Theme Flask Webapp
========================================
Multi-market trending data met per-category themes.
"""

from flask import Flask, render_template, jsonify, request
from apis.coingecko import get_trending_crypto
from apis.stocks import get_trending_stocks
from apis.ecommerce import get_trending_ecommerce
from apis.entertainment import get_trending_entertainment
from apis.sports import get_trending_sports
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
    articles = get_demo_articles()
    return render_template(
        'home.html',
        theme='newspaper',
        featured=articles[0],
        articles=articles[1:],
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/crypto')
def crypto():
    """Crypto page - Cyberpunk theme"""
    coins = get_trending_crypto()
    if not coins:
        coins = [{"name": "Demo Mode", "symbol": "N/A", "market_cap_rank": "N/A", "score": 0, "thumb": ""}]
    return render_template(
        'crypto_page.html',
        theme='cyberpunk',
        coins=coins,
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/stocks')
def stocks():
    """Stocks page - Finance theme"""
    stocks_data = get_trending_stocks()
    if not stocks_data:
        stocks_data = [{"symbol": "Demo", "price": "0", "change_percentage": "0%", "volume": "0", "trend_type": "gainer"}]
    return render_template(
        'stocks_page.html',
        theme='finance',
        stocks=stocks_data,
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/ecommerce')
def ecommerce():
    """E-commerce page - Shop theme"""
    products = get_trending_ecommerce()
    if not products:
        products = [{"keyword": "Demo Product", "value": 0, "category": "Demo"}]
    return render_template(
        'ecommerce_page.html',
        theme='shop',
        products=products,
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/entertainment')
def entertainment():
    """Entertainment page - Magazine theme"""
    items = get_trending_entertainment()
    if not items:
        items = [{"title": "Demo Content", "type": "Demo", "platform": "Demo", "rating": 0, "popularity": 0}]

    # Prep data for sidebar
    trending_items = items[:5]  # First 5 items
    top_rated_items = sorted(items, key=lambda x: x.get('rating', 0), reverse=True)[:5]

    return render_template(
        'entertainment_page.html',
        theme='magazine',
        items=items,
        trending_items=trending_items,
        top_rated_items=top_rated_items,
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
        GA_ID=GA_TRACKING_ID
    )

@app.route('/sports')
def sports():
    """Sports page - Sports theme"""
    matches = get_trending_sports()
    if not matches:
        matches = [{"title": "Demo Match", "league": "Demo", "status": "Live", "engagement": "0"}]
    return render_template(
        'sports_page.html',
        theme='sports',
        matches=matches,
        gainers=get_demo_gainers(),
        losers=get_demo_losers(),
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
