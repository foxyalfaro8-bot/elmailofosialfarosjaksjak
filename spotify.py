import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("Falta SPOTIFY_CLIENT_ID o SPOTIFY_CLIENT_SECRET en .env")

creds = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=creds)

def get_track_features(track_id):
    try:
        return sp.audio_features(track_id)[0]
    except Exception as e:
        print(f"Error features: {e}")
        return None

def search_track(query):
    try:
        results = sp.search(q=query, type='track', limit=10)
        return results['tracks']['items']
    except Exception as e:
        print(f"Error search: {e}")
        return []

def get_track(track_id):
    try:
        return sp.track(track_id)
    except Exception as e:
        print(f"Error get_track: {e}")
        return None
