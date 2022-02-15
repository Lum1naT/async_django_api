# Generated by Django 4.0 on 2022-02-09 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_offer_accepted_offer_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(editable=False, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='lead',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.lead'),
        ),
    ]