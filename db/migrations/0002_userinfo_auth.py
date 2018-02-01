# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-21 01:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_remove_user_userinfo'),
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='auth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.User', verbose_name='关联'),
        ),
    ]
