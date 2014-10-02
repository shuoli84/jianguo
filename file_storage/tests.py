from django.core.files.base import ContentFile
from django.test import TestCase
from file_storage.storages import DatabaseStorage


class FileStorage(TestCase):
    def test_save(self):
        storage = DatabaseStorage()
        path = storage.save('abc', ContentFile('test'))
        self.assertIsNotNone(path)

        path2 = storage.save('abc', ContentFile('test 2'))
        self.assertNotEqual(path, path2)

        paths = set()
        count = 5000
        for i in xrange(0, count):
            path = storage.save('abc', ContentFile('test content'))
            self.assertTrue(path not in paths)
            paths.add(path)
        self.assertEqual(len(paths), count)
        print paths
