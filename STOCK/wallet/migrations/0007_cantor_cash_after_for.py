# Generated by Django 3.1.3 on 2021-02-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_auto_20210213_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='cantor',
            name='cash_after_for',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
