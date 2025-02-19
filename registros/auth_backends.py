from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None):
        User = get_user_model()

        print(f"Tentando autenticar: username={username}, email={email}")  # Debug

        if email:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    print("Usuário autenticado com email")
                    return user
            except User.DoesNotExist:
                print("Usuário com este email não encontrado")

        if username:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    print("Usuário autenticado com username")
                    return user
            except User.DoesNotExist:
                print("Usuário com este username não encontrado")

        return None