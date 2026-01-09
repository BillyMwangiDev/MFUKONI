"""
Storage module for persisting database to JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from my_rdbms.exceptions import StorageError


class Storage:
    """Handles saving and loading database tables from JSON files."""

    def __init__(self, db_path: str):
        """
        Initialize storage with database path.
        
        Args:
            db_path: Path to database directory (e.g., 'data/mfukoni.db')
        """
        self.db_path = Path(db_path)
        # Create both parent directory and the database directory itself
        self.db_path.mkdir(parents=True, exist_ok=True)

    def save_table(self, table_name: str, schema: Dict[str, Any], rows: List[Dict[str, Any]]) -> None:
        """
        Save a table to a JSON file.
        
        Args:
            table_name: Name of the table
            schema: Table schema definition
            rows: List of row dictionaries
        """
        try:
            table_file = self.db_path / f"{table_name}.json"
            data = {
                "schema": schema,
                "rows": rows
            }
            with open(table_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise StorageError(f"Failed to save table {table_name}: {str(e)}")

    def load_table(self, table_name: str):
        """
        Load a table from a JSON file.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Tuple of (schema, rows)
        """
        try:
            table_file = self.db_path / f"{table_name}.json"
            if not table_file.exists():
                return None, None
            
            with open(table_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("schema"), data.get("rows", [])
        except Exception as e:
            raise StorageError(f"Failed to load table {table_name}: {str(e)}")

    def table_exists(self, table_name: str) -> bool:
        """Check if a table file exists."""
        table_file = self.db_path / f"{table_name}.json"
        return table_file.exists()

    def delete_table(self, table_name: str) -> None:
        """Delete a table file."""
        try:
            table_file = self.db_path / f"{table_name}.json"
            if table_file.exists():
                table_file.unlink()
        except Exception as e:
            raise StorageError(f"Failed to delete table {table_name}: {str(e)}")

    def list_tables(self) -> List[str]:
        """List all table files in the database directory."""
        if not self.db_path.exists():
            return []
        
        tables = []
        for file in self.db_path.glob("*.json"):
            tables.append(file.stem)
        return tables
