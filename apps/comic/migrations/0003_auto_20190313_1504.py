# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-13 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0002_auto_20190313_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='date_of_purchase',
            field=models.DateField(blank=True, default='2019-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='date_of_sale',
            field=models.DateField(blank=True, default='2019-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='year',
            field=models.DateField(blank=True, default='2019-01-01', null=True),
        ),
    ]
