# Generated by Django 3.2.5 on 2021-07-25 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0060_rename_pagelisting_pageinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='builder.pageinfo'),
            preserve_default=False,
        ),
    ]
