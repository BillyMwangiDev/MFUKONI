"""
Tests for utility functions and decorators.
"""

import pytest
from mfukoni_web.tracker.utils import (
    sanitize_sql_string,
    format_currency,
    parse_date,
    validate_input_types,
    handle_db_errors,
)
from my_rdbms.exceptions import DatabaseError


def test_sanitize_sql_string():
    """Test SQL string sanitization."""
    # Test normal string
    assert sanitize_sql_string("test") == "test"

    # Test string with single quote
    assert sanitize_sql_string("test'value") == "test''value"

    # Test string with multiple quotes
    assert sanitize_sql_string("test'value'here") == "test''value''here"

    # Test empty string
    assert sanitize_sql_string("") == ""

    # Test non-string input
    assert sanitize_sql_string(123) == "123"


def test_format_currency():
    """Test currency formatting."""
    assert format_currency(1000.50) == "KES 1,000.50"
    assert format_currency(0) == "KES 0.00"
    assert format_currency(1234567.89) == "KES 1,234,567.89"


def test_parse_date():
    """Test date parsing."""
    # Valid date
    assert parse_date("2026-01-15") == "2026-01-15"

    # Invalid date format
    with pytest.raises(ValueError):
        parse_date("01/15/2026")

    # Invalid date
    with pytest.raises(ValueError):
        parse_date("2026-13-45")


def test_validate_input_types():
    """Test input type validation decorator."""

    @validate_input_types(x=int, y=float)
    def test_func(x, y, z):
        return str(x + y) + z  # x and y are validated, z is not

    # Valid types
    assert test_func(1, 2.0, "test") == "3.0test"  # z is not validated

    # Invalid types
    with pytest.raises(TypeError):
        test_func("1", 2.0, "test")

    with pytest.raises(TypeError):
        test_func(1, "2.0", "test")


def test_handle_db_errors():
    """Test database error handling decorator."""

    @handle_db_errors
    def success_func():
        return "success"

    @handle_db_errors
    def error_func():
        raise DatabaseError("Test error")

    # Success case
    assert success_func() == "success"

    # Error case
    with pytest.raises(DatabaseError):
        error_func()
