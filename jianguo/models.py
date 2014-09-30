# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)

    name = models.TextField(u'名字')
    introduction = models.TextField(u'简介')

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.TextField(u'标题')
    content = models.TextField(u'内容')
    created_at = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.title
