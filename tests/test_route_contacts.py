from unittest.mock import patch

import pytest

from src.database.models import Contact
from src.services.auth import auth_service


def test_create_contact(client, contact, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts/", json=contact, headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "test firstname"
        assert data["email"] == "test@test.com"
        assert "id" in data


def test_get_contact(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "test firstname"
        assert data["email"] == "test@test.com"
        assert "id" in data


def test_get_contact_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/2", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_get_contacts(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "test firstname"
        assert data[0]["email"] == "test@test.com"
        assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "first_name": "test firstname",
                "last_name": "test lastname",
                "email": "test2@test.com",
                "phone_number": "+380123456789",
                "birthday": "2001-05-25",
                "additional_info": "test test info",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "test firstname"
        assert data["email"] == "test2@test.com"
        assert "id" in data


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                "first_name": "test firstname",
                "last_name": "test lastname",
                "email": "test2@test.com",
                "phone_number": "+380123456789",
                "birthday": "2001-05-25",
                "additional_info": "test test info",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Contact not found"


@pytest.mark.parametrize(
    "param",
    [
        (""),
        ("first_name=test firstname"),
        ("last_name=test lastname"),
        ("email=test2@test.com"),
        ("first_name=test firstname&last_name=test lastname&email=test2@test.com"),
    ],
)
def test_search_contacts(client, token, param):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            f"/api/contacts/search?{param}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "test firstname"
        assert data[0]["last_name"] == "test lastname"
        assert data[0]["email"] == "test2@test.com"
        assert "id" in data[0]


def test_search_contacts_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            f"/api/contacts/search?first_name=username",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


def test_get_upcoming_birthdays(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            f"/api/contacts/upcoming_birthdays",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "test firstname"
        assert data[0]["last_name"] == "test lastname"
        assert data[0]["email"] == "test2@test.com"
        assert "id" in data[0]


def test_delete_contact(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "test firstname"
        assert data["email"] == "test2@test.com"
        assert "id" in data


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Contact not found"
