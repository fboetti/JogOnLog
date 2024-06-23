# -- Pure Python Imports -- #
import typing
# -- Backend Requirements Imports -- #
from fastapi import Depends
from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
# -- Backend Package Imports -- #
from src.core import (
    get_settings,
    BackendSettings,
)

__all__ = [
    "get_database_url_from_settings",
    "get_database_session_from_settings",
]


# -- Private Classes & Methods -- #

def _get_engine_from_database_url(
        database_url: str,
) -> Engine:
    return create_engine(
        url=database_url,
    )


def _get_session_maker_from_engine(
        engine: Engine,
) -> sessionmaker:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


# -- Exposed Methods -- #


def get_database_url_from_settings() -> str:
    """
    Function to get the database URL from the backend settings.
    FIXME: Check why dependency injection doesn't work here.
    """
    backend_settings: BackendSettings = get_settings()
    return backend_settings.get_database_connection_string()


def get_database_session_from_settings(
        backend_settings: BackendSettings = Depends(get_settings),
) -> typing.Generator:
    session_maker: sessionmaker = _get_session_maker_from_engine(
        engine=_get_engine_from_database_url(
            database_url=backend_settings.get_database_connection_string(),
        ),
    )
    session: Session = session_maker()
    try:
        yield session
    finally:
        session.close()
