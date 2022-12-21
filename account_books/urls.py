from django.urls import path
from account_books.views import *

urlpatterns = [
    path('', AccountBookListAPIView.as_view()),
    path('<int:pk>', AccountBookDetailAPIView.as_view()),
]