# Generated by Django 2.1.15 on 2020-05-06 11:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0012_auto_20200504_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 6, 13, 29, 32, 110493)),
        ),
    ]