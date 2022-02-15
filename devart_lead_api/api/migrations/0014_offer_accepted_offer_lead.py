# Generated by Django 4.0 on 2022-02-09 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_acceptdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='Accepted'),
        ),
        migrations.AddField(
            model_name='offer',
            name='lead',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.lead'),
        ),
    ]
