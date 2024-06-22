# -- Backend Requirements Imports -- #
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# -- Backend Package Imports -- #
from src.core import (
    BackendSettings,
    get_settings,
)

backend_settings: BackendSettings = get_settings()

engine = create_engine(backend_settings.get_database_connection_string())

SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
