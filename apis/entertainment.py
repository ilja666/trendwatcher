"""
Entertainment Trends API Module
================================
Deze module handelt trending entertainment data af.
Bronnen: IMDb, YouTube, Spotify, Netflix trending content.
"""

import requests
import os

# YouTube API config
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', None)
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"

def get_trending_entertainment():
    """
    Haalt trending entertainment data op.

    Gebruikt YouTube API als key beschikbaar, anders demo data.

    Returns:
        list: Lijst met trending entertainment items
        None: Als de data ophalen mislukt
    """
    # Probeer eerst YouTube API (als key beschikbaar)
    if YOUTUBE_API_KEY:
        youtube_data = get_youtube_trending()
        if youtube_data:
            return youtube_data

    # Fallback naar demo data
    try:
        # MVP: Trending entertainment (statisch voor demo)
        # In productie: vervang met YouTube API, TMDb, etc.
        trending_items = [
            {
                'title': 'Dune: Part Three',
                'type': 'Movie',
                'category': 'Sci-Fi',
                'popularity': 98,
                'platform': 'Cinema',
                'rating': 8.9
            },
            {
                'title': 'The Last of Us S2',
                'type': 'TV Series',
                'category': 'Drama/Action',
                'popularity': 95,
                'platform': 'HBO Max',
                'rating': 9.2
            },
            {
                'title': 'GTA VI Trailer',
                'type': 'Gaming',
                'category': 'Action/Adventure',
                'popularity': 92,
                'platform': 'YouTube',
                'rating': 9.8
            },
            {
                'title': 'Taylor Swift Concert Film',
                'type': 'Music/Concert',
                'category': 'Pop',
                'popularity': 89,
                'platform': 'Disney+',
                'rating': 8.7
            },
            {
                'title': 'Oppenheimer Director\'s Cut',
                'type': 'Movie',
                'category': 'Biography/Drama',
                'popularity': 86,
                'platform': 'Peacock',
                'rating': 9.1
            },
            {
                'title': 'One Piece Live Action S2',
                'type': 'TV Series',
                'category': 'Adventure/Fantasy',
                'popularity': 84,
                'platform': 'Netflix',
                'rating': 8.5
            },
            {
                'title': 'AI Music Generator',
                'type': 'Tech/Music',
                'category': 'Innovation',
                'popularity': 81,
                'platform': 'Spotify',
                'rating': 7.8
            },
            {
                'title': 'Marvel Phase 6 Announcement',
                'type': 'Movie News',
                'category': 'Superhero',
                'popularity': 78,
                'platform': 'YouTube',
                'rating': 8.3
            },
            {
                'title': 'Stranger Things Finale',
                'type': 'TV Series',
                'category': 'Horror/Sci-Fi',
                'popularity': 75,
                'platform': 'Netflix',
                'rating': 8.9
            },
            {
                'title': 'Kendrick Lamar New Album',
                'type': 'Music',
                'category': 'Hip-Hop',
                'popularity': 72,
                'platform': 'Spotify',
                'rating': 9.3
            }
        ]

        return trending_items

    except Exception as e:
        print(f"Entertainment Error: {e}")
        return None


def get_youtube_trending():
    """
    Haalt trending videos op van YouTube Data API.
    Gratis API met 10,000 requests/dag quota.
    """
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == 'YOUR_YOUTUBE_API_KEY':
        return None

    try:
        params = {
            'part': 'snippet,statistics',
            'chart': 'mostPopular',
            'regionCode': 'US',
            'maxResults': 10,
            'videoCategoryId': '0',  # All categories
            'key': YOUTUBE_API_KEY
        }

        response = requests.get(YOUTUBE_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        trending_items = []

        if 'items' in data:
            for video in data['items']:
                snippet = video.get('snippet', {})
                stats = video.get('statistics', {})

                # Converteer views naar popularity score (0-100)
                views = int(stats.get('viewCount', 0))
                popularity = min(100, int((views / 1000000) * 10))  # 10M views = 100

                trending_items.append({
                    'title': snippet.get('title', 'Unknown'),
                    'type': 'YouTube Video',
                    'category': snippet.get('categoryId', 'General'),
                    'popularity': popularity,
                    'platform': 'YouTube',
                    'rating': min(10, int(stats.get('likeCount', 0)) / max(1, int(stats.get('viewCount', 1))) * 1000)
                })

        return trending_items

    except Exception as e:
        print(f"YouTube API Error: {e}")
        return None


def get_tmdb_trending():
    """
    FUTURE: Implementatie met TMDb (The Movie Database) API.
    Gratis API voor trending movies & TV shows.
    """
    pass


def get_spotify_trending():
    """
    FUTURE: Implementatie met Spotify Web API.
    Trending tracks, artists, playlists.
    """
    pass
