from django.urls import path
from .views import recuperar_senha, resetar_senha

urlpatterns = [
    path("forgot-password/", recuperar_senha, name="forgot-password"),
    path("reset-password/<str:token>/", resetar_senha, name="reset-password"),
]
