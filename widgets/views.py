from django.shortcuts import render
from django.http import JsonResponse
from .services.weather_service import WeatherFetcherService
from .services.news_service import NewsFetcherService

def mirror_view(request):
    """
    Renderiza a interface principal (Frontend) do Smart Mirror.
    Essa será a página exibida em tela cheia (fullscreen) no navegador do Raspberry Pi.
    """
    return render(request, 'widgets/mirror.html')

def api_widgets_data(request):
    """
    Endpoint interno chamado pelo Javascript.
    No futuro, leremos o Profile do usuário que está na frente do espelho,
    buscaremos o WidgetPreference dele, e passaremos as variáveis certas.
    """
    # Por enquanto, estamos fixando o Rio de Janeiro para teste estrutural
    lat = -22.9064
    lon = -43.1822
    city = "Rio de Janeiro"
    news_category = "geral" # A categoria 'tecnologia' demora dias para atualizar. 'geral' atualiza a cada minuto!

    # Usa os nossos serviços em Python!
    weather_data = WeatherFetcherService.get_weather(lat, lon)
    news_data = NewsFetcherService.get_news(category=news_category)

    return JsonResponse({
        "weather": {
            "city": city,
            "temperature": weather_data.get("temperature", "--"),
            "description": weather_data.get("description", "Indisponível")
        },
        "news": news_data
    })

