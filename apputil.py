import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class Genius:
    
    def __init__(self, access_token=None):
        if access_token is None:
            access_token = os.environ.get('ACCESS_TOKEN')
        
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
    
    def _search(self, search_term):
        search_url = f"{self.base_url}/search?q={search_term}&access_token={self.access_token}"
        response = requests.get(search_url)
        return response.json()
    
    def _get_artist_by_id(self, artist_id):
        artist_url = f"{self.base_url}/artists/{artist_id}?access_token={self.access_token}"
        response = requests.get(artist_url)
        return response.json()
    
    def get_artist(self, search_term):
        try:
            search_results = self._search(search_term)
            hits = search_results['response']['hits']
            
            if not hits:
                return None
            
            first_hit = hits[0]
            artist_id = first_hit['result']['primary_artist']['id']
            artist_data = self._get_artist_by_id(artist_id)
            
            return artist_data['response']['artist']
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_artists(self, search_terms):
        results = []
        
        for term in search_terms:
            artist = self.get_artist(term)
            
            if artist:
                results.append({
                    'search_term': term,
                    'artist_name': artist.get('name'),
                    'artist_id': artist.get('id'),
                    'followers_count': artist.get('followers_count')
                })
            else:
                results.append({
                    'search_term': term,
                    'artist_name': None,
                    'artist_id': None,
                    'followers_count': None
                })
        
        return pd.DataFrame(results)