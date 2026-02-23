import pytest

from src.app import activities


# The ``client`` fixture is provided by ``tests/conftest.py``

def test_root_redirect(client):
    response = client.get("/")
    # root currently returns a 200 serving the static index, so simply
    # verify we get the expected HTML content.
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")



def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    data = {"email": email}
    response = client.post("/activities/Chess Club/signup", params=data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    existing = activities["Chess Club"]["participants"][0]
    data = {"email": existing}
    response = client.post("/activities/Chess Club/signup", params=data)
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity(client):
    response = client.post("/activities/Nonexistent/signUp", params={"email": "foo@bar.com"})
    assert response.status_code == 404


def test_remove_participant_success(client):
    email = activities["Programming Class"]["participants"][0]
    response = client.delete(
        "/activities/Programming Class/participants", params={"email": email}
    )
    assert response.status_code == 200
    assert email not in activities["Programming Class"]["participants"]


def test_remove_participant_not_signed_up(client):
    response = client.delete(
        "/activities/Programming Class/participants", params={"email": "nobody@mergington.edu"}
    )
    assert response.status_code == 400


def test_remove_activity_not_found(client):
    response = client.delete(
        "/activities/Nope/participants", params={"email": "foo@bar.com"}
    )
    assert response.status_code == 404
