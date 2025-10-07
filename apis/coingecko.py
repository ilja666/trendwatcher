"""
CoinGecko API Module
====================
Deze module handelt alle interacties met de CoinGecko API af.
Gratis API - geen API key nodig!
"""

import requests

# CoinGecko API endpoint voor trending coins
COINGECKO_TRENDING_URL = "https://api.coingecko.com/api/v3/search/trending"

def get_trending_crypto():
    """
    Haalt trending cryptocurrency data op van CoinGecko.

    Returns:
        list: Lijst met trending coins (naam, symbool, market_cap_rank)
        None: Als de API call mislukt
    """
    try:
        # Doe een GET request naar de CoinGecko API
        response = requests.get(COINGECKO_TRENDING_URL, timeout=10)

        # Check of de request succesvol was (status code 200)
        response.raise_for_status()

        # Parse de JSON response
        data = response.json()

        # Verwerk de data en haal alleen relevante velden eruit
        trending_coins = []

        # CoinGecko geeft data terug in 'coins' array
        if 'coins' in data:
            for item in data['coins']:
                coin = item.get('item', {})

                # Extraheer alleen de data die we nodig hebben
                coin_info = {
                    'name': coin.get('name', 'Unknown'),
                    'symbol': coin.get('symbol', 'N/A'),
                    'market_cap_rank': coin.get('market_cap_rank', 'N/A'),
                    'thumb': coin.get('thumb', ''),  # Kleine afbeelding URL
                    'score': item.get('score', 0)  # Trending score
                }

                trending_coins.append(coin_info)

        return trending_coins

    except requests.exceptions.RequestException as e:
        # Netwerk fouten, timeouts, etc.
        print(f"❌ API Error: {e}")
        return None

    except Exception as e:
        # Andere onverwachte fouten
        print(f"❌ Unexpected Error: {e}")
        return None
