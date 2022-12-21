from django.db import models
from members.models import Member

class AccountBook(models.Model):
    account_book_id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    written = models.DateTimeField()
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ACCOUNT_BOOKS'

class ShortUrl(models.Model):
    short_url_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2000)
    encoded = models.CharField(max_length=1000)
    expired = models.DateTimeField()
    
    class Meta:
        db_table = 'SHORT_URLS'