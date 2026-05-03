from django.urls import path
from . import views

urlpatterns = [
    # A rota raiz (vazia) vai exibir a interface do espelho
    path('', views.mirror_view, name='mirror_home'),
    
    # --- APIs de Dados ---
    path('api/data/', views.api_widgets_data, name='api_widgets_data'),
    
    # --- APIs de Estado do Cérebro (Reconhecimento) ---
    path('api/status/', views.api_mirror_status, name='api_mirror_status'),
    path('api/debug/set_state/', views.api_debug_set_state, name='api_debug_set_state'),
]
