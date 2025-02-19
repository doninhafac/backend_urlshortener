from django.urls import path
from .views import (
    premium_edit_links, 
    redirect_to_original, 
    shorten_url, 
    track_click, 
    link_stats,
    list_user_links  # Certifique-se de importar aqui
)

urlpatterns = [
    path('shorten/', shorten_url, name='shorten_url'),
    path('<str:short_code>/', redirect_to_original, name='redirect_to_original'),
    path('premium/edit/', premium_edit_links, name='premium_edit_links'),
    path('track_click/<str:short_code>/', track_click, name='track_click'),
    path('stats/<str:short_code>/', link_stats, name='link_stats'),
    path('list/', list_user_links, name='list_user_links'),
]
