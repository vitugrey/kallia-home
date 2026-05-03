import requests
import xml.etree.ElementTree as ET
import random
from django.core.cache import cache

class NewsFetcherService:
    @staticmethod
    def get_news(category="geral", force_refresh=False):
        """
        Busca as principais manchetes usando o feed RSS do G1.
        Não precisa de chaves de API, e o XML é super leve.
        """
        cache_key = f"news_data_{category}"
        
        if not force_refresh:
            cached_data = cache.get(cache_key)
            if cached_data:
                # Sorteia 3 manchetes a cada requisição para não congelar a tela
                if len(cached_data) >= 3:
                    return random.sample(cached_data, 3)
                return cached_data
            
        try:
            # RSS público de notícias
            url = f"https://g1.globo.com/rss/g1/{category}/"
            if category == "geral":
                url = "https://g1.globo.com/rss/g1/"
                
            response = requests.get(url, timeout=3)
            
            # Navega no XML do RSS
            root = ET.fromstring(response.content)
            
            all_headlines = []
            # Pega as top 15 notícias para ter bastante variação
            for item in root.findall('./channel/item')[:15]:
                title = item.find('title').text
                all_headlines.append(title)
                
            # Salva TODAS as 15 no cache por 3 horas (10800 segundos) para poupar internet
            cache.set(cache_key, all_headlines, 10800)
            
            # Sorteia 3 para a resposta imediata
            if len(all_headlines) >= 3:
                return random.sample(all_headlines, 3)
            return all_headlines
            
        except Exception as e:
            print(f"[NewsFetcherService] Erro ao buscar notícias RSS: {e}")
            return ["Não foi possível carregar as notícias."]
