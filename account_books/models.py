from django.db import models
from members.models import Member

class AccountBook(models.Model):
    account_book_id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    written = models.DateField()
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)

class Detail(models.Model):
    detail_id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    account_book_id = models.ForeignKey(AccountBook, on_delete=models.CASCADE)

class ShortUrl(models.Model):
    short_url_id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    url = models.CharField(max_length=2000)
    encoded = models.CharField(max_length=1000)
    expired = models.DateTimeField()