# Generated by Django 3.2 on 2021-05-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0049_auto_20210414_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
