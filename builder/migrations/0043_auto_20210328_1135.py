# Generated by Django 3.1.5 on 2021-03-28 11:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builder', '0042_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='acceptees',
            field=models.ManyToManyField(related_name='event_acceptees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='declinees',
            field=models.ManyToManyField(related_name='event_declinees', to=settings.AUTH_USER_MODEL),
        ),
    ]
