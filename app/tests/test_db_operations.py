from typing import Generator
from sqlalchemy.orm import Session
from ..db.models import Base, DBLead
from ..db.connection import session_test, test_engine
from ..helpers.repositories import LeadRepository
import pytest


@pytest.fixture(scope="function")
def setup_database() -> Generator[Session, None, None]:
    # create table in db
    Base.metadata.create_all(bind=test_engine)

    try:
        yield test_engine

    finally:
        # Drop all tables after tests are done
        Base.metadata.drop_all(bind=test_engine)
        session_test.remove()


@pytest.fixture(scope="function")
def db_session(setup_database: Session) -> Generator[Session, None, None]:
    """Yield a new database session for a test."""
    connection = setup_database.connect()
    transaction = connection.begin()
    session = session_test(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# TESTS
def test_create_lead(db_session):
    lead_db = LeadRepository(db_session)
    lead_data = DBLead(
        nombre="Lionel",
        apellido="Messi",
        email="lionel.messi@example.com",
        direccion="Calle nro",
        tel=12345678,
    )
    new_lead = lead_db.create_db_lead(lead_data)
    assert new_lead.nombre == "Lionel"
    assert new_lead.apellido == "Messi"


def test_get_lead_by_id(db_session):
    lead_db = LeadRepository(db_session)
    lead_data = DBLead(
        nombre="Lionel",
        apellido="Messi",
        email="lionel.messi@example.com",
        direccion="Calle nro",
        tel=12345678,
    )
    new_lead = lead_db.create_db_lead(lead_data)
    lead = lead_db.read_db_lead(new_lead.lead_id)
    assert lead is not None
    assert lead.nombre == "Lionel"


def test_get_all_leads(db_session):
    lead_db = LeadRepository(db_session)

    lead_data1 = DBLead(
        nombre="Lionel",
        apellido="Messi",
        email="lionel.messi@example.com",
        direccion="Calle nro",
        tel=12345678,
    )
    lead_data2 = DBLead(
        nombre="Lautaro",
        apellido="Martinez",
        email="toro_martinez@example.com",
        direccion="Calle nro",
        tel=12345678,
    )
    lead_db.create_db_lead(lead_data1)
    lead_db.create_db_lead(lead_data2)
    leads = lead_db.read_all_db_leads(limit=10, offset=0)
    assert len(leads) == 2
    assert any(lead.nombre == "Lionel" for lead in leads)
    assert any(lead.nombre == "Lautaro" for lead in leads)
