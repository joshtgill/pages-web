# Generated by Django 3.1.5 on 2021-01-27 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0006_remove_creatoruser_organizations'),
        ('meta', '0003_remove_organization_creatoruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='creatorUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='builder.creatoruser'),
            preserve_default=False,
        ),
    ]