from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from ..config import settings

"""A scoped_session is constructed by calling it, passing it a factory which can create new Session objects. A factory is just something that produces a new object when called, and in the case of Session, the most common factory is the sessionmaker, introduced earlier in this section."""

# Production Database URL
DATABASE_URL = f"mysql+pymysql://root:{settings.mysql_root_password}@mysql_db:3306/{settings.mysql_database}"

# Test Database URL
TEST_DATABASE_URL = settings.test_database_url

# Create the engine
engine = create_engine(DATABASE_URL)
test_engine = create_engine(TEST_DATABASE_URL)

# Create session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Scoped sessions for thread safety
session = scoped_session(SessionLocal)
session_test = scoped_session(TestSessionLocal)

# Create all tables
Base.metadata.create_all(bind=test_engine)


def get_db():
    database = session()
    try:
        yield database
    finally:
        database.close()
