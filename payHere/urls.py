"""payHere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework_simplejwt.views import TokenRefreshView

from account_books.views import ShortUrlAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('auth/refresh', TokenRefreshView.as_view()),
    path('account-books/', include('account_books.urls')),
    path('short', ShortUrlAPIView.as_view()),
    path('short/<str:encoded>', ShortUrlAPIView.as_view()),
]
