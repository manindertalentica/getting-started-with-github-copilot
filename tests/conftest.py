import pytest

from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the global activities dictionary between tests.

    The tests modify the in-memory state; this fixture saves a copy of the
    original dictionary and restores it after each test so that tests are
    isolated from one another.
    """
    original = {name: data.copy() for name, data in activities.items()}
    yield
    activities.clear()
    activities.update({name: data.copy() for name, data in original.items()})
