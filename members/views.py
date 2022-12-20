from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from members.models import Member
from members.serializers import MemberSerializer

@transaction.atomic
@api_view(['POST'])
def sign_up(request):
    # TODO: data validation, exception Handler
    if request.method == 'POST':
        member = Member(
            email=request.data.get('email'),
            password=request.data.get('password')
            )
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            # get()보다 filter().exists()가 fast
            # get()을 이용하여 객체를 반환할 필요 X
            exist = Member.objects.filter(email=member.__getattribute__('email')).exists()
            if exist is True:
                return Response(data={"message":"email already exist"},status=status.HTTP_400_BAD_REQUEST)
            
            member.save()
            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@transaction.atomic
@api_view(['POST'])
def login(request):
    # TODO: data validation, exception Handler, Jwt Authentication
    if request.method == 'POST':
        member = Member(
            email=request.data.get('email'),
            password=request.data.get('password')
            )
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            db_member = Member.objects.filter(email=member.__getattribute__('email'), password=member.__getattribute__('password'))
            
            return Response(status=status.HTTP_200_OK)    
    return Response(status=status.HTTP_400_BAD_REQUEST)