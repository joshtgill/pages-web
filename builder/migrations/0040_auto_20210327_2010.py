# Generated by Django 3.1.5 on 2021-03-27 20:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builder', '0039_auto_20210327_1502'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrganizationApplication',
            new_name='NewOrganizationRequest',
        ),
    ]