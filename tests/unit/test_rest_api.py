from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase

from app.models import Label


class LabelsApiTest(APITestCase):
    def setUp(self):
        self.label1 = Label.objects.create(
            name="Label 1",
            description=None,
        )
        self.label2 = Label.objects.create(
            name="Label 2",
            description="Description for label 2",
        )

    def test_get_labels(self):
        url = reverse("label-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.data['results']
        response_data = sorted(response_data, key=lambda x: x['id'])  # ignore the default sorting for this test case
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], "Label 1")
        self.assertEqual(response_data[1]['name'], "Label 2")
        self.assertEqual(response_data[0]['description'], None)
        self.assertEqual(response_data[1]['description'], "Description for label 2")
        self.assertEqual(parse_datetime(response_data[0]['created_at']), self.label1.created_at)
        self.assertEqual(parse_datetime(response_data[1]['created_at']), self.label2.created_at)

    def test_get_label(self):
        url = reverse("label-detail", kwargs={"pk": self.label1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.label1.pk)
        self.assertEqual(response.data['name'], 'Label 1')
        self.assertEqual(response.data['description'], None)
        self.assertEqual(parse_datetime(response.data['created_at']), self.label1.created_at)

    # TODO: add more tests
