from rest_framework import status,exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import transaction
from django.http import HttpResponseRedirect
from django.conf import settings
from account_books.models import AccountBook, ShortUrl
from account_books.serializers import AccountBookSerializer, ShortUrlSerializer

from datetime import datetime, timedelta
import os

class AccountBookListAPIView(APIView):
    def get_list(self, member_id, year=None, month=None, day=None):
        try:
            queryset_1 = AccountBook.objects.filter(member_id=member_id).order_by('written')
            if year is not None:
                queryset_2 = AccountBook.objects.filter(written__year=year)
                queryset_1 = queryset_1 & queryset_2
            if month is not None:
                queryset_3 = AccountBook.objects.filter(written__month=month)
                queryset_1 = queryset_1 & queryset_3
            if day is not None:
                queryset_4 = AccountBook.objects.filter(written__day=day)
                queryset_1 = queryset_1 & queryset_4
            account_book_list = list(queryset_1)
            return account_book_list
        except:
            raise AccountBook.DoesNotExist

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

    @transaction.atomic
    def get(self, request):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        if member_data is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        member_id = member_data.__getattribute__('member_id')
        
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        day = request.GET.get('day', None)

        account_book_list = self.get_list(member_id,year,month,day)
        serializer = AccountBookSerializer(account_book_list, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
            

class AccountBookDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return AccountBook.objects.get(account_book_id=pk)
        except AccountBook.DoesNotExist:
            raise exceptions.NotFound
    
    @transaction.atomic
    def post(self, request, pk):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        account_book = self.get_object(pk)  # raise exception

        if member_data is None or \
        member_data.__getattribute__('member_id') == account_book.__getattribute__('member_id'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        new_data = {
            'account_book_id': None,
            'description': account_book.description + '-copy',
            'written': account_book.written,
            'member_id': member_data.__getattribute__('member_id')
        }
        serializer = AccountBookSerializer(data=new_data)

        if serializer.is_valid():
            serializer.save()
        
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @transaction.atomic
    def get(self, request, pk):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        account_book = self.get_object(pk)  # raise exception
        serializer = AccountBookSerializer(account_book)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    
    @transaction.atomic
    def put(self, request, pk):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        account_book = self.get_object(pk)  # raise exception

        if member_data is None or \
        member_data.__getattribute__('member_id') == account_book.__getattribute__('member_id'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data['member_id'] = member_data.__getattribute__('member_id')
        serializer = AccountBookSerializer(account_book, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    def delete(self, request, pk):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        account_book = self.get_object(pk)  # raise exception

        if member_data is None or \
        member_data.__getattribute__('member_id') == account_book.__getattribute__('member_id'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        account_book.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class ShortUrlAPIView(APIView):
    def convert_base62(self, pk):
        CODEC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ret = []
        pk = int(pk)
        while pk > 0:
            pk, idx = divmod(pk, 62)
            ret.insert(0, CODEC[idx])
        return ''.join(ret)


    @transaction.atomic
    def post(self, request):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        target_url = request.data['url']
        try:
            url = ShortUrl.objects.get(url=target_url)
            serializer = ShortUrlSerializer(url)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )
        except ShortUrl.DoesNotExist:
            pk = target_url.split('/')[-1]
            temp_url = self.convert_base62(pk)
            encoded = settings.APP_URL + temp_url
            request.data['encoded'] = encoded
            request.data['expired'] = datetime.now() + timedelta(hours=6)
            serializer = ShortUrlSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save(encoded=encoded)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    @transaction.atomic
    @permission_classes([AllowAny])
    def get(self, request, encoded):
        jwt_authenticator = JWTAuthentication()
        member_data, token = jwt_authenticator.authenticate(request)
        encoded_url = 'http://127.0.0.1:8000/short/' + encoded
        print(encoded_url)
        redirect = ShortUrl.objects.get(encoded=encoded_url)
        date_diff = datetime.now() - redirect.expired
        if date_diff.seconds > 0:
            return HttpResponseRedirect(redirect_to=redirect.url)
        redirect.delete()
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )