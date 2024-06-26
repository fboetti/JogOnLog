# -- Pure Python Imports -- #
import typing
# -- Backend Requirements Imports -- #
from sqlalchemy.orm import Session
# -- Backend Package Imports -- #
from src.api.models.base import (
    PydanticBaseModel,
    SqlAlchemyBase,
)

__all__ = [
    "create_model_db",
]


def create_model_db(
        session: Session,
        object_to_create: typing.Type[PydanticBaseModel],
        orm_model: typing.Type[SqlAlchemyBase],
        object_to_return_schema: typing.Type[PydanticBaseModel],
) -> PydanticBaseModel:
    """
    Creates a new instance of the given model in the database and returns the instance.
    """
    orm_instance: orm_model = orm_model(**object_to_create.dict())
    session.add(orm_instance)

    # Commit the session to the database and take the id of the object created before returning it.
    session.commit()
    session.refresh(orm_instance)

    return object_to_return_schema.from_orm(orm_instance)
