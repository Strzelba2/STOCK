# Generated by Django 3.1.3 on 2021-02-20 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0012_auto_20210220_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='broker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.broker_account'),
        ),
    ]
