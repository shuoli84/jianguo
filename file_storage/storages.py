import os
import random
from urlparse import urljoin
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.db import IntegrityError
from django.middleware.transaction import transaction
import time
from file_storage.models import File


class DatabaseStorage(Storage):

    def __init__(self):
        super(DatabaseStorage, self).__init__()

        self.base_url = settings.MEDIA_URL

    def save(self, name, content):
        original_name, ext = os.path.splitext(name)
        filename = original_name

        count = 10
        if hasattr(content, 'file'):
            content_data = content.file.read()
        elif hasattr(content, 'read'):
            content_data = content.read()
        else:
            raise ValueError("Don't know how to read content")

        while count:
            try:
                with transaction.atomic():
                    file_record = File()
                    file_record.path = filename + ext
                    file_record.content = content_data
                    file_record.size = len(content_data)
                    file_record.save()
                    return file_record.path
            except IntegrityError, e:
                if count:
                    count -= 1
                    filename = u'%s_%d' % (original_name, hash(time.time()))
                    continue
                else:
                    raise

    def open(self, name, mode='rb'):
        file_record = File.objects.get(path=name)
        return ContentFile(file_record.content)

    def delete(self, name):
        File.objects.filter(path=name).delete()

    def exists(self, name):
        return File.objects.filter(path=name).exists()

    def listdir(self, path):
        raise NotImplementedError()

    def size(self, name):
        file_ = File.objects.get(path="name")
        return file_.size

    def url(self, name):
        return urljoin(self.base_url, name)
