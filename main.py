from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db import init_db, get_conn
from spotify import search_track, get_track_features, get_track
from recommender import recommend
from config import PORT, DEBUG

init_db()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(q: str):
    tracks = search_track(q)
    return {"results": tracks}

@app.post("/save")
def save_song(spotify_id: str, title: str, artist: str, rating: int = 5):
    try:
        features = get_track_features(spotify_id)
        if not features:
            return {"error": "No features"}, 400
        
        track = get_track(spotify_id)
        
        conn = get_conn()
        c = conn.cursor()
        
        c.execute('''
            INSERT OR IGNORE INTO songs 
            (spotify_id, title, artist, album, bpm, energy, danceability, loudness, key, genre, year, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            spotify_id,
            title,
            artist,
            track.get('album', {}).get('name') if track else None,
            features.get('tempo'),
            features.get('energy'),
            features.get('danceability'),
            features.get('loudness'),
            features.get('key'),
            None,
            track.get('album', {}).get('release_date', '')[:4] if track else None,
            track.get('external_urls', {}).get('spotify') if track else None
        ))
        
        song_id = c.lastrowid
        
        c.execute('INSERT INTO ratings (song_id, rating) VALUES (?, ?)', (song_id, rating))
        
        conn.commit()
        conn.close()
        
        return {"saved": True, "song_id": song_id}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/recommendations")
def get_recommendations(limit: int = 10):
    try:
        ids = recommend(limit)
        
        if not ids:
            return {"recommendations": []}
        
        conn = get_conn()
        c = conn.cursor()
        
        placeholders = ','.join('?' * len(ids))
        c.execute(f'SELECT id, title, artist, album, spotify_id FROM songs WHERE id IN ({placeholders})', ids)
        
        results = []
        for row in c.fetchall():
            results.append({
                "id": row[0],
                "title": row[1],
                "artist": row[2],
                "album": row[3],
                "spotify_id": row[4]
            })
        
        conn.close()
        return {"recommendations": results}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/library")
def get_library():
    try:
        conn = get_conn()
        c = conn.cursor()
        
        c.execute('''
            SELECT s.id, s.title, s.artist, r.rating
            FROM songs s
            JOIN ratings r ON s.id = r.song_id
            ORDER BY r.timestamp DESC
        ''')
        
        results = []
        for row in c.fetchall():
            results.append({
                "id": row[0],
                "title": row[1],
                "artist": row[2],
                "rating": row[3]
            })
        
        conn.close()
        return {"library": results}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=DEBUG)
