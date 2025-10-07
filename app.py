"""
TrendWatcher - Flask Webapp voor Crypto Trending Data
======================================================
Dit is de hoofd-applicatie die de Flask server runt.
"""

from flask import Flask, jsonify, render_template
from apis.coingecko import get_trending_crypto
from apis.stocks import get_trending_stocks
from apis.ecommerce import get_trending_ecommerce

# Flask app initialiseren
app = Flask(__name__)

# Route: Homepage met dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    """
    Toont de dashboard pagina met trending crypto coins.
    Rendert de index.html template.
    """
    return render_template('index.html')

# Route: API endpoint voor trending crypto data
@app.route('/crypto/trending')
def crypto_trending():
    """
    Haalt trending crypto data op van CoinGecko API.
    Returns:
        JSON response met trending coins (naam, symbool, market_cap_rank)
    """
    try:
        # Haal trending data op via de CoinGecko module
        trending_data = get_trending_crypto()

        # Check of we data hebben ontvangen
        if trending_data is None:
            return jsonify({
                'error': 'Kon geen data ophalen van CoinGecko API'
            }), 500

        # Succesvol - stuur data terug
        return jsonify({
            'success': True,
            'data': trending_data
        })

    except Exception as e:
        # Error handling voor onverwachte fouten
        return jsonify({
            'error': f'Er ging iets mis: {str(e)}'
        }), 500

# Route: API endpoint voor trending stocks data
@app.route('/api/stocks/trending')
def stocks_trending():
    """
    Haalt trending stock market data op van Alpha Vantage API.
    Returns:
        JSON response met trending stocks (top gainers en losers)
    """
    try:
        # Haal trending stocks data op via de Alpha Vantage module
        trending_data = get_trending_stocks()

        # Check of we data hebben ontvangen
        if trending_data is None:
            return jsonify({
                'error': 'Kon geen data ophalen van Alpha Vantage API'
            }), 500

        # Succesvol - stuur data terug
        return jsonify({
            'success': True,
            'data': trending_data
        })

    except Exception as e:
        # Error handling voor onverwachte fouten
        return jsonify({
            'error': f'Er ging iets mis: {str(e)}'
        }), 500

# Route: API endpoint voor trending e-commerce data
@app.route('/api/ecommerce/trending')
def ecommerce_trending():
    """
    Haalt trending e-commerce/shopping data op.
    Returns:
        JSON response met trending products en keywords
    """
    try:
        # Haal trending e-commerce data op
        trending_data = get_trending_ecommerce()

        # Check of we data hebben ontvangen
        if trending_data is None:
            return jsonify({
                'error': 'Kon geen e-commerce data ophalen'
            }), 500

        # Succesvol - stuur data terug
        return jsonify({
            'success': True,
            'data': trending_data
        })

    except Exception as e:
        # Error handling voor onverwachte fouten
        return jsonify({
            'error': f'Er ging iets mis: {str(e)}'
        }), 500

# Start de Flask development server
if __name__ == '__main__':
    print("🚀 TrendWatcher is gestart!")
    print("📊 Dashboard: http://127.0.0.1:5000/dashboard")
    print("🔗 API endpoints:")
    print("   - Crypto: http://127.0.0.1:5000/crypto/trending")
    print("   - Stocks: http://127.0.0.1:5000/api/stocks/trending")
    print("   - E-commerce: http://127.0.0.1:5000/api/ecommerce/trending")
    app.run(debug=True, host='0.0.0.0', port=5000)
