from django.urls import path
from . import views

app_name = "registros"

urlpatterns = [
    path('register/', views.RegistrarUsuarioView.as_view(), name='register'),
]
