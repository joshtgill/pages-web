# Generated by Django 3.1.5 on 2021-03-09 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('builder', '0017_auto_20210306_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='requesters',
            field=models.ManyToManyField(to='client.ClientUser'),
        ),
    ]
