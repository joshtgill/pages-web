# Generated by Django 3.1.5 on 2021-03-17 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0030_auto_20210316_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='dateJoined',
            new_name='relatedDate',
        ),
    ]
