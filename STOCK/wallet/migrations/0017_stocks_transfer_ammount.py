# Generated by Django 3.1.3 on 2021-03-04 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0016_broker_account_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks_transfer',
            name='ammount',
            field=models.IntegerField(default=1),
        ),
    ]