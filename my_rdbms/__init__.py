"""
Mfukoni Custom RDBMS
A simple relational database management system with SQL support.
"""

__version__ = "1.0.0"

from my_rdbms.database import Database
from my_rdbms.exceptions import (
    DatabaseError,
    TableError,
    ConstraintError,
    PrimaryKeyError,
    UniqueConstraintError,
    ParseError,
)

__all__ = [
    "Database",
    "DatabaseError",
    "TableError",
    "ConstraintError",
    "PrimaryKeyError",
    "UniqueConstraintError",
    "ParseError",
]
