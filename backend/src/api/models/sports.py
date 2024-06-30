# -- Pure Python Imports -- #
import datetime
import typing
# -- Backend Requirements Imports -- #
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Float,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
    text,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
)
from sqlalchemy.dialects.postgresql import JSONB
# -- Backend Package Imports -- #
from src.core import DatabaseSchemas
from src.api.models.base import (
    SqlAlchemyBase,
    PydanticBaseModel,
)
from src.api.models.users import (
    User,
    UserPydanticSchema,
)

__all__ = [
    "Sport",
    "SportCreatePydanticSchema",
    "SportPydanticSchema",
    "SportActivity",
    "SportActivityCreatePydanticSchema",
    "SportActivityPydanticSchema",
    "SportActivityWithSportAndUserPydanticSchema",
    "SportWithActivitiesPydanticSchema",
    "UserPydanticSchemaWithSportActivities",
]


# -- ORM Models -- #

class Sport(SqlAlchemyBase):
    """
    SQLAlchemy ORM model for the 'data_entry.sports' table.
    """

    __tablename__ = "sports"
    __table_args__ = {
        "schema": DatabaseSchemas.data_entry.value,
    }

    id: Column = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
    )
    name: Column = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    kcal_per_hour: Column = Column(
        Float,
        nullable=True,
    )
    # Custom properties for the sport (e.g. km_travelled, height_difference, reps, etc.).
    custom_properties: Column = Column(
        JSONB,
        nullable=True,
    )

    # Relationships
    sport_activities: Mapped["SportActivity"] = relationship(
        back_populates="sport",
        lazy="noload",
    )


class SportActivity(SqlAlchemyBase):
    """
    SQLAlchemy ORM model for the 'data_entry.sport_activities' table.
    This table will be partitioned by 'start_time' (yearly).
    """

    __tablename__ = "sport_activities"
    __table_args__ = (
        PrimaryKeyConstraint(
            "id_sport",
            "id_user",
            "start_time",
            name="sport_activities_pkey",
        ),
        {
            "schema": DatabaseSchemas.data_entry.value,
            "postgresql_partition_by": "RANGE (start_time)",
        },
    )

    id: Column = Column(
        Integer,
        index=True,
        autoincrement=True,
        nullable=False,
        server_default=text(f"nextval('{DatabaseSchemas.data_entry.value}.sport_activities_id_seq'::regclass)"),
    )
    id_sport: Column = Column(
        Integer,
        ForeignKey(
            Sport.id,
            ondelete="cascade",
        ),
        nullable=False,
    )
    id_user: Column = Column(
        Integer,
        ForeignKey(
            User.id,
            ondelete="cascade",
        ),
        nullable=False,
    )
    start_time: Column = Column(
        DateTime,
        nullable=False,
    )
    end_time: Column = Column(
        DateTime,
        nullable=False,
    )
    # Keep track of costs for the specific sport activity.
    cost: Column = Column(
        Float,
        nullable=True,
    )
    # Custom properties for the sport activity (mapped with 'sports' custom properties).
    custom_properties: Column = Column(
        JSONB,
        nullable=True,
    )

    # Relationships
    sport: Mapped["Sport"] = relationship(
        back_populates="sport_activities",
        lazy="noload",
        uselist=False,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sport_activities",
        lazy="noload",
        uselist=False,
    )


# -- Pydantic Models -- #

class SportCreatePydanticSchema(PydanticBaseModel):
    name: str
    kcal_per_hour: typing.Optional[float]
    custom_properties: typing.Optional[
        typing.Dict[
            str,
            typing.Literal["int", "float", "str", "bool"],
        ]
    ]


class SportPydanticSchema(SportCreatePydanticSchema):
    id: int


class SportActivityCreatePydanticSchema(PydanticBaseModel):
    id_sport: int
    id_user: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    cost: typing.Optional[float]
    custom_properties: typing.Optional[typing.Dict[str, typing.Any]]


class SportActivityPydanticSchema(SportActivityCreatePydanticSchema):
    id: int


class SportActivityWithSportAndUserPydanticSchema(SportActivityPydanticSchema):
    sport: SportPydanticSchema
    user: UserPydanticSchema


class SportWithActivitiesPydanticSchema(SportPydanticSchema):
    sport_activities: typing.List[SportActivityPydanticSchema]


class UserPydanticSchemaWithSportActivities(UserPydanticSchema):
    sport_activities: typing.List[SportActivityPydanticSchema]
