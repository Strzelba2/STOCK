# Generated by Django 3.1.3 on 2021-03-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0020_auto_20210318_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nc',
            name='order',
        ),
        migrations.RemoveField(
            model_name='stocks',
            name='order',
        ),
        migrations.AddField(
            model_name='nc_transfer',
            name='order',
            field=models.CharField(choices=[('Zakup', 'Zakup'), ('Sprzedarz', 'Sprzedarz')], default='Zakup', max_length=9),
        ),
        migrations.AddField(
            model_name='stocks_transfer',
            name='order',
            field=models.CharField(choices=[('Zakup', 'Zakup'), ('Sprzedarz', 'Sprzedarz')], default='Zakup', max_length=9),
        ),
    ]
