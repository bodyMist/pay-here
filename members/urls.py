from django.urls import path
from members.views import *
urlpatterns = [
    path('signup', sign_up),
    path('login', login),
    path('logout', logout)
]