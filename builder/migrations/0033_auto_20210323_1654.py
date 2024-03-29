# Generated by Django 3.1.5 on 2021-03-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0032_auto_20210320_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sheetitem',
            name='startDataTime',
        ),
        migrations.AddField(
            model_name='sheetitem',
            name='startDateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='sheetitem',
            name='endDateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='sheetitem',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
