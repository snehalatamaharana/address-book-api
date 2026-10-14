"""API tests using an in-memory SQLite DB."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


PAYLOAD = {
    "name": "Office", "street": "MG Road", "city": "Bengaluru",
    "country": "India", "postal_code": "560001",
    "latitude": 12.9716, "longitude": 77.5946,
}


def test_create_and_get(client):
    r = client.post("/addresses/", json=PAYLOAD)
    assert r.status_code == 201
    assert client.get(f"/addresses/{r.json()['id']}").json()["city"] == "Bengaluru"


def test_invalid_latitude_rejected(client):
    r = client.post("/addresses/", json={**PAYLOAD, "latitude": 123})
    assert r.status_code == 422


def test_update_and_delete(client):
    addr_id = client.post("/addresses/", json=PAYLOAD).json()["id"]
    assert client.patch(f"/addresses/{addr_id}", json={"city": "Mysuru"}).json()["city"] == "Mysuru"
    assert client.delete(f"/addresses/{addr_id}").status_code == 204
    assert client.get(f"/addresses/{addr_id}").status_code == 404


def test_nearby_search(client):
    client.post("/addresses/", json=PAYLOAD)  # Bengaluru
    client.post("/addresses/", json={**PAYLOAD, "name": "Delhi", "latitude": 28.61, "longitude": 77.20})
    r = client.get("/addresses/nearby", params={"latitude": 12.97, "longitude": 77.59, "distance_km": 20})
    assert [a["name"] for a in r.json()] == ["Office"]