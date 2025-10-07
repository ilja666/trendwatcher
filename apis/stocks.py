"""
Alpha Vantage API Module
=========================
Deze module handelt alle interacties met de Alpha Vantage API af.
API voor stock market data - trending aandelen en top gainers/losers.
"""

import requests
import os

# Alpha Vantage API endpoints
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def get_trending_stocks(api_key=None):
    """
    Haalt trending stock market data op van Alpha Vantage.
    Gebruikt de TOP_GAINERS_LOSERS functie voor de meest bewegende aandelen.

    Args:
        api_key (str): Alpha Vantage API key (optioneel, gebruikt env var als niet gegeven)

    Returns:
        list: Lijst met trending stocks (symbol, naam, price, change_percentage)
        None: Als de API call mislukt
    """
    # Gebruik API key van parameter of environment variable
    if api_key is None:
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY', 'IIBD0TLOIBKW0AXZ')

    try:
        # Alpha Vantage TOP_GAINERS_LOSERS endpoint
        params = {
            'function': 'TOP_GAINERS_LOSERS',
            'apikey': api_key
        }

        # Doe een GET request naar de Alpha Vantage API
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)

        # Check of de request succesvol was (status code 200)
        response.raise_for_status()

        # Parse de JSON response
        data = response.json()

        # Check voor API error messages
        if 'Error Message' in data or 'Note' in data:
            print(f"Alpha Vantage API Error: {data}")
            return None

        # Verwerk de data - combineer top gainers en top losers
        trending_stocks = []

        # Voeg top 5 gainers toe
        if 'top_gainers' in data:
            for stock in data['top_gainers'][:5]:
                stock_info = {
                    'symbol': stock.get('ticker', 'N/A'),
                    'name': stock.get('ticker', 'N/A'),  # Alpha Vantage geeft geen volledige naam in deze endpoint
                    'price': stock.get('price', '0'),
                    'change_amount': stock.get('change_amount', '0'),
                    'change_percentage': stock.get('change_percentage', '0%'),
                    'volume': stock.get('volume', '0'),
                    'trend_type': 'gainer'  # Markeer als gainer
                }
                trending_stocks.append(stock_info)

        # Voeg top 5 losers toe
        if 'top_losers' in data:
            for stock in data['top_losers'][:5]:
                stock_info = {
                    'symbol': stock.get('ticker', 'N/A'),
                    'name': stock.get('ticker', 'N/A'),
                    'price': stock.get('price', '0'),
                    'change_amount': stock.get('change_amount', '0'),
                    'change_percentage': stock.get('change_percentage', '0%'),
                    'volume': stock.get('volume', '0'),
                    'trend_type': 'loser'  # Markeer als loser
                }
                trending_stocks.append(stock_info)

        return trending_stocks

    except requests.exceptions.RequestException as e:
        # Netwerk fouten, timeouts, etc.
        print(f"API Error: {e}")
        return None

    except Exception as e:
        # Andere onverwachte fouten
        print(f"Unexpected Error: {e}")
        return None


def get_stock_quote(symbol, api_key=None):
    """
    Haalt een realtime quote op voor een specifiek aandeel.

    Args:
        symbol (str): Stock ticker symbol (bijv. 'AAPL', 'MSFT')
        api_key (str): Alpha Vantage API key (optioneel)

    Returns:
        dict: Stock quote data
        None: Als de API call mislukt
    """
    if api_key is None:
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY', 'IIBD0TLOIBKW0AXZ')

    try:
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': api_key
        }

        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            return {
                'symbol': quote.get('01. symbol', symbol),
                'price': quote.get('05. price', '0'),
                'change': quote.get('09. change', '0'),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': quote.get('06. volume', '0')
            }

        return None

    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return None
