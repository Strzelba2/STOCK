# Generated by Django 3.1.2 on 2020-11-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusers',
            name='facebook_picture',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='myusers',
            name='facebook_user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
