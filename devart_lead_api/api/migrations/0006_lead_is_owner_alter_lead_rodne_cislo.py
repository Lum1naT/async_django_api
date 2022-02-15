# Generated by Django 4.0 on 2022-01-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_request_lead_created_at_lead_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='is_owner',
            field=models.BooleanField(default=False, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='rodne_cislo',
            field=models.CharField(max_length=20, unique=True, verbose_name='Rodne Cislo'),
        ),
    ]