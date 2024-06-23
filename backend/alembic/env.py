# -- Pure Python Imports -- #
import typing
from logging.config import fileConfig
# -- Backend Requirements Imports -- #
from sqlalchemy import (
    engine_from_config,
    pool,
    schema,
    MetaData,
)
from alembic import context
# -- Backend Package Imports -- #
from src.core import (
    get_database_url_from_settings,
    DatabaseSchemas,
)
# This import from api.models is instead required to include the API models in the migration environment.
from src.api.models import *

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the main option of the config object to the current database URL.
config.set_main_option("sqlalchemy.url", get_database_url_from_settings())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(
        config.config_file_name,
        disable_existing_loggers=False,
    )

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
backend_metadata = SqlAlchemyBase.metadata
target_metadata = MetaData()


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

schemas_to_include: typing.List[str] = [
    None,  # None is the "public" schema
    DatabaseSchemas.data_entry.value,
    DatabaseSchemas.presentation.value,
]

# Add tables to the target metadata
for table in backend_metadata.tables.values():
    if table.schema in schemas_to_include:
        table.to_metadata(target_metadata)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        include_schemas=True,
        dialect_opts={"paramstyle": "named"},
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        schemas_to_create_if_not_exist: typing.List[str] = [s for s in schemas_to_include if s]
        for stc in schemas_to_create_if_not_exist:
            if not connection.dialect.has_schema(connection, stc):
                connection.execute(schema.CreateSchema(stc))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
            transaction_per_migration=True,
        )

        with context.begin_transaction():
            context.run_migrations()

        connection.commit()
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
