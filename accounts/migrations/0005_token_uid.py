# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-30 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_token_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='uid',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
