import firebase_admin.auth as firebase_auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from registros.models import Usuario
from .serializers import UsuarioSerializer

@api_view(['POST'])
def login(request):
    """
    Realiza a autenticação do usuário e retorna um token.
    """
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    usuario = Usuario.objects.filter(email=username_or_email).first()
    if usuario:
        username = usuario.username  
    else:
        username = username_or_email 

    # Autentica com username e senha
    usuario = authenticate(request, username=username, password=password)

    if usuario is not None:
        auth_login(request, usuario)  # Cria a sessão no Django
        token, _ = Token.objects.get_or_create(user=usuario)

        return JsonResponse({
            "message": "Login realizado com sucesso!",
            "token": token.key,
            "usuario": {
                "id": usuario.id,
                "name": usuario.name,
                "username": usuario.username,
                "email": usuario.email,
                "perfil": usuario.perfil.nome if usuario.perfil else None  # Ajuste para acessar corretamente
            }
        }, status=200)

    return JsonResponse({"error": "Usuário ou senha inválidos."}, status=401)

@api_view(['POST'])
def google_login(request):
    """
    Autenticação com Google via Firebase.
    """
    id_token = request.data.get("id_token")  # Token recebido do frontend
    if not id_token:
        return JsonResponse({"error": "ID token é obrigatório."}, status=400)

    try:
        # Verifica e decodifica o ID Token do Firebase
        decoded_token = firebase_auth.verify_id_token(id_token)
        print("Token decodificado:", decoded_token)

        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name", "Usuário Google")

        if not email:
            return JsonResponse({"error": "O token não contém um e-mail válido."}, status=400)

        # Busca usuário no banco de dados
        usuario, created = Usuario.objects.get_or_create(email=email, defaults={
            "username": email.split("@")[0],  # Usa o prefixo do e-mail como username
            "name": name,
            "firebase_uid": uid,
            "is_active": True
        })

        # Se o usuário já existia, atualiza o UID do Firebase e salva
        if not created:
            usuario.firebase_uid = uid
            usuario.save()

        # Autenticação manual do usuário no Django
        usuario.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(request, usuario)

        return JsonResponse({
            "message": "Login com Google realizado com sucesso!",
            "usuario": {
                "id": usuario.id,
                "name": usuario.name,
                "username": usuario.username,
                "email": usuario.email
            }
        }, status=200)

    except firebase_auth.ExpiredIdTokenError:
        return JsonResponse({"error": "O token do Firebase expirou."}, status=400)

    except firebase_auth.InvalidIdTokenError:
        return JsonResponse({"error": "O token do Firebase é inválido."}, status=400)

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return JsonResponse({"error": f"Erro inesperado: {str(e)}"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Faz logout e deleta o token do usuário.
    """
    if request.user.is_authenticated:
        request.user.auth_token.delete()  # Deleta o token de autenticação
        auth_logout(request)  # Finaliza a sessão
        return JsonResponse({"message": "Logout realizado com sucesso."}, status=200)
    
    return JsonResponse({"error": "Usuário não autenticado."}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    """
    Retorna os dados do perfil do usuário autenticado.
    """
    usuario = request.user
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)