from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'name', 'username', 'email', 'password', 'perfil']

    def create(self, validated_data):
        perfil = validated_data.pop('perfil', None)
        # A criação do usuário já irá associar o perfil corretamente
        user = Usuario.objects.create_user(**validated_data, perfil=perfil)
        return user