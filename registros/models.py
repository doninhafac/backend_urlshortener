from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Perfil(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class UsuarioManager(BaseUserManager):
    def create_user(self, name, username, email, password=None, perfil=None):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        if not username:
            raise ValueError('O usuário deve ter um nome de usuário')

        user = self.model(
            name=name,
            username=username,
            email=self.normalize_email(email),
            perfil=perfil  # Define o perfil na criação
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=300)
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, default=3)
    
    firebase_uid = models.CharField(max_length=255, blank=True, null=True)
    firebase_token = models.TextField(blank=True, null=True)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']
    
    def __str__(self):
        return self.name if self.name else self.email
