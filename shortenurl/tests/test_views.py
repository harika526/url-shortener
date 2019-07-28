import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Links
from ..serializers import LinksSerializer


# initialize the APIClient app
client = Client()


class GetAllLinksTest(TestCase):
    """ Tests for GET all links API """

    def setUp(self):
        Links.objects.create(main_url='https://google.com', short_url='abc')
        Links.objects.create(main_url='https://youtube.com', short_url='def')
        Links.objects.create(main_url='https://yahoo.com', short_url='123')
        Links.objects.create(main_url='https://bing.com', short_url='456')

    def test_get_all_links(self):
        # get API response
        response = client.get(reverse('get_post_link'))
        # get data from db
        links = Links.objects.all()
        serializer = LinksSerializer(links, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleLinkTest(TestCase):
    """ Tests for GET single link API """

    def setUp(self):
        self.google = Links.objects.create(main_url='https://google.com', short_url='abc')
        self.youtube = Links.objects.create(main_url='https://youtube.com', short_url='def')
        self.yahoo = Links.objects.create(main_url='https://yahoo.com', short_url='123')
        self.bing = Links.objects.create(main_url='https://bing.com', short_url='456')

    def test_get_valid_single_link(self):
        response = client.get(reverse('get_delete_link', kwargs={'surl': self.bing.short_url}))
        link = Links.objects.get(pk=self.bing.pk)
        serializer = LinksSerializer(link)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_link(self):
        response = client.get(reverse('get_delete_link', kwargs={'surl': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewLinkTest(TestCase):
    """ Tests for adding a new link """

    def setUp(self):
        self.valid_post = {
            'main_url': 'https://google.com',
            'short_url': 'abc',
        }
        self.invalid_post = {
            'main_url': '',
            'short_url': 'def',
        }

    def test_create_valid_link(self):
        response = client.post(reverse('get_post_link'),
                               data=json.dumps(self.valid_post),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_link(self):
        response = client.post(reverse('get_post_link'),
                               data=json.dumps(self.invalid_post),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleLinkTest(TestCase):
    """ Tests for deleting an existing record """

    def setUp(self):
        self.google = Links.objects.create(main_url='https://google.com', short_url='abc')
        self.youtube = Links.objects.create(main_url='https://youtube.com', short_url='def')

    def test_delete_valid_link(self):
        response = client.delete(
            reverse('get_delete_link', kwargs={'surl': self.youtube.short_url}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_link(self):
        response = client.delete(
            reverse('get_delete_link', kwargs={'surl': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

