# Generated by Django 3.1.1 on 2020-11-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201109_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='playlist_id',
            field=models.IntegerField(),
        ),
    ]
