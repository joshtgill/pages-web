# Generated by Django 3.1.5 on 2021-03-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0035_sheetitem_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetitem',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
