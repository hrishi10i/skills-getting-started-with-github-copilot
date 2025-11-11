import copy
import pytest

from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app


client = TestClient(app)
original = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # restore the original in-memory activities before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
    yield


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister():
    email = "testuser@example.com"
    activity = "Chess Club"

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # unregister
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "noone@nowhere.test"
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp.status_code == 404
