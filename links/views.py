import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.http import HttpResponseGone, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Categoria, ShortenedURL, Click, ShortenedURLCategoria
from registros.models import Usuario, Perfil
from .models import ShortenedURL

def track_click(request, short_code):
    url = get_object_or_404(ShortenedURL, short_code=short_code)

    Click.objects.create(
        url=url,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )

    return redirect(url.original_url)

@api_view(['POST'])
@permission_classes([AllowAny])
def shorten_url(request):
    original_url = request.data.get('url')
    user = request.user if request.user.is_authenticated else None
    categories = request.data.get('categories', [])

    if not original_url:
        return Response({'error': 'URL não fornecida'}, status=400)

    url_pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)(\/[\w\-./?%&=]*)?$')
    validator = URLValidator()

    try:
        validator(original_url) 
        if not url_pattern.match(original_url):
            raise ValidationError("URL inválida.")
    except ValidationError:
        return Response({'error': 'URL inválida. Certifique-se de incluir http:// ou https://'}, status=400)

    existing_url = ShortenedURL.objects.filter(original_url=original_url, user=user).first()
    if existing_url:
        return Response({'shortened_url': f"http://localhost:8000/{existing_url.short_code}"}, status=200)

    new_short_url = ShortenedURL.objects.create(original_url=original_url, user=user)

    if categories:
        for cat_name in categories:
            category, created = Categoria.objects.get_or_create(nome=cat_name)
            ShortenedURLCategoria.objects.create(url=new_short_url, categoria=category)

    return Response({'shortened_url': f"http://localhost:8000/{new_short_url.short_code}"}, status=201)



@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_to_original(request, short_code):
    short_url = ShortenedURL.objects.filter(short_code=short_code).first()
    
    if not short_url:
        return HttpResponseNotFound()

    if short_url.expires_at and short_url.expires_at <= now():
        return HttpResponseGone()

    return redirect(short_url.original_url)

# Função para editar link (somente usuários premium)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def premium_edit_links(request):
    user = request.user

    if user.perfil.nome != "Premium":
        return Response({'error': 'Apenas usuários premium podem editar links'}, status=403)

    short_code = request.data.get('short_code')
    new_original_url = request.data.get('new_url')

    if not short_code or not new_original_url:
        return Response({'error': 'Código curto e nova URL são necessários'}, status=400)

    url_pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)(\/[\w\-./?%&=]*)?$')
    validator = URLValidator()

    try:
        validator(new_original_url)
        if not url_pattern.match(new_original_url):
            raise ValidationError("URL inválida.")
    except ValidationError:
        return Response({'error': 'URL inválida. Certifique-se de incluir http:// ou https://'}, status=400)

    short_url = get_object_or_404(ShortenedURL, short_code=short_code, user=user)

    try:
        short_url.original_url = new_original_url
        short_url.save()
        return Response({'message': 'URL atualizada com sucesso'}, status=200)
    except Exception as e:
        return Response({'error': f'Ocorreu um erro: {str(e)}'}, status=500)

def link_stats(request, short_code):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Você precisa estar autenticado para acessar esta funcionalidade.")

    url = get_object_or_404(ShortenedURL, short_code=short_code)

    perfil_usuario = getattr(request.user, 'perfil', None)
    perfil_nome = perfil_usuario.nome if perfil_usuario else None
    perfis_permitidos = ["Premium", "Administrador"]

    if request.user == url.user or perfil_nome in perfis_permitidos:
        data = {
            "short_code": short_code,
            "original_url": url.original_url,
        }

        if perfil_nome in perfis_permitidos:
            data.update({
                "clicks": url.clicks.count(),
                "categories": list(url.categorias.values_list("nome", flat=True)),  # Ajuste aqui para pegar as categorias
                "qr_code": url.qr_code.image.url if hasattr(url, "qr_code") and url.qr_code.image else None,
            })

        return JsonResponse(data)

    return HttpResponseForbidden("Apenas usuários premium podem acessar estatísticas, QR Code e categorias.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_links(request):
    user = request.user
    links = ShortenedURL.objects.filter(user=user)
    data = [
        {
            'id': link.id,
            'original_url': link.original_url,
            'shortened_url': f"http://localhost:8000/{link.short_code}",
            'clicks': link.clicks.count(),
            'expiration_date': link.expires_at,
        }
        for link in links
    ]
    return Response(data, status=200)