from django.urls import path, include

urlpatterns = [
    path('', include('links.urls')),
    path('registros/', include('registros.urls')),
    path('autenticacao/', include('autenticacao.urls')),
    path('forgotpassword/', include('forgotpassword.urls')),
    path('beneficios/', include('beneficios.urls')),
]
