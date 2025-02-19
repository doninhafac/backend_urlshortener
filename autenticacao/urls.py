from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "autenticacao"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('google-login/', views.google_login, name='google_login'),
]
