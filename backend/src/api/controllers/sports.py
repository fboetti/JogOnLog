# -- Backend Requirements Imports -- #
from fastapi import (
    APIRouter,
)
# -- Backend Package Imports -- #
from src.core import (
    get_database_session_from_settings,
)
from src.api.controllers import (
    create_standard_controller,
    HttpMethods,
)
from src.api.models import (
    Sport,
    SportActivity,
    SportCreatePydanticSchema,
    SportPydanticSchema,
    SportActivityCreatePydanticSchema,
    SportActivityPydanticSchema,
)

__all__ = [
    "sports_controller",
    "sports_activities_controller",
]


sports_controller: APIRouter = create_standard_controller(
    prefix="/sports",
    get_session=get_database_session_from_settings,
    sqlalchemy_model=Sport,
    pydantic_model=SportPydanticSchema,
    pydantic_create_model=SportCreatePydanticSchema,
    methods_to_expose=[
        HttpMethods.POST,
    ],
)

sports_activities_controller: APIRouter = create_standard_controller(
    prefix="/sport_activities",
    get_session=get_database_session_from_settings,
    sqlalchemy_model=SportActivity,
    pydantic_model=SportActivityPydanticSchema,
    pydantic_create_model=SportActivityCreatePydanticSchema,
    methods_to_expose=[
        HttpMethods.POST,
    ],
)
