# Generated by Django 3.1.5 on 2021-02-15 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0010_sheet_sheetitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='organization',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='builder.organization'),
            preserve_default=False,
        ),
    ]
