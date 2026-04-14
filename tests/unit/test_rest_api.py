from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
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

    @pytest.fixture(scope='function')
    def labels_extended(self, db):
        base_time = timezone.now()

        return {
            'a': Label.objects.create(
                name="A",
                description=None,
                created_at=base_time
            ),
            'b': Label.objects.create(
                name="B",
                description="B desc",
                created_at=base_time + timedelta(minutes=1)
            ),
            'c': Label.objects.create(
                name="G",
                description="G desc",
                created_at=base_time + timedelta(minutes=2)
            ),
        }

    def test_list_structure(self, api_client, labels):
        url = reverse("label-list")
        response = api_client.get(url)
        assert response.status_code == 200

        assert "results" in response.data
        assert isinstance(response.data["results"], list)

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

    def test_detail_not_found(self, api_client, db):
        url = reverse("label-detail", kwargs={"pk": 999999})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_filter_by_exact_name(self, api_client, labels_extended):
        url = reverse("label-list")
        response = api_client.get(url, {"name": "B"})
        assert response.status_code == 200

        results = response.data["results"]
        assert len(results) == 1
        assert results[0]["name"] == "B"

    def test_filter_by_created_at_gte(self, api_client, labels_extended):
        label_b = labels_extended["b"]

        url = reverse("label-list")
        response = api_client.get(url, {
            "created_at__gte": label_b.created_at.isoformat()
        })
        assert response.status_code == 200

        names = [r["name"] for r in response.data["results"]]
        assert "A" not in names
        assert "B" in names
        assert "G" in names

    def test_ordering_desc(self, api_client, labels_extended):
        url = reverse("label-list")
        response = api_client.get(url, {"ordering": "-created_at"})
        assert response.status_code == 200

        results = response.data["results"]
        dates = [parse_datetime(res["created_at"]) for res in results]

        assert dates == sorted(dates, reverse=True)

    def test_ordering_asc(self, api_client, labels_extended):
        url = reverse("label-list")
        response = api_client.get(url, {"ordering": "created_at"})
        assert response.status_code == 200

        results = response.data["results"]
        dates = [parse_datetime(res["created_at"]) for res in results]

        assert dates == sorted(dates)

    def test_filter_by_created_at_range_gte_lte(self, api_client, labels_extended):
        label_a = labels_extended["a"]
        label_b = labels_extended["b"]

        url = reverse("label-list")
        response = api_client.get(url, {
            "created_at__gte": label_a.created_at.isoformat(),
            "created_at__lte": label_b.created_at.isoformat(),
        })
        assert response.status_code == 200

        names = [res["name"] for res in response.data["results"]]

        # all should be included
        assert "A" in names
        assert "B" in names
        assert "G" not in names

        assert len(names) == 2
