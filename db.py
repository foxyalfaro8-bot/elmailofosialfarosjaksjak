import sqlite3
import os
from config import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT,
            spotify_id TEXT UNIQUE,
            bpm REAL,
            energy REAL,
            danceability REAL,
            loudness REAL,
            key TEXT,
            genre TEXT,
            year INTEGER,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY,
            song_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(song_id) REFERENCES songs(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY,
            source_song_id INTEGER NOT NULL,
            target_song_id INTEGER NOT NULL,
            similarity REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(source_song_id) REFERENCES songs(id),
            FOREIGN KEY(target_song_id) REFERENCES songs(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[DB] Inicializado")

def get_conn():
    return sqlite3.connect(DB_PATH)
