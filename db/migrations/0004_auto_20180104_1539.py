# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-04 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20180104_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memory',
            name='size',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='内存/G'),
        ),
    ]
