from django.shortcuts import get_object_or_404
from registros.models import Usuario, Perfil
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tornar_premium(request):
    usuario = request.user

    perfil_premium = get_object_or_404(Perfil, id=2)

    if usuario.perfil == perfil_premium:
        return Response({'message': 'Usuário já é premium.'}, status=400)

    usuario.perfil = perfil_premium
    usuario.save()

    return Response({'message': 'Usuário atualizado para Premium.'}, status=200)
