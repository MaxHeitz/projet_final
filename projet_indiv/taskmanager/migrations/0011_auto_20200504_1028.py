# Generated by Django 2.1.15 on 2020-05-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0010_auto_20200430_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
