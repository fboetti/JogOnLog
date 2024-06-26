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
    User,
    UserPydanticSchema,
    UserCreatePydanticSchema,
)

__all__ = [
    "users_controller",
]


users_controller: APIRouter = create_standard_controller(
    prefix="/users",
    get_session=get_database_session_from_settings,
    sqlalchemy_model=User,
    pydantic_model=UserPydanticSchema,
    pydantic_create_model=UserCreatePydanticSchema,
    methods_to_expose=[
        HttpMethods.POST,
    ],
)
