"""
Main database module - entry point for all database operations.
"""

from typing import Dict, Any, List, Optional
from my_rdbms.table import Table
from my_rdbms.parser import SQLParser
from my_rdbms.executor import QueryExecutor
from my_rdbms.storage import Storage
from my_rdbms.exceptions import DatabaseError, PrimaryKeyError, UniqueConstraintError, TableError


class Database:
    """Main database class that manages tables and executes queries."""

    def __init__(self, db_path: str = "data/mfukoni.db"):
        """
        Initialize database.

        Args:
            db_path: Path to database directory
        """
        self.db_path = db_path
        self.storage = Storage(db_path)
        self.tables: Dict[str, Table] = {}
        self.parser = SQLParser()
        self.executor = None  # Will be set after loading tables
        self._load_tables()

    def _load_tables(self) -> None:
        """Load all tables from storage."""
        table_names = self.storage.list_tables()
        for table_name in table_names:
            schema, rows = self.storage.load_table(table_name)
            if schema:
                table = Table(table_name, schema)
                if rows:
                    table.load_rows(rows)
                self.tables[table_name] = table

        # Initialize executor with loaded tables
        self.executor = QueryExecutor(self.tables)

    def execute(self, sql: str) -> Any:
        """
        Execute a SQL statement.

        Args:
            sql: SQL statement string

        Returns:
            Query result (varies by command type)

        Raises:
            PrimaryKeyError: If PRIMARY KEY constraint is violated
            UniqueConstraintError: If UNIQUE constraint is violated
            TableError: If table operation fails
            DatabaseError: For other database errors
        """
        # Parse SQL - let ParseError bubble up
        parsed = self.parser.parse(sql)

        # Execute query - let constraint errors (PrimaryKeyError, UniqueConstraintError, TableError) bubble up
        result = self.executor.execute(parsed)

        # Auto-commit for data modification operations (only if execution succeeded)
        if parsed.get("command") in ("INSERT", "UPDATE", "DELETE", "CREATE_TABLE"):
            try:
                self.commit()
            except Exception as e:
                # Wrap commit errors
                raise DatabaseError(f"Error committing changes: {str(e)}")

        return result

    def commit(self) -> None:
        """Save all tables to disk."""
        for table_name, table in self.tables.items():
            schema = table.get_schema()
            rows = table.rows
            self.storage.save_table(table_name, schema, rows)

    def get_table(self, table_name: str) -> Optional[Table]:
        """Get a table by name."""
        return self.tables.get(table_name)

    def list_tables(self) -> List[str]:
        """List all table names."""
        return list(self.tables.keys())

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        return table_name in self.tables
