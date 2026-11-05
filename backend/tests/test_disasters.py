
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.core.database import Base, get_db


# Create a temporary SQLite database for testing
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Replace the real database with the test database
def override_get_db():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def sample_disaster():
    return {
        "name": "Hyderabad Flood Alert",
        "disaster_type": "flood",
        "severity": "critical",
        "location": "Hyderabad, Telangana",
        "description": "Heavy rainfall has caused flooding in low-lying areas.",
        "status": "active",
    }


def test_create_disaster():
    response = client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Hyderabad Flood Alert"


def test_get_all_disasters():
    client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    response = client.get("/api/v1/disasters/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_disaster_by_id():
    created = client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    disaster_id = created.json()["id"]

    response = client.get(
        f"/api/v1/disasters/{disaster_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == disaster_id


def test_update_disaster():
    created = client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    disaster_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/disasters/{disaster_id}",
        json={"severity": "high"},
    )

    assert response.status_code == 200
    assert response.json()["severity"] == "high"


def test_delete_disaster():
    created = client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    disaster_id = created.json()["id"]

    response = client.delete(
        f"/api/v1/disasters/{disaster_id}"
    )

    assert response.status_code == 200

    check = client.get(
        f"/api/v1/disasters/{disaster_id}"
    )

    assert check.status_code == 404


def test_get_nonexistent_disaster():
    response = client.get("/api/v1/disasters/9999")

    assert response.status_code == 404

def test_filter_by_disaster_type():
    client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    response = client.get(
        "/api/v1/disasters/?disaster_type=flood"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["disaster_type"] == "flood"


def test_filter_by_severity():
    client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    response = client.get(
        "/api/v1/disasters/?severity=critical"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["severity"] == "critical"


def test_filter_by_status():
    client.post(
        "/api/v1/disasters/",
        json=sample_disaster(),
    )

    response = client.get(
        "/api/v1/disasters/?status=active"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "active"
