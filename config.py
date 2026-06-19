import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
DEBUG = os.getenv("DEBUG", "True") == "True"
PORT = int(os.getenv("PORT", 8000))

DB_PATH = "data/music.db"
