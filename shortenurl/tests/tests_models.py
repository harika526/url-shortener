from django.test import TestCase
from ..models import Links


class LinksTest(TestCase):
    """ Tests for Links model """

    def setUp(self):
        Links.objects.create(main_url='https://google.com', short_url='abc')
        Links.objects.create(main_url='https://youtube.com', short_url='def')

    def test_puppy_breed(self):
        google = Links.objects.get(main_url='https://google.com')
        youtube = Links.objects.get(main_url='https://youtube.com')
        self.assertEqual(google.short_url, 'abc')
        self.assertEqual(youtube.short_url, 'def')
