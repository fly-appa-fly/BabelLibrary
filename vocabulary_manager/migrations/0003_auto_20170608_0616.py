# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary_manager', '0002_auto_20170601_0222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vocabularyword',
            name='state',
        ),
        migrations.AddField(
            model_name='vocabularyword',
            name='easiness_factor',
            field=models.FloatField(default=2.5),
        ),
        migrations.AddField(
            model_name='vocabularyword',
            name='interval',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='vocabularyword',
            name='repetitions',
            field=models.IntegerField(default=0),
        ),
    ]
