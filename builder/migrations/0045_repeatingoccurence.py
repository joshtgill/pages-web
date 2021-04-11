# Generated by Django 3.1.5 on 2021-04-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0044_event_attendanceispublic'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepeatingOccurence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
    ]