# Generated by Django 2.1.15 on 2020-05-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0011_auto_20200504_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
