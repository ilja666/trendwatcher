"""
Sports Trends API Module
=========================
Deze module handelt trending sports data af.
Bronnen: TheSportsDB (live events), ESPN, Reddit sports communities.
"""

import requests
from datetime import datetime, timedelta

# TheSportsDB API endpoint (gratis, geen key nodig voor basis calls)
THESPORTSDB_BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"

def get_trending_sports():
    """
    Haalt trending sports events en nieuws op.

    Probeert eerst live data van TheSportsDB API, fallback naar demo data.

    Returns:
        list: Lijst met trending sports items
        None: Als de data ophalen mislukt
    """
    # Return None to force fallback to mockdata with images
    return None

    # Probeer eerst TheSportsDB API
    live_data = get_thesportsdb_trending()
    if live_data and len(live_data) > 0:
        return live_data

    # Fallback naar demo data als API niet werkt
    try:
        # MVP: Trending sports (statisch voor demo)
        # In productie: vervang met ESPN API, TheSportsDB, etc.
        trending_items = [
            {
                'title': 'Champions League Final',
                'sport': 'Football',
                'league': 'UEFA Champions League',
                'popularity': 98,
                'status': 'Upcoming',
                'engagement': '2.4M mentions'
            },
            {
                'title': 'NBA Finals Game 7',
                'sport': 'Basketball',
                'league': 'NBA',
                'popularity': 95,
                'status': 'Live',
                'engagement': '1.8M mentions'
            },
            {
                'title': 'F1 Monaco Grand Prix',
                'sport': 'Formula 1',
                'league': 'FIA F1',
                'popularity': 92,
                'status': 'Live',
                'engagement': '1.5M mentions'
            },
            {
                'title': 'Wimbledon Finals',
                'sport': 'Tennis',
                'league': 'ATP/WTA',
                'popularity': 88,
                'status': 'Upcoming',
                'engagement': '987K mentions'
            },
            {
                'title': 'Super Bowl LVIII',
                'sport': 'American Football',
                'league': 'NFL',
                'popularity': 86,
                'status': 'Highlights',
                'engagement': '3.2M mentions'
            },
            {
                'title': 'World Cup Qualifiers',
                'sport': 'Football',
                'league': 'FIFA',
                'popularity': 84,
                'status': 'Live',
                'engagement': '1.2M mentions'
            },
            {
                'title': 'UFC Title Fight',
                'sport': 'MMA',
                'league': 'UFC',
                'popularity': 81,
                'status': 'Upcoming',
                'engagement': '845K mentions'
            },
            {
                'title': 'Tour de France',
                'sport': 'Cycling',
                'league': 'UCI',
                'popularity': 78,
                'status': 'Live',
                'engagement': '654K mentions'
            },
            {
                'title': 'Premier League Derby',
                'sport': 'Football',
                'league': 'EPL',
                'popularity': 75,
                'status': 'Live',
                'engagement': '1.1M mentions'
            },
            {
                'title': 'Olympics 2024 Highlights',
                'sport': 'Multi-Sport',
                'league': 'IOC',
                'popularity': 72,
                'status': 'Highlights',
                'engagement': '2.8M mentions'
            }
        ]

        return trending_items

    except Exception as e:
        print(f"Sports Error: {e}")
        return None


def get_espn_trending():
    """
    FUTURE: Implementatie met ESPN API.
    Real-time scores, trending news, live events.
    """
    pass


def get_thesportsdb_trending():
    """
    Haalt live sports events op van TheSportsDB API.
    Gratis API voor league data, live scores, upcoming matches.

    Returns:
        list: Lijst met trending sports events
        None: Als de API call mislukt
    """
    try:
        trending_items = []

        # Populaire leagues om te checken (Belgische Jupiler Pro League eerst!)
        popular_leagues = [
            ('4330', 'Belgian Jupiler Pro League', 'Football'),
            ('4424', 'UEFA Champions League', 'Football'),
            ('4328', 'English Premier League', 'Football'),
            ('4331', 'Spanish La Liga', 'Football'),
            ('4332', 'Italian Serie A', 'Football'),
            ('4387', 'NBA', 'Basketball'),
        ]

        # Haal volgende events op voor elke league
        for league_id, league_name, sport in popular_leagues[:3]:  # Eerste 3 om API calls te beperken
            try:
                url = f"{THESPORTSDB_BASE_URL}/eventsnextleague.php?id={league_id}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data and 'events' in data and data['events']:
                    # Neem eerste upcoming event
                    for event in data['events'][:2]:  # Max 2 per league
                        if event:
                            trending_items.append({
                                'title': f"{event.get('strHomeTeam', 'TBD')} vs {event.get('strAwayTeam', 'TBD')}",
                                'sport': sport,
                                'league': league_name,
                                'popularity': 85 + len(trending_items) * 2,  # Mock popularity score
                                'status': event.get('strStatus', 'Upcoming'),
                                'engagement': f"{(100 - len(trending_items) * 10)}K mentions"  # Mock engagement
                            })

            except Exception as e:
                # Skip deze league bij fout, ga door met volgende
                print(f"Error fetching league {league_id}: {e}")
                continue

        return trending_items if len(trending_items) > 0 else None

    except Exception as e:
        print(f"TheSportsDB Error: {e}")
        return None


def get_reddit_sports_trending():
    """
    FUTURE: Implementatie met Reddit API.
    Trending posts from sports subreddits.
    """
    pass
