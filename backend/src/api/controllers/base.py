# -- Pure Python Imports -- #
import enum
import types
import typing
# -- Backend Requirements Imports -- #
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import (
    Session,
)
# -- Backend Package Imports -- #
from src.api.models.base import (
    SqlAlchemyBase,
    PydanticBaseModel,
)
from src.api.services import base as base_service

__all__ = [
    "create_standard_controller",
    "HttpMethods",
]


class HttpMethods(enum.Enum):
    """
    Enum for the HTTP methods.
    """
    GET: str = "GET"
    POST: str = "POST"
    PUT: str = "PUT"
    DELETE: str = "DELETE"


def create_standard_controller(
        prefix: str,
        get_session: typing.Callable[[], typing.Generator],
        sqlalchemy_model: typing.Type[SqlAlchemyBase],
        pydantic_model: typing.Type[PydanticBaseModel],
        tag: typing.Optional[typing.List[str]] = None,
        pydantic_create_model: typing.Optional[typing.Type[PydanticBaseModel]] = None,
        methods_to_expose: typing.Optional[typing.List[HttpMethods]] = None,
        service_module: types.ModuleType = base_service,
        dependencies: typing.Optional[typing.List[typing.Callable]] = None,
) -> APIRouter:
    """
    Creates a standard CRUD controller for the given model.

    :param prefix: The `prefix` param is a string that represents the prefix of the controller. The first character
        is usually a slash.
    :param get_session: The `get_session` param is a function that returns a SQLAlchemy session.
    :param sqlalchemy_model: The `sqlalchemy_model` param is a class that represents the SQLAlchemy model.
    :param pydantic_model: The `pydantic_model` param is a class that represents the Pydantic model.
    :param tag: The `tag` param is a list of strings that represents the tags of the controller.
    :param pydantic_create_model: The `pydantic_create_model` param is a class that represents the Pydantic model
        used by the controller for the creation of new instances.
    :param methods_to_expose: The `methods_to_expose` param is a list of `Methods` enum representing the HTTP methods
        to be exposed; if not specified, none of the enumerable methods will be exposed.
    :param service_module: The `service_module` param is a module that represents the service of the controller.
    :param dependencies: The `dependencies` param is a list of functions that represents the dependencies of the
        controller (like security token check for example, coming soon).
    """
    controller: APIRouter = APIRouter(
        prefix=prefix,
        tags=tag if tag else [prefix[1:].capitalize()],     # Remove slash from prefix and capitalize the first letter.
        dependencies=dependencies,
    )

    if HttpMethods.POST in methods_to_expose:
        @controller.post(
            "/",
            response_model=pydantic_model,
            dependencies=dependencies,
        )
        def post(
                instance: pydantic_create_model,
                session: Session = Depends(get_session),
        ) -> pydantic_model:
            """
            Creates a new instance on database of the ORM model.
            """
            return service_module.create_model_db(
                session=session,
                object_to_create=instance,
                orm_model=sqlalchemy_model,
                object_to_return_schema=pydantic_model,
            )

    return controller
