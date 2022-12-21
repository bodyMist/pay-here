from django.contrib import admin
from account_books.models import AccountBook, ShortUrl

admin.site.register([AccountBook, ShortUrl])