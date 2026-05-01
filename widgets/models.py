from django.db import models
from users.models import Profile

class WidgetPreference(models.Model):
    # Um perfil tem apenas UMA configuração de widgets
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="widget_preference")
    
    # --- Configurações do Widget de Clima ---
    weather_city = models.CharField(max_length=100, default="Rio de Janeiro")
    weather_lat = models.FloatField(default=-22.9064)
    weather_lon = models.FloatField(default=-43.1822)
    
    # --- Configurações do Widget de Notícias ---
    # Categorias possíveis no RSS do G1: geral, tecnologia, economia, ciencia-e-saude
    news_category = models.CharField(max_length=50, default="geral")
    
    def __str__(self):
        return f"Preferências Visuais de {self.profile.name}"
