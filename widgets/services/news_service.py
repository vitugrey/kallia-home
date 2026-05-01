import requests
import xml.etree.ElementTree as ET
from django.core.cache import cache

class NewsFetcherService:
    @staticmethod
    def get_news(category="geral"):
        """
        Busca as principais manchetes usando o feed RSS do G1.
        Não precisa de chaves de API, e o XML é super leve.
        """
        cache_key = f"news_data_{category}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            # RSS público de notícias
            url = f"https://g1.globo.com/rss/g1/{category}/"
            if category == "geral":
                url = "https://g1.globo.com/rss/g1/"
                
            response = requests.get(url, timeout=3)
            
            # Navega no XML do RSS
            root = ET.fromstring(response.content)
            
            headlines = []
            # O padrão RSS tem os itens dentro de channel -> item
            # Pegamos apenas as 3 últimas notícias
            for item in root.findall('./channel/item')[:3]:
                title = item.find('title').text
                headlines.append(title)
                
            # Salva no cache por 3 horas (10800 segundos) para poupar internet
            cache.set(cache_key, headlines, 10800)
            return headlines
            
        except Exception as e:
            print(f"[NewsFetcherService] Erro ao buscar notícias RSS: {e}")
            return ["Não foi possível carregar as notícias."]
