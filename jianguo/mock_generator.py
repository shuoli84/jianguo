# coding=utf-8
from django.contrib.auth.models import User
from django.utils import timezone
from jianguo.models import Article
import random


class MockGenerator(object):
    @classmethod
    def generate_user(cls):
        for index in xrange(0, 100):
            u = User()
            u.username = 'user_%d' % index
            u.set_password('pass')
            u.save()

            u.profile.name = 'user %d' % index
            u.profile.save()

    @classmethod
    def generate_article(cls):
        users = User.objects.all()
        for index in xrange(0, 100):
            a = Article()
            a.title = u'文章%d号' % index
            a.content = u'文章的内容' * 10
            a.author = users[random.randint(0, len(users)-1)]
            a.created_at = timezone.now()
            a.save()
