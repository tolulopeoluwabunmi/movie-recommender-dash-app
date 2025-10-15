import requests
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
movie_db_api_key = 'c4c9fd3840bd511c97f3f17fa0f4999d'

# Function to fetch a movie poster by TMDB ID
def fetch_poster_url(tmdb_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{int(tmdb_id)}?api_key={movie_db_api_key}'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        print("fetch_poster_url error:", e)
    return "https://via.placeholder.com/300x450?text=No+Image"

# Function to render a list of movie cards using Bootstrap
def render_movie_cards(filtered_df):
    cards = []
    for _, row in filtered_df.iterrows():
        if pd.isna(row.get('tmdbId')):
            continue
        poster_url = fetch_poster_url(row.get('tmdbId'))
        link = f"/movie/tmdb/{int(row['tmdbId'])}"
        cards.append(
            dbc.Card([
                dcc.Link([
                    dbc.CardImg(src=poster_url, top=True),
                    dbc.CardBody([
                        html.H5(f"{row['title']} ({row.get('year', 'N/A')})", className='card-title'),
                        html.P(f"⭐ Rating: {row.get('rating', 'N/A')}", className='card-text'),
                        html.P(f"🎭 Genres: {row.get('genres', 'N/A')}", className='card-text text-muted')
                    ])
                ], href=link, style={"textDecoration": "none", "color": "inherit"})
            ], className='m-2', style={
                'width': '18rem',
                'background': 'linear-gradient(to top right, #ffffff, #e3f2fd)',
                'border': '2px solid #007bff',
                'borderRadius': '15px',
                'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
            })
        )
    return dbc.Row(cards, className='d-flex flex-wrap justify-content-center')

# Function to fetch full movie details from TMDB API
def fetch_movie_details(tmdb_id):
    try:
        if tmdb_id is None:
            raise ValueError("tmdb_id is missing or None")

        tmdb_id = int(tmdb_id)

        base_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={movie_db_api_key}"
        response = requests.get(base_url)
        data = response.json() if response.status_code == 200 else {}
        # Fetches movie trailer (YouTube)
        trailer_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={movie_db_api_key}"
        trailer_response = requests.get(trailer_url)
        trailer_id = None
        if trailer_response.status_code == 200:
            videos = trailer_response.json().get("results", [])
            for vid in videos:
                if vid.get("type") == "Trailer" and vid.get("site") == "YouTube":
                    trailer_id = vid.get("key")
                    break
        # Fetches cast details (Top 5 actors)
        cast_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={movie_db_api_key}"
        cast_response = requests.get(cast_url)
        cast_names, cast_imgs = [], []
        if cast_response.status_code == 200:
            cast_data = cast_response.json().get("cast", [])
            for c in cast_data[:5]:
                cast_names.append(c["name"])
                cast_imgs.append(f"https://image.tmdb.org/t/p/w185{c['profile_path']}" if c.get("profile_path") else None)

        poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else "https://via.placeholder.com/300x450?text=No+Image"
        genres = ", ".join([genre["name"] for genre in data.get("genres", [])])
        companies = ", ".join([c["name"] for c in data.get("production_companies", [])])
        languages = ", ".join([lang["english_name"] for lang in data.get("spoken_languages", [])])
        # Returns a dictionary of movie details
        return {
            "title": data.get("title"),
            "release_date": data.get("release_date"),
            "overview": data.get("overview"),
            "runtime": data.get("runtime"),
            "genres": genres,
            "poster": poster,
            "rating": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "homepage": data.get("homepage"),
            "companies": companies,
            "languages": languages,
            "trailer": trailer_id,
            "cast_names": cast_names,
            "cast_imgs": cast_imgs
        }

    except Exception as e:
        print("fetch_movie_details error:", e)
    return None

# Function to fetch an actor's biography and profile picture
def fetch_actor_bio_and_photo(actor_name):
    try:
        search_url = f"https://api.themoviedb.org/3/search/person?api_key={movie_db_api_key}&query={actor_name}"
        search_resp = requests.get(search_url).json()
        if not search_resp['results']:
            return None, None
        person_id = search_resp['results'][0]['id']
        details_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={movie_db_api_key}"
        details_resp = requests.get(details_url).json()
        bio = details_resp.get('biography')
        profile_path = details_resp.get('profile_path')
        profile_url = f"https://image.tmdb.org/t/p/w300{profile_path}" if profile_path else "https://via.placeholder.com/300x450?text=No+Photo"
        return bio, profile_url
    except Exception as e:
        print("fetch_actor_bio_and_photo error:", e)
        return None, None

# Function to fetch movies that an actor has appeared in
def fetch_actor_movies(actor_name):
    try:
        search_url = f"https://api.themoviedb.org/3/search/person?api_key={movie_db_api_key}&query={actor_name}"
        search_resp = requests.get(search_url).json()
        if not search_resp['results']:
            return []
        person_id = search_resp['results'][0]['id']
        credits_url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={movie_db_api_key}"
        credits_resp = requests.get(credits_url).json()
        return credits_resp.get('cast', [])
    except Exception as e:
        print("fetch_actor_movies error:", e)
        return []