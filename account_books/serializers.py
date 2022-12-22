from rest_framework import serializers
from account_books.models import AccountBook, ShortUrl

class AccountBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'

class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = '__all__'