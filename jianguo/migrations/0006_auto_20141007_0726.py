# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models, migrations


def create_default_avatar(apps, schema_editor):
    Profile = apps.get_model("jianguo", "Profile")
    for p in Profile.objects.filter(avatar=''):
        p.avatar = settings.DEFAULT_AVATAR
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jianguo', '0005_auto_20141006_1605'),
    ]

    operations = [
        migrations.RunPython(create_default_avatar)
    ]