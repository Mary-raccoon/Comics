# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-28 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0004_auto_20190327_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='docfile',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
