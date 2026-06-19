import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from db import get_conn

def get_user_profile():
    conn = get_conn()
    c = conn.cursor()
    
    c.execute('''
        SELECT s.bpm, s.energy, s.danceability, s.loudness
        FROM songs s
        JOIN ratings r ON s.id = r.song_id
        WHERE r.rating >= 4
    ''')
    
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        return None
    
    features = np.array([list(row) for row in rows])
    return np.mean(features, axis=0)

def recommend(limit=10):
    profile = get_user_profile()
    if profile is None:
        return []
    
    conn = get_conn()
    c = conn.cursor()
    
    # Songs con rating
    c.execute('SELECT id FROM ratings')
    rated_ids = set(row[0] for row in c.fetchall())
    
    # Todos los songs
    c.execute('SELECT id, bpm, energy, danceability, loudness FROM songs')
    all_songs = c.fetchall()
    conn.close()
    
    candidates = []
    for song_id, bpm, energy, danceability, loudness in all_songs:
        if song_id not in rated_ids:
            feat = np.array([[bpm or 0, energy or 0, danceability or 0, loudness or 0]])
            sim = cosine_similarity([profile], feat)[0][0]
            candidates.append((song_id, sim))
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [song_id for song_id, _ in candidates[:limit]]
