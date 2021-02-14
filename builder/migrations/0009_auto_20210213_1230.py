# Generated by Django 3.1.5 on 2021-02-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0008_auto_20210126_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='iconFileName',
        ),
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
