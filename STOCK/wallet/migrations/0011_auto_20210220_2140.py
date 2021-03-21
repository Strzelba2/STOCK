# Generated by Django 3.1.3 on 2021-02-20 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WIG', '0006_auto_20210125_2126'),
        ('wallet', '0010_broker_account_stocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WIG.companydata'),
        ),
    ]