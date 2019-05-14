import re

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apis.models import Person, PersonTitle, Title, TitleGenre


class PersonTests(APITestCase):
    fixtures = ['movies_test.json']

    def setUp(self):
        self.valid_id = 1
        self.invalid_id = 241

    def test_person_get(self):
        pk = self.valid_id
        url = reverse("person_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_json = response.json()
        person = Person.objects.get(pk=pk)
        self.assertEqual(person.primary_name, person_json['primary_name'])

    def test_person_titles(self):
        pk = self.valid_id
        url = reverse("person_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_json = response.json()
        person_titles = PersonTitle.objects.filter(person__id=pk)
        self.assertEqual(len(person_titles), len(person_json['known_titles']))

    def test_person_not_found(self):
        pk = self.invalid_id
        url = reverse("person_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_lookup(self):
        name = "john"
        url = reverse("person_lookup", args=[name, ])
        response = self.client.get(url, format='json')
        person_list = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(person_list), 0)
        self.assertIsNotNone(re.search("john", person_list[0]['primary_name'].lower()))

    def test_person_lookup_not_found(self):
        name = "lorem ipsum"
        url = reverse("person_lookup", args=[name, ])
        response = self.client.get(url, format='json')
        person_list = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(person_list), 0)

    def test_person_put_restricted(self):
        pk = self.valid_id
        url = reverse("person_detail", args=[pk, ])
        response = self.client.put(url, data={"primary_name": "John Doe"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TitleTests(APITestCase):
    fixtures = ['movies_test.json']

    def setUp(self):
        self.valid_id = 42192
        self.invalid_id = 0

    def test_title_get(self):
        pk = self.valid_id
        url = reverse("title_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title_json = response.json()
        title = Title.objects.get(pk=pk)
        self.assertEqual(title.original_name, title_json['original_name'])

    def test_title_genres(self):
        pk = self.valid_id
        url = reverse("title_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title_json = response.json()
        title_genres = TitleGenre.objects.filter(title__id=pk)
        self.assertEqual(len(title_genres), len(title_json['genres']))

    def test_title_titles(self):
        pk = self.valid_id
        url = reverse("title_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title_json = response.json()
        title_genres = TitleGenre.objects.filter(title__id=pk)
        self.assertEqual(len(title_genres), len(title_json['genres']))

    def test_title_not_found(self):
        pk = self.invalid_id
        url = reverse("title_detail", args=[pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_title_put_restricted(self):
        pk = self.valid_id
        url = reverse("title_detail", args=[pk, ])
        response = self.client.put(url, data={"original_name": "Twinkle twinkle"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
