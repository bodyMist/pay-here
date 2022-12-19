from django.db import models

# Create your models here.
class Member(models.Model):
    member_id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'MEMBERS'