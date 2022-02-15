# Generated by Django 4.0 on 2022-02-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_offer_created_at_alter_offer_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='bought',
        ),
        migrations.AddField(
            model_name='offer',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='Checked'),
        ),
    ]
