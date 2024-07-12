from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import settings

DATABASE_PW = settings.mysql_root_password
DATABASE_NAME = settings.mysql_database
DATABASE_URL = f"mysql+pymysql://root:{DATABASE_PW}@localhost:3306/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
