import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from hawc.apps.vocab.models import Guideline, GuidelineProfile, Term


@pytest.mark.django_db
class TestEhvTermViewSet:
    def test_permissions(self):
        url = reverse("vocab:api:ehv-system")
        anon_client = APIClient()
        auth_client = APIClient()
        assert auth_client.login(username="team@hawcproject.org", password="pw") is True
        assert anon_client.get(url).status_code == 403
        assert auth_client.get(url).status_code == 200

    def test_expected_response(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        test_cases = [
            # test urls resolve
            (reverse("vocab:api:ehv-system"), [{"id": 1, "name": "Cardiovascular"}]),
            (reverse("vocab:api:ehv-organ"), [{"id": 2, "name": "Serum"}]),
            (reverse("vocab:api:ehv-effect"), [{"id": 3, "name": "Fatty Acids"}]),
            (reverse("vocab:api:ehv-effect-subtype"), [{"id": 4, "name": "Clinical Chemistry"}]),
            (reverse("vocab:api:ehv-endpoint-name"), [{"id": 5, "name": "Fatty Acid Balance"}]),
        ]

        for url, resp in test_cases:
            assert client.get(url).json() == resp

    def test_nested(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True
        url = reverse("vocab:api:ehv-nested") + "?format=csv"
        resp = client.get(url)
        assert resp.status_code == 200
        data = resp.content.decode().split("\n")
        assert len(data) >= 2
        assert (
            data[0]
            == "system_term_id,system,organ_term_id,organ,effect_term_id,effect,effect_subtype_term_id,effect_subtype,name_term_id,name"
        )

    def test_query_params(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        test_cases = [
            # test term lookup
            (
                reverse("vocab:api:ehv-endpoint-name") + "?term=Acid",
                [{"id": 5, "name": "Fatty Acid Balance"}],
            ),
            (reverse("vocab:api:ehv-endpoint-name") + "?term=NONE", []),
            # test parent lookup
            (
                reverse("vocab:api:ehv-endpoint-name") + "?parent=4",
                [{"id": 5, "name": "Fatty Acid Balance"}],
            ),
            (reverse("vocab:api:ehv-endpoint-name") + "?parent=3", []),
            (
                reverse("vocab:api:ehv-endpoint-name") + "?parent=text",
                [{"id": 5, "name": "Fatty Acid Balance"}],
            ),
        ]

        for url, resp in test_cases:
            assert client.get(url).json() == resp


@pytest.mark.django_db
class TestToxRefDBTermViewSet:
    def test_permissions(self):
        url = reverse("vocab:api:toxrefdb-system")
        anon_client = APIClient()
        auth_client = APIClient()
        assert auth_client.login(username="team@hawcproject.org", password="pw") is True
        assert anon_client.get(url).status_code == 403
        assert auth_client.get(url).status_code == 200

    def test_expected_response(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        test_cases = [
            # test urls resolve
            (reverse("vocab:api:toxrefdb-system"), [{"id": 7000, "name": "systemic"}]),
            (reverse("vocab:api:toxrefdb-effect"), [{"id": 7001, "name": "pathology microscopic"}]),
            (reverse("vocab:api:toxrefdb-effect-subtype"), [{"id": 7002, "name": "eye"}]),
            (reverse("vocab:api:toxrefdb-endpoint-name"), [{"id": 7003, "name": "dysplasia"}]),
        ]

        for url, resp in test_cases:
            assert client.get(url).json() == resp

    def test_nested(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True
        url = reverse("vocab:api:toxrefdb-nested") + "?format=csv"
        resp = client.get(url)
        assert resp.status_code == 200
        data = resp.content.decode().split("\n")
        assert len(data) >= 2
        assert (
            data[0]
            == "system_term_id,system,effect_term_id,effect,effect_subtype_term_id,effect_subtype,name_term_id,name"
        )

    def test_query_params(self):
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        test_cases = [
            # test term lookup
            (
                reverse("vocab:api:toxrefdb-endpoint-name") + "?term=dysplasia",
                [{"id": 7003, "name": "dysplasia"}],
            ),
            (reverse("vocab:api:toxrefdb-endpoint-name") + "?term=NONE", []),
            # test parent lookup
            (
                reverse("vocab:api:toxrefdb-endpoint-name") + "?parent=7002",
                [{"id": 7003, "name": "dysplasia"}],
            ),
            (reverse("vocab:api:toxrefdb-endpoint-name") + "?parent=7001", []),
            (
                reverse("vocab:api:toxrefdb-endpoint-name") + "?parent=text",
                [{"id": 7003, "name": "dysplasia"}],
            ),
        ]

        for url, resp in test_cases:
            assert client.get(url).json() == resp


@pytest.mark.django_db
class TestTermViewSet:
    def test_bulk_permissions(self):
        url = reverse("vocab:api:term-bulk-create")
        # non superusers do not have permission
        client = APIClient()
        assert client.login(username="pm@hawcproject.org", password="pw") is True
        response = client.post(url, [], format="json")
        assert response.status_code == 403
        # superusers have permission
        client = APIClient()
        assert client.login(username="admin@hawcproject.org", password="pw") is True
        response = client.post(url, [], format="json")
        assert response.status_code == 201

    def test_bad_bulk_create(self):
        url = reverse("vocab:api:term-bulk-create")
        client = APIClient()
        assert client.login(username="admin@hawcproject.org", password="pw") is True

        test_cases = [
            # not array
            ({}, {"non_field_errors": ['Expected a list of items but got type "dict".']}),
            # id provided
            (
                [{"id": 1, "uid": 100, "type": 1, "name": "name"}],
                {"non_field_errors": ["'id' is prohibited."]},
            ),
            # wrong attr type
            (
                [{"uid": "slug", "type": 1, "name": "name"}],
                [{"uid": ["A valid integer is required."]}],
            ),
        ]

        for data, err in test_cases:
            response = client.post(url, data, format="json")
            assert response.status_code == 400 and response.json() == err

    def test_valid_bulk_create(self):
        url = reverse("vocab:api:term-bulk-create")
        client = APIClient()
        assert client.login(username="admin@hawcproject.org", password="pw") is True
        # simple singular create
        data = [{"uid": 100, "type": 1, "name": "new term 1", "notes": "notes"}]
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.json()[0].items() >= data[0].items()
        # multiple create with parents / deprecated
        data = [
            {"uid": 101, "type": 1, "name": "new term 2", "parent_id": 1},
            {"uid": 102, "type": 1, "name": "new term 3", "deprecated": True},
        ]
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.json()[0]["parent"] == 1
        assert response.json()[1]["deprecated_on"] is not None

    def test_bad_bulk_update(self):
        url = reverse("vocab:api:term-bulk-update")
        client = APIClient()
        assert client.login(username="admin@hawcproject.org", password="pw") is True

        test_cases = [
            # not array
            ({}, {"non_field_errors": ['Expected a list of items but got type "dict".']}),
            # id missing
            ([{"name": "name"}], [{"id": ["This field is required."]}]),
            # invalid id
            ([{"id": 9999, "name": "name"}], {"non_field_errors": ["Invalid 'id's: 9999."]}),
            (
                ["not-a-dict"],
                [{"non_field_errors": ["Invalid data. Expected a dictionary, but got str."]}],
            ),
            ([{"id": "str"}], [{"id": ["A valid integer is required."]}]),
            # wrong attr type
            ([{"id": 1, "type": "one"}], [{"type": ['"one" is not a valid choice.']}]),
        ]

        for data, err in test_cases:
            response = client.patch(url, data, format="json")
            assert response.status_code == 400 and response.json() == err

    def test_valid_bulk_update(self):
        url = reverse("vocab:api:term-bulk-update")
        client = APIClient()
        assert client.login(username="admin@hawcproject.org", password="pw") is True
        terms = Term.objects.filter(id__in=[1, 2, 3])
        data = [
            {"id": terms[0].id, "uid": 9999},
            {"id": terms[1].id, "deprecated": True},
            {"id": terms[2].id},
        ]
        response = client.patch(url, data, format="json")
        # term 3 was not updated
        assert len(response.json()) == 2
        terms = terms.all()
        # uid has been set on term 1
        assert terms[0].id == response.json()[0]["id"] and terms[0].uid == response.json()[0]["uid"]
        # deprecated_on has been set on term 2
        assert terms[1].id == response.json()[1]["id"] and terms[1].deprecated_on is not None


@pytest.mark.django_db
class TestGuidelineViewSet:
    def test_list(self):
        url = reverse("vocab:api:guideline-list")
        # anon cannot read
        anon_client = APIClient()
        assert anon_client.get(url).status_code == 403
        # authenticated can read
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True
        resp = client.get(url)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_anon_write_denied(self):
        url = reverse("vocab:api:guideline-list")
        anon_client = APIClient()
        resp = anon_client.post(
            url,
            {"id": 99999, "number": "999", "name": "Test", "profile_name": "test-anon"},
            format="json",
        )
        assert resp.status_code == 403

    def test_crud(self):
        url = reverse("vocab:api:guideline-list")
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        # create
        data = {
            "id": 99999,
            "number": "999.9999",
            "name": "Test Guideline",
            "profile_name": "test-crud",
        }
        resp = client.post(url, data, format="json")
        assert resp.status_code == 201
        guideline_id = resp.json()["id"]
        assert Guideline.objects.filter(id=guideline_id).exists()

        # read
        detail_url = f"{url}{guideline_id}/"
        resp = client.get(detail_url)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Test Guideline"

        # update
        resp = client.patch(detail_url, {"name": "Updated Guideline"}, format="json")
        assert resp.status_code == 200
        assert Guideline.objects.get(id=guideline_id).name == "Updated Guideline"

        # delete
        resp = client.delete(detail_url)
        assert resp.status_code == 204
        assert not Guideline.objects.filter(id=guideline_id).exists()


@pytest.mark.django_db
class TestGuidelineProfileViewSet:
    def test_list(self):
        url = reverse("vocab:api:guideline-profile-list")
        anon_client = APIClient()
        assert anon_client.get(url).status_code == 403
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True
        resp = client.get(url)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_anon_write_denied(self):
        url = reverse("vocab:api:guideline-profile-list")
        anon_client = APIClient()
        guideline = Guideline.objects.first()
        resp = anon_client.post(
            url, {"guideline": guideline.id, "description": "test"}, format="json"
        )
        assert resp.status_code == 403

    def test_crud(self):
        url = reverse("vocab:api:guideline-profile-list")
        client = APIClient()
        assert client.login(username="team@hawcproject.org", password="pw") is True

        guideline = Guideline.objects.first()
        term = Term.objects.first()

        # create
        data = {"guideline": guideline.id, "endpoint": term.id, "description": "Test Profile"}
        resp = client.post(url, data, format="json")
        assert resp.status_code == 201
        profile_id = resp.json()["id"]
        assert GuidelineProfile.objects.filter(id=profile_id).exists()

        # read
        detail_url = f"{url}{profile_id}/"
        resp = client.get(detail_url)
        assert resp.status_code == 200
        assert resp.json()["description"] == "Test Profile"

        # update
        resp = client.patch(detail_url, {"description": "Updated Profile"}, format="json")
        assert resp.status_code == 200
        assert GuidelineProfile.objects.get(id=profile_id).description == "Updated Profile"

        # filter by guideline
        filter_url = f"{url}?guideline={guideline.id}"
        resp = client.get(filter_url)
        assert resp.status_code == 200
        assert any(p["id"] == profile_id for p in resp.json())

        # delete
        resp = client.delete(detail_url)
        assert resp.status_code == 204
        assert not GuidelineProfile.objects.filter(id=profile_id).exists()
