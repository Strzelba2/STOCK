# Generated by Django 3.1.3 on 2021-02-28 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WIG', '0006_auto_20210125_2126'),
        ('wallet', '0014_broker_transfer_stocks_transfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='last_price',
            field=models.ForeignKey(default=447, on_delete=django.db.models.deletion.CASCADE, to='WIG.quotes_last'),
        ),
    ]
