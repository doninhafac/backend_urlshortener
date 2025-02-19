from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from registros.models import Perfil

class Command(BaseCommand):
    help = 'Inicializa o sistema com dados padrão'
    
    def handle(self, *args, **kwargs):
        # Cria os perfis de usuário
        perfis = {
            1: 'Administrador',
            2: 'Premium',
            3: 'Comum'  # Garantir que o ID 3 corresponde ao perfil Comum
        }

        perfil_objs = {}
        for id_perfil, nome in perfis.items():
            perfil, created = Perfil.objects.get_or_create(nome=nome)
            perfil_objs[nome] = perfil
            if created:
                self.stdout.write(self.style.SUCCESS(f'Perfil criado: {nome}'))

        # Cria usuários padrão
        User = get_user_model()
        usuarios = [
            {'name': 'Andressa', 'username': 'andressa', 'email': 'andressacaroline082011@gmail.com', 'password': '123', 'perfil': 'Administrador', 'is_superuser': True, 'is_staff': True},
            {'name': 'Teste', 'username': 'teste', 'email': 'teste@teste.com', 'password': '123', 'perfil': 'Premium', 'is_superuser': False, 'is_staff': False},
            {'name': 'Teste1', 'username': 'teste1', 'email': 'teste@gmail.com', 'password': '123', 'perfil': 'Comum', 'is_superuser': False, 'is_staff': False},
        ]

        for user_data in usuarios:
            if not User.objects.filter(email=user_data['email']).exists():
                perfil = perfil_objs.get(user_data['perfil'])
                
                # Se o perfil não existir (em caso de erro de digitação no nome), um erro será levantado
                if perfil is None:
                    self.stdout.write(self.style.ERROR(f'Erro: Perfil {user_data["perfil"]} não encontrado!'))
                    continue
                
                # Criar o usuário com o perfil associado
                usuario = User.objects.create_user(
                    name=user_data['name'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    perfil=perfil  # Aqui estamos associando o perfil corretamente
                )
                usuario.is_superuser = user_data['is_superuser']
                usuario.is_staff = user_data['is_staff']
                usuario.save()
                
                self.stdout.write(self.style.SUCCESS(f'Usuário {user_data["username"]} criado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuário {user_data["username"]} já existe!'))

