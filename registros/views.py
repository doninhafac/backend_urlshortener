from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer

class RegistrarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
