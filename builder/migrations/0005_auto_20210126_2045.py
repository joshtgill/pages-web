# Generated by Django 3.1.5 on 2021-01-27 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0001_initial'),
        ('builder', '0004_auto_20210123_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creatoruser',
            name='organization',
        ),
        migrations.AddField(
            model_name='creatoruser',
            name='organizations',
            field=models.ManyToManyField(to='meta.Organization'),
        ),
    ]
