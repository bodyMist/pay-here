from django.urls import path
from account_books.views import *

urlpatterns = [
    path('detail', AccountBookAPIView.as_view()),
]