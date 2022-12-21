from rest_framework import serializers
from account_books.models import AccountBook

class AccountBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'