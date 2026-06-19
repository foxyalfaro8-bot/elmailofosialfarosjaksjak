from db import get_conn
from scraper import get_recommendations_from_chosic
from spotify import search_track

def get_chosic_recommendations(artist, track, limit=10):
    """
    Obtiene recomendaciones desde Chosic scrapeado
    Busca en Spotify y guarda localmente
    """
    try:
        # Scrapea Chosic
        chosic_results = get_recommendations_from_chosic(artist, track)
        
        if not chosic_results:
            return []
        
        recommendations = []
        conn = get_conn()
        c = conn.cursor()
        
        for title, rec_artist in chosic_results[:limit]:
            try:
                # Busca en Spotify
                tracks = search_track(f"{rec_artist} {title}")
                
                if tracks:
                    track_data = tracks[0]
                    spotify_id = track_data['id']
                    
                    # Guarda en DB si no existe
                    c.execute('''
                        INSERT OR IGNORE INTO songs
                        (spotify_id, title, artist, album, url)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        spotify_id,
                        track_data['name'],
                        track_data['artists'][0]['name'],
                        track_data.get('album', {}).get('name'),
                        track_data['external_urls']['spotify']
                    ))
                    
                    recommendations.append({
                        'title': track_data['name'],
                        'artist': track_data['artists'][0]['name'],
                        'spotify_id': spotify_id,
                        'url': track_data['external_urls']['spotify'],
                        'album': track_data.get('album', {}).get('name')
                    })
            except Exception as e:
                print(f"Error procesando recomendacion: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return recommendations
    
    except Exception as e:
        print(f"Error en get_chosic_recommendations: {e}")
        return []

def recommend(artist=None, track=None, limit=10):
    """
    API principal de recomendaciones
    Ahora usa Chosic como fuente
    """
    if not artist or not track:
        return []
    
    return get_chosic_recommendations(artist, track, limit)
