# Generated by Django 3.2.16 on 2022-12-20 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]