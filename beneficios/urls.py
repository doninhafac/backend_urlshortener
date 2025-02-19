from django.urls import path
from .views import tornar_premium

urlpatterns = [
    path('upgrade/', tornar_premium, name='tornar_premium'),
]
