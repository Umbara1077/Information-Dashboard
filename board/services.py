import time
import requests
from django.conf import settings

def fetch_recent_games(limit=8, days=30):
    """
    Fetch games released within the last `days` days, sorted by release date descending.
    """
    now = int(time.time())
    cutoff = now - days * 24 * 3600  # seconds in `days`

    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {settings.TWITCH_OAUTH_TOKEN}',
    }
    body = f'''
        fields name, cover.url, first_release_date;
        where cover.url != null
          & first_release_date != null
          & first_release_date > {cutoff}
          & first_release_date <= {now};
        sort first_release_date desc;
        limit {limit};
    '''
    resp = requests.post(url, headers=headers, data=body)
    games = resp.json() if resp.ok else []

    for g in games:
        thumb = g.get('cover', {}).get('url', '')
        if thumb:
            # strip leading slashes, swap to the t_720p size, then prefix HTTPS
            cleaned = thumb.lstrip('/')                     # "images.igdb.com/.../t_thumb/coXYZ.jpg"
            cleaned = cleaned.replace('t_thumb', 't_cover_big')  # "images.igdb.com/.../t_720p/coXYZ.jpg"
            g['cover_url'] = f'https://{cleaned}'
        else:
            g['cover_url'] = None

    return games

def fetch_now_playing_movies(limit=8):
    url = 'https://api.themoviedb.org/3/movie/now_playing'
    params = {
        'api_key': settings.TMDB_KEY,
        'language': 'en-US',
        'page': 1,
    }
    data = requests.get(url, params=params).json().get('results', [])
    # attach full poster URLs
    for m in data[:limit]:
        m['poster_url'] = f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
    return data[:limit]

def fetch_upcoming_movies(limit=8):
    url = 'https://api.themoviedb.org/3/movie/upcoming'
    params = {
        'api_key': settings.TMDB_KEY,
        'language': 'en-US',
        'page': 1,
    }
    data = requests.get(url, params=params).json().get('results', [])
    for m in data[:limit]:
        m['poster_url'] = f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
    return data[:limit]

def fetch_now_in_theaters(limit=8):

    return fetch_now_playing_movies(limit)

def fetch_tech_news(limit=6):
    """
    Fetch top technology headlines (US).
    """
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': settings.NEWSAPI_KEY,
        'category': 'technology',
        'country': 'us',
        'pageSize': limit,
    }
    data = requests.get(url, params=params).json().get('articles', [])
    return data

def fetch_general_news(limit=6):
    """
    Fetch top general headlines (US).
    """
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': settings.NEWSAPI_KEY,
        'country': 'us',
        'pageSize': limit,
    }
    data = requests.get(url, params=params).json().get('articles', [])
    return data

def fetch_game_detail(game_id):
    """
    Fetch full details for a single IGDB game.
    """
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {settings.TWITCH_OAUTH_TOKEN}',
    }
    body = f'''
        fields name, summary, cover.url, first_release_date, genres.name, platforms.name;
        where id = {game_id};
    '''
    data = requests.post(url, headers=headers, data=body).json()
    if not data: return {}
    g = data[0]
    thumb = g.get('cover', {}).get('url','').lstrip('/')
    g['cover_url'] = f'https://{thumb.replace("t_thumb","t_cover_big")}'
    return g

def fetch_movie_detail(movie_id):
    """
    Fetch full details for a single TMDB movie.
    """
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {'api_key': settings.TMDB_KEY, 'language': 'en-US'}
    m = requests.get(url, params=params).json()
    m['poster_url'] = f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
    return m

