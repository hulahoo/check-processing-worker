# Generated by Django 4.0.4 on 2022-08-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intelhandler', '0008_userstatistic'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='comment',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='false_or_positive',
            field=models.BooleanField(default=False),
        ),
    ]