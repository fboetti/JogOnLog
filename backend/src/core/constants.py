# -- Pure Python Imports -- #
import enum

__all__ = [
    "DatabaseSchemas",
]


class DatabaseSchemas(enum.Enum):
    """
    Enumerates the available database schemas for the JogOnLog application.
    """
    data_entry: str = "data_entry"
    presentation: str = "presentation"
