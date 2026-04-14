import pytest
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from app.models import Label


class TestLabelsApi:
    @pytest.fixture(scope='function')
    def labels(self, db):
        yield {
            'label1': Label.objects.create(
                name="Label 1",
                description=None,
            ),
            'label2': Label.objects.create(
                name="Label 2",
                description="Description for label 2",
            ),
        }

    def test_get_labels(self, api_client, labels):
        url = reverse("label-list")
        response = api_client.get(url)

        assert response.status_code == 200
        response_data = response.data["results"]

        # ignore the default sorting for this test case
        response_data = sorted(response_data, key=lambda x: x["id"])

        assert len(response_data) == 2

        assert response_data[0]["name"] == "Label 1"
        assert response_data[1]["name"] == "Label 2"

        assert response_data[0]["description"] is None
        assert response_data[1]["description"] == "Description for label 2"

        label1, label2 = labels.values()
        assert parse_datetime(response_data[0]["created_at"]) == label1.created_at
        assert parse_datetime(response_data[1]["created_at"]) == label2.created_at

    def test_get_label(self, api_client, labels):
        label1 = labels["label1"]

        url = reverse("label-detail", kwargs={"pk": label1.pk})
        response = api_client.get(url)
        assert response.status_code == 200

        assert response.data["id"] == label1.pk
        assert response.data["name"] == "Label 1"
        assert response.data["description"] is None

        assert parse_datetime(response.data["created_at"]) == label1.created_at

    # TODO: add more tests
