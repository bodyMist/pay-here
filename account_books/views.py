from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import transaction
from datetime import datetime

from account_books.models import AccountBook
from account_books.serializers import AccountBookSerializer

class AccountBookAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        # Authorization: Bearer access_token        
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        if member_data is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        request_data = JSONParser().parse(request)
        
        request_data['member_id'] = member_data.__getattribute__('member_id')
        serializer = AccountBookSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )