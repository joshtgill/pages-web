# Generated by Django 3.2.5 on 2021-07-26 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0065_rename_name_pageinfo_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pageinfo',
            old_name='monoItemed',
            new_name='hasSingleItem',
        ),
    ]
