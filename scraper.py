import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def scrape_chosic_similar(artist, track):
    """
    Scrapea Chosic para canciones similares
    Retorna lista de (titulo, artista, url)
    """
    try:
        query = f"{artist} {track}"
        url = f"https://www.chosic.com/spotify/spotify-playlist-generator/?artist_name={quote(artist)}&track_name={quote(track)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        results = []
        
        # Buscar en tabla de resultados
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows[:15]:  # Top 15
                cols = row.find_all('td')
                if len(cols) >= 2:
                    title = cols[0].text.strip()
                    artist_name = cols[1].text.strip()
                    results.append((title, artist_name))
        
        return results
    except Exception as e:
        print(f"Error scraping Chosic: {e}")
        return []

def scrape_chosic_playlist_analyzer(playlist_id):
    """
    Scrapea análisis de playlist desde Chosic
    Retorna metadata de género, mood, etc
    """
    try:
        url = f"https://www.chosic.com/spotify/playlist-analyzer/?id={playlist_id}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        data = {}
        
        # Info general
        info = soup.find('div', {'class': 'playlist-info'})
        if info:
            data['info'] = info.text.strip()
        
        return data
    except Exception as e:
        print(f"Error analyzing playlist: {e}")
        return {}

def get_recommendations_from_chosic(artist, track):
    """
    Wrapper principal para obtener recomendaciones
    """
    return scrape_chosic_similar(artist, track)
