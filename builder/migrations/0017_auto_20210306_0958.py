# Generated by Django 3.1.5 on 2021-03-06 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0016_organization_membershiprequired'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='membershipRequired',
            new_name='private',
        ),
    ]
