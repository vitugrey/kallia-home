from django.urls import path
from . import views

urlpatterns = [
    # A rota raiz (vazia) vai exibir a interface do espelho
    path('', views.mirror_view, name='mirror_home'),
]
