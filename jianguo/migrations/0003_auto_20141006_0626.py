# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jianguo', '0002_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='career',
            field=models.TextField(null=True, verbose_name='\u804c\u4e1a', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='introduction',
            field=models.TextField(null=True, verbose_name='\u7b80\u4ecb', blank=True),
        ),
    ]
