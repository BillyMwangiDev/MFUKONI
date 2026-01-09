"""
Custom exceptions for the RDBMS.
"""


class DatabaseError(Exception):
    """Base exception for all database errors."""
    pass


class TableError(DatabaseError):
    """Raised when table operations fail."""
    pass


class ConstraintError(DatabaseError):
    """Base exception for constraint violations."""
    pass


class PrimaryKeyError(ConstraintError):
    """Raised when PRIMARY KEY constraint is violated."""
    pass


class UniqueConstraintError(ConstraintError):
    """Raised when UNIQUE constraint is violated."""
    pass


class ParseError(DatabaseError):
    """Raised when SQL parsing fails."""
    pass


class StorageError(DatabaseError):
    """Raised when storage operations fail."""
    pass
