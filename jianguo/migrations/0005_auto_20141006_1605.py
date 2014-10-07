# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sites.models import Site

from django.db import models, migrations


def create_site(apps, schema_editor):
    site = Site()
    site.domain = 'www.jianguo.com'
    site.name = 'jianguo'
    site.id = 1
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jianguo', '0004_auto_20141006_1534'),
        #('django.contrib.sites', '__first__'),
    ]

    operations = [
        migrations.RunPython(create_site)
    ]
