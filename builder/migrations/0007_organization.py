# Generated by Django 3.1.5 on 2021-01-27 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0006_remove_creatoruser_organizations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('creatorUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.creatoruser')),
            ],
        ),
    ]
