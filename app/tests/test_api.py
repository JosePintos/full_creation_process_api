from typing import Generator
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from ..main import app
from ..db.connection import get_db, test_engine, session_test
from ..db.models import Base
import pytest
import logging

logger = logging.getLogger(__name__)


# Setup in-memory sqlite db
# DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# override dependency in app fastapi
def override_get_db():
    try:
        db = session_test()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Setup test client
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown() -> Generator[Session, None, None]:
    # create table in db
    Base.metadata.create_all(bind=test_engine)
    # create session
    session = session_test()
    try:
        yield session
    finally:
        # Drop all tables after tests are done
        Base.metadata.drop_all(bind=test_engine)
        # Remove the session to ensure it's properly closed
        session_test.remove()


INPUT = {
    "nombre": "Lionel",
    "apellido": "Messi",
    "email": "lionel.messi@example.com",
    "direccion": "Calle nro",
    "tel": 12345678,
    "cursados": [
        {
            "año_cursado": 2024,
            "carrera": {"nombre": "Engineering"},
            "universidad": "University A",
            "inscripciones": [
                {"materia": {"nombre": "Mathematics"}, "veces_cursada": 1},
                {"materia": {"nombre": "Cienciaasasds"}, "veces_cursada": 2},
            ],
        }
    ],
}


# Test cases
def test_get_all_leads():
    # first create lead
    response = client.post("/leads", json=INPUT)
    assert response.status_code == 200
    data = response.json()

    response = client.get("/leads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_one_lead():
    # first create lead
    response = client.post("/leads", json=INPUT)
    assert response.status_code == 200
    data = response.json()
    lead_id = data["lead_id"]

    response = client.get(f"/leads/{lead_id}")
    assert response.status_code == 200
    lead = response.json()
    assert lead["nombre"] == "Lionel"
    assert lead["apellido"] == "Messi"


def test_create_lead():
    response = client.post("/leads", json=INPUT)
    assert response.status_code == 200

    lead = response.json()
    assert len(lead) == 1
    assert "lead_id" in lead


def test_api_pagination():
    # first create lead in case there's none
    response = client.post("/leads", json=INPUT)
    assert response.status_code == 200

    response = client.get("/leads")
    total_leads = len(response.json())

    response = client.get("/leads", params={"limit": 1, "offset": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

    response = client.get(
        "/leads", params={"limit": total_leads, "offset": total_leads}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_lead_missing_fields():
    response = client.post(
        "/leads",
        json={
            "nombre": "Jane",  # Missing 'apellido', 'email', 'direccion', 'tel', 'cursados'
        },
    )
    assert response.status_code == 422  # Unprocessable Entity


def test_create_lead_empty_cursados():
    response = client.post(
        "/leads",
        json={
            "nombre": "Jane",
            "apellido": "Doe",
            "email": "jane.doe@example.com",
            "direccion": "456 Main St",
            "tel": 5556678,
            "cursados": [],
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "lead_id" in response.json()


def test_get_nonexistent_lead():
    response = client.get("/leads/9999")
    assert response.status_code == 404  # Not Found
    assert response.json()["detail"] == "Lead with id 9999 not found."


def test_invalid_pagination_params():
    response = client.get("/leads", params={"limit": -1, "offset": 0})
    assert response.status_code == 400  # Unprocessable Entity
    assert response.json()["detail"] == "Illegal limit/offset value. Only numbers >= 0."

    response = client.get("/leads", params={"limit": 1, "offset": -1})
    assert response.status_code == 400  # Unprocessable Entity
    assert response.json()["detail"] == "Illegal limit/offset value. Only numbers >= 0."
