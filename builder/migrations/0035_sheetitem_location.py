# Generated by Django 3.1.5 on 2021-03-24 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0034_auto_20210323_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetitem',
            name='location',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
