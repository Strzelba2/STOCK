# Generated by Django 3.1.3 on 2021-02-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_currency_account_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='cantor',
            name='exchange_rate_after',
            field=models.FloatField(blank=True, null=True),
        ),
    ]