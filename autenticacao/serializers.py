from rest_framework import serializers
from registros.models import Usuario, Perfil

class UsuarioSerializer(serializers.ModelSerializer):
    perfil = serializers.StringRelatedField(source='perfil_id')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'name', 'username', 'email', 'perfil', 'password'] 

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
