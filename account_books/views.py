from rest_framework import status,exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import transaction
from account_books.models import AccountBook
from account_books.serializers import AccountBookSerializer

class AccountBookListAPIView(APIView):
    @transaction.atomic
    def post(self, request):     
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

class AccountBookDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return AccountBook.objects.get(account_book_id=pk)
        except AccountBook.DoesNotExist:
            raise exceptions.NotFound
    @transaction.atomic
    def get(self, request, pk):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        account_book = self.get_object(pk)  # raise exception

        if member_data is None or \
        member_data.__getattribute__('member_id') == account_book.__getattribute__('member_id'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = AccountBookSerializer(account_book)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )