"""
Tests for SQL parser.
"""

import pytest
from my_rdbms.parser import SQLParser
from my_rdbms.exceptions import ParseError


def test_parse_create_table():
    """Test CREATE TABLE parsing."""
    parser = SQLParser()
    result = parser.parse("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")

    assert result["command"] == "CREATE_TABLE"
    assert result["table_name"] == "users"
    assert "id" in result["columns"]
    assert "name" in result["columns"]
    assert result["primary_key"] == "id"


def test_parse_insert():
    """Test INSERT parsing."""
    parser = SQLParser()
    result = parser.parse("INSERT INTO users VALUES (1, 'Alice')")

    assert result["command"] == "INSERT"
    assert result["table_name"] == "users"
    assert result["values"] == [1, "Alice"]


def test_parse_select():
    """Test SELECT parsing."""
    parser = SQLParser()
    result = parser.parse("SELECT * FROM users WHERE age > 25")

    assert result["command"] == "SELECT"
    assert result["table_name"] == "users"
    assert result["columns"] is None
    assert "age > 25" in result["where"]


def test_parse_update():
    """Test UPDATE parsing."""
    parser = SQLParser()
    result = parser.parse("UPDATE users SET name = 'Bob' WHERE id = 1")

    assert result["command"] == "UPDATE"
    assert result["table_name"] == "users"
    assert result["updates"]["name"] == "Bob"
    assert "id = 1" in result["where"]


def test_parse_delete():
    """Test DELETE parsing."""
    parser = SQLParser()
    result = parser.parse("DELETE FROM users WHERE id = 1")

    assert result["command"] == "DELETE"
    assert result["table_name"] == "users"
    assert "id = 1" in result["where"]
