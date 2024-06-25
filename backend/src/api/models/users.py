# -- Pure Python Imports -- #
import enum
import typing
# -- Backend Requirements Imports -- #
from sqlalchemy import (
    Boolean,
    Column,
    Enum as SqlAlchemyEnum,
    Integer,
    String,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
)
# -- Backend Package Imports -- #
from src.core import DatabaseSchemas
from src.api.models.base import (
    SqlAlchemyBase,
    PydanticBaseModel,
)

__all__ = [
    "User",
    "UserGender",
    "UserPydanticSchema",
]


# -- ORM Models -- #

class UserGender(enum.Enum):
    male: str = "male"
    female: str = "female"
    other: str = "other"


class User(SqlAlchemyBase):
    """
    Users of the application.
    TODO: introduce roles and authentication mechanisms.
    """

    __tablename__ = "users"
    __table_args__ = {
        "schema": DatabaseSchemas.data_entry.value,
    }

    id: Column = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    first_name: Column = Column(
        String,
        nullable=True,
    )
    last_name: Column = Column(
        String,
        nullable=True,
    )
    gender: Column = Column(
        SqlAlchemyEnum(UserGender),
        nullable=True,
    )
    birth_year: Column = Column(
        Integer,
        nullable=True,
    )
    email: Column = Column(
        String,
        unique=True,
        nullable=False,
    )
    hashed_password: Column = Column(
        String,
        nullable=True,
    )
    banned_from_webapp: Column = Column(
        Boolean,
        server_default="False",
    )

    # Relationships
    sport_activities: Mapped["User"] = relationship(
        "SportActivity",
        back_populates="user",
        lazy="noload",
    )


# -- Pydantic Models -- #

class UserPydanticSchema(PydanticBaseModel):
    id: int
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]
    gender: typing.Optional[UserGender]
    birth_year: typing.Optional[int]
    email: str
    banned_from_webapp: bool
