# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-29 08:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userinfo',
        ),
    ]
