# Generated by Django 3.2.5 on 2021-07-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0052_rename_description_page_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='color',
            field=models.CharField(default='rgb(231, 231, 231)', max_length=30),
            preserve_default=False,
        ),
    ]