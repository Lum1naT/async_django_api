# Generated by Django 4.0 on 2022-02-02 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_request_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='duplicity',
        ),
        migrations.AddField(
            model_name='lead',
            name='bought',
            field=models.BooleanField(default=False, verbose_name='Bought'),
        ),
    ]
