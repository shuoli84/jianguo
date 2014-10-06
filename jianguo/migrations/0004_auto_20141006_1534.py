# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jianguo', '0003_auto_20141006_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u53d1\u5e03'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='\u5185\u5bb9', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(verbose_name='\u6807\u9898', blank=True),
        ),
    ]
