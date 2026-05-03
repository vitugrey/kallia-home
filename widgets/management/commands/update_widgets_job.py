import time
from django.core.management.base import BaseCommand
from widgets.models import WidgetPreference
from widgets.services.weather_service import WeatherFetcherService
from widgets.services.news_service import NewsFetcherService

class Command(BaseCommand):
    help = 'Roda em background atualizando o cache de clima e notícias proativamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando Job de Atualização de Widgets (Crtl+C para parar)..."))
        
        while True:
            self.stdout.write("\n[Job] Analisando perfis para atualizar dados...")
            preferences = WidgetPreference.objects.all()
            
            # Se não tiver perfis cadastrados, atualiza um cache padrão
            if not preferences:
                self.stdout.write(" -> Nenhum perfil encontrado. Atualizando cache padrão do Rio de Janeiro.")
                WeatherFetcherService.get_weather(-22.9064, -43.1822, force_refresh=True)
                NewsFetcherService.get_news("geral", force_refresh=True)
            else:
                for pref in preferences:
                    self.stdout.write(f" -> Renova cache para: {pref.profile.name}")
                    WeatherFetcherService.get_weather(pref.weather_lat, pref.weather_lon, force_refresh=True)
                    NewsFetcherService.get_news(pref.news_category, force_refresh=True)
            
            self.stdout.write(self.style.SUCCESS("[Job] Atualização concluída. Dormindo por 1 hora..."))
            
            # Dorme por 3600 segundos (1 hora)
            # Dessa forma a API do Open-Meteo não é bloqueada por uso excessivo
            time.sleep(3600)
