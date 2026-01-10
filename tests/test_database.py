"""
Tests for core database functionality.
"""

import pytest
import os
import shutil
from my_rdbms.database import Database
from my_rdbms.exceptions import DatabaseError, PrimaryKeyError, UniqueConstraintError, TableError


@pytest.fixture
def test_db():
    """Create a test database."""
    db_path = "test_data/test.db"
    os.makedirs("test_data", exist_ok=True)
    db = Database(db_path)
    yield db
    # Cleanup
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")


def test_create_table(test_db):
    """Test table creation."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    assert test_db.table_exists("users")


def test_insert_and_select(test_db):
    """Test INSERT and SELECT operations."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")
    result = test_db.execute("SELECT * FROM users")
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_primary_key_constraint(test_db):
    """Test PRIMARY KEY constraint."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")

    with pytest.raises(PrimaryKeyError):
        test_db.execute("INSERT INTO users VALUES (1, 'Bob')")


def test_unique_constraint(test_db):
    """Test UNIQUE constraint."""
    test_db.execute("CREATE TABLE users (id INT, email VARCHAR UNIQUE)")
    test_db.execute("INSERT INTO users VALUES (1, 'test@test.com')")

    with pytest.raises(UniqueConstraintError):
        test_db.execute("INSERT INTO users VALUES (2, 'test@test.com')")


def test_update(test_db):
    """Test UPDATE operation."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")
    test_db.execute("UPDATE users SET name = 'Bob' WHERE id = 1")
    result = test_db.execute("SELECT * FROM users WHERE id = 1")
    assert result[0]["name"] == "Bob"


def test_delete(test_db):
    """Test DELETE operation."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")
    test_db.execute("DELETE FROM users WHERE id = 1")
    result = test_db.execute("SELECT * FROM users")
    assert len(result) == 0


def test_where_clause(test_db):
    """Test WHERE clause filtering."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR, age INT)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice', 25)")
    test_db.execute("INSERT INTO users VALUES (2, 'Bob', 30)")

    result = test_db.execute("SELECT * FROM users WHERE age > 25")
    assert len(result) == 1
    assert result[0]["name"] == "Bob"


def test_join(test_db):
    """Test JOIN operation."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")
    test_db.execute("INSERT INTO orders VALUES (1, 1, 'Laptop')")

    result = test_db.execute(
        """
        SELECT u.name, o.product 
        FROM users u 
        INNER JOIN orders o ON u.id = o.user_id
    """
    )
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
    assert "product" in result[0] or "o.product" in result[0]


def test_persistence(test_db):
    """Test data persistence."""
    test_db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    test_db.execute("INSERT INTO users VALUES (1, 'Alice')")
    test_db.commit()

    # Create new database instance (should load from disk)
    db2 = Database(test_db.db_path)
    result = db2.execute("SELECT * FROM users")
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
