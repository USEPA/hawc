import pytest
from django.urls import reverse

from ..test_utils import check_200, check_403, get_client


@pytest.mark.django_db
class TestHeatmapStudyDesign:
    def test_permission(self, db_keys):
        url = reverse("eco:heatmap_study_design", args=(db_keys.study_working,))
        client = get_client()
        check_403(client, url)

    def test_success(self, db_keys):
        url = reverse("eco:heatmap_study_design", args=(db_keys.study_working,))
        client = get_client("pm")
        check_200(client, url)


@pytest.mark.django_db
class TestHeatmapResult:
    def test_permission(self, db_keys):
        url = reverse("eco:heatmap_results", args=(db_keys.study_working,))
        client = get_client()
        check_403(client, url)

    def test_success(self, db_keys):
        url = reverse("eco:heatmap_results", args=(db_keys.study_working,))
        client = get_client("pm")
        check_200(client, url)


@pytest.mark.django_db
class TestResultView:
    def test_permission(self, db_keys):
        url = reverse("eco:result_list", args=(db_keys.study_working,))
        client = get_client()
        check_403(client, url)

    def test_success(self, db_keys):
        url = reverse("eco:result_list", args=(db_keys.study_working,))
        client = get_client("pm")
        response = check_200(client, url)
        assert len(response.context["object_list"]) == 1
