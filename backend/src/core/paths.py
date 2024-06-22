# -- Pure Python Imports -- #
import os


__all__ = [
    "alembic_directory_path",
    "environment_variables_path",
]


backend_directory_path: os.path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
alembic_directory_path: os.path = os.path.join(backend_directory_path, "alembic")
environment_variables_path: os.path = os.path.join(backend_directory_path, "env_variables")
