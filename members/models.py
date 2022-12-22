from django.db import models
from django.contrib.auth.models import (AbstractUser,BaseUserManager)
from django.contrib.auth.hashers import make_password

class MemberManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Memebers require an email field')

        user = self.model(
            email= self.normalize_email(email),
            password = make_password(password)
        )
        user.setUsername(email)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(
            email=email,
            password=make_password(password)
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class Member(AbstractUser):
    username=None
    member_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=255)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        db_table = 'MEMBERS'