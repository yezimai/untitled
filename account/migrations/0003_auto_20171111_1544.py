# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20171111_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_date',
            field=models.DateTimeField(auto_now=True, verbose_name='\u53d1\u9001\u7684\u65f6\u95f4'),
        ),
    ]
