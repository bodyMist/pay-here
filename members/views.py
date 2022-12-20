from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate

from members.models import Member
from members.serializers import MemberSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

@transaction.atomic
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    # TODO: data validation, exception Handler
    if request.method == 'POST':
        member = Member(
            email=request.data.get('email'),
            password=request.data.get('password')
            )
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            exist = Member.objects.filter(email=member.__getattribute__('email')).exists()
            if exist is True:
                return Response(data={"message":"email already exist"},status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # TODO: data validation, exception Handler
    
    # 토큰이 이미 발행되었지만 토큰을 첨부하지 않고 로그인 했을 경우,
    # 기존 토큰에 대한 만료 작업이 필요
    if request.method == 'POST':
        member = authenticate(
            username=request.data.get('email'),
            password=request.data.get('password')
        )
        if member is not None:
            serializer = MemberSerializer(data=member)
            token = TokenObtainPairSerializer.get_token(member)
            refresh_token = str(token)
            access_token = str(token.access_token)

            response = Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                status=status.HTTP_200_OK
                )
            return response
    return Response(status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        access_token = RefreshToken(request.data.get('access_token'))
        refresh_token = RefreshToken(request.data.get('refresh_token'))
        access_token.blacklist()
        refresh_token.blacklist()

        return Response(status=status.HTTP_204_NO_CONTENT)
        