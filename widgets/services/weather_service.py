import requests
from django.core.cache import cache

class WeatherFetcherService:
    @staticmethod
    def get_weather(lat, lon):
        """
        Busca o clima atual baseado nas coordenadas.
        Utiliza o cache do Django para não estourar os limites da API e deixar a tela rápida.
        """
        # Cria uma chave única no cache para essa localização específica
        cache_key = f"weather_data_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            # API do Open-Meteo (Gratuita e sem necessidade de cadastro)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url, timeout=3)
            data = response.json()
            
            weather_code = data["current_weather"]["weathercode"]
            
            # Tradutor simples do código WMO da API para português
            desc = "Céu Limpo"
            if 1 <= weather_code <= 3: desc = "Parcialmente Nublado"
            elif 45 <= weather_code <= 48: desc = "Neblina"
            elif 51 <= weather_code <= 67: desc = "Chuva Leve"
            elif 71 <= weather_code <= 77: desc = "Neve"
            elif 80 <= weather_code <= 82: desc = "Pancadas de Chuva"
            elif weather_code >= 95: desc = "Tempestade"

            resultado = {
                "temperature": round(data["current_weather"]["temperature"]),
                "description": desc
            }
            
            # Salva no cache por 1 hora (3600 segundos)
            cache.set(cache_key, resultado, 3600)
            return resultado
            
        except Exception as e:
            print(f"[WeatherFetcherService] Erro de conexão com a API de clima: {e}")
            return {"temperature": "--", "description": "Offline"}
