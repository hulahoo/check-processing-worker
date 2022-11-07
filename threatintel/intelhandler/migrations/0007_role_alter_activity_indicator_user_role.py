# Generated by Django 4.0.4 on 2022-08-25 12:23

from django.db import migrations, models
import django.db.models.deletion
from threatintel.intelhandler import models as intel_models


class Migration(migrations.Migration):

    dependencies = [
        ('intelhandler', '0006_activity_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', intel_models.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', intel_models.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('name', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='activity',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='intelhandler.indicator'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='intelhandler.role'),
        ),
    ]
