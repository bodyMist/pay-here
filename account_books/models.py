from django.db import models
from members.models import Member

class AccountBook(models.Model):
    account_book_id = models.AutoField(primary_key=True)
    written = models.DateField()
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ACCOUNT_BOOK'

class Detail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    account_book_id = models.ForeignKey(AccountBook, on_delete=models.CASCADE)

    class Meta:
        db_table = 'DETAIL'

class ShortUrl(models.Model):
    short_url_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2000)
    encoded = models.CharField(max_length=1000)
    expired = models.DateTimeField()
    
    class Meta:
        db_table = 'SHORT_URL'