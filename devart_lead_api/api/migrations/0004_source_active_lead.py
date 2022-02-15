# Generated by Django 4.0 on 2022-01-23 12:17

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_key_delete_sourceapikey'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodne_cislo', models.CharField(max_length=20, verbose_name='Rodne Cislo')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Price')),
                ('duplicity', models.BooleanField(default=0, verbose_name='Duplicity')),
                ('source', models.ForeignKey(on_delete=api.models.Source, to='api.source')),
            ],
        ),
    ]