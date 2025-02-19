from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

from registros.models import Usuario

TOKENS = {}

@csrf_exempt
def recuperar_senha(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'O e-mail é obrigatório.'}, status=400)

            if Usuario.objects.filter(email=email).exists():
                token = get_random_string(32)
                TOKENS[token] = email 

                # Envia e-mail com o link de redefinição
                reset_url = f"http://localhost:5173/reset-password/{token}/"
                send_mail(
                    'Recuperação de senha',
                    f'Clique no link para redefinir sua senha: {reset_url}',
                    'seuemail@exemplo.com',
                    [email],
                )

                return JsonResponse({'message': 'Se o e-mail existir, um link será enviado.'}, status=200)

            return JsonResponse({'message': 'Se o e-mail existir, um link será enviado.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
def resetar_senha(request, token):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nova_senha = data.get('password')

            if not nova_senha:
                return JsonResponse({'error': 'A senha é obrigatória.'}, status=400)

            email = TOKENS.get(token)
            if email:
                user = Usuario.objects.get(email=email)
                user.password = make_password(nova_senha)
                user.save()
                del TOKENS[token]  # Remove o token após o uso

                return JsonResponse({'message': 'Senha redefinida com sucesso!'}, status=200)

            return JsonResponse({'error': 'Token inválido ou expirado.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
