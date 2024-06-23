# -- Pure Python Imports -- #
import typing
# -- Backend Requirements Imports -- #
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

# -- Backend Package Imports -- #

__all__ = [
    "SqlAlchemyBase",
    "PydanticBaseModel",
]

# This is the base class for all SQLAlchemy ORM models.
SqlAlchemyBase: typing.Type[DeclarativeBase] = declarative_base()


class PydanticBaseModel(BaseModel):
    """
    Base class for Pydantic models used in API requests and responses.
    """

    class Config:
        from_attributes: bool = True
        validate_assignment: bool = True
