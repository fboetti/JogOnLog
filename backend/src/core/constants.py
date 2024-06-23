# -- Pure Python Imports -- #
import enum

__all__ = [
    "DatabaseSchemas",
]


class DatabaseSchemas(enum.Enum):
    """
    Enumerates the available database schemas for the JogOnLog application.
    """
    DATA_ENTRY: str = "data_entry"
    PRESENTATION: str = "presentation"
