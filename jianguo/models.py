# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User)

    name = models.TextField(u'名字')
    career = models.TextField(u'职业', blank=True, null=True)
    introduction = models.TextField(u'简介', blank=True, null=True)

    avatar = models.ImageField(u'头像', null=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.TextField(u'标题')
    content = models.TextField(u'内容')
    created_at = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.title


def create_profile(sender, **kw):
    """
    Create the user profile when a user object is created
    """
    user = kw["instance"]
    if kw["created"]:
        profile = Profile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profile-creation-signal")