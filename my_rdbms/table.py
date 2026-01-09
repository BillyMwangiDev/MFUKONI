"""
Table module for managing table data and operations.
"""

from typing import Dict, Any, List, Optional, Callable
from my_rdbms.constraints import ConstraintValidator
from my_rdbms.index import IndexManager
from my_rdbms.exceptions import TableError


class Table:
    """Represents a database table with schema, rows, and operations."""

    def __init__(self, name: str, schema: Dict[str, Any]):
        """
        Initialize a table.
        
        Args:
            name: Table name
            schema: Table schema with columns, types, constraints
        """
        self.name = name
        self.schema = schema
        self.rows: List[Dict[str, Any]] = []
        self.index_manager = IndexManager()
        self._build_indexes()

    def _build_indexes(self) -> None:
        """Build indexes for primary key and unique columns."""
        primary_key = self.schema.get("primary_key")
        if primary_key:
            self.index_manager.create_index(primary_key)
        
        unique_cols = self.schema.get("unique", [])
        for col in unique_cols:
            self.index_manager.create_index(col)
        
        # Rebuild indexes from existing rows
        if self.rows:
            self.index_manager.rebuild_all(self.rows)

    def insert(self, row: Dict[str, Any]) -> None:
        """
        Insert a new row into the table.
        
        Args:
            row: Dictionary with column names as keys
            
        Raises:
            ConstraintError: If constraints are violated
        """
        # Validate constraints
        ConstraintValidator.validate_row(self.name, self.schema, row, self.rows)
        
        # Type conversion
        row = self._convert_types(row)
        
        # Insert row
        self.rows.append(row.copy())
        
        # Update indexes
        self._update_indexes_for_insert(row, len(self.rows) - 1)

    def select(
        self,
        columns: Optional[List[str]] = None,
        where: Optional[Callable[[Dict[str, Any]], bool]] = None
    ) -> List[Dict[str, Any]]:
        """
        Select rows from the table.
        
        Args:
            columns: List of column names to select (None = all)
            where: Filter function
            
        Returns:
            List of matching rows
        """
        results = []
        for row in self.rows:
            if where is None or where(row):
                if columns:
                    filtered_row = {col: row.get(col) for col in columns}
                    results.append(filtered_row)
                else:
                    results.append(row.copy())
        return results

    def update(
        self,
        updates: Dict[str, Any],
        where: Optional[Callable[[Dict[str, Any]], bool]] = None
    ) -> int:
        """
        Update rows in the table.
        
        Args:
            updates: Dictionary of column: value pairs to update
            where: Filter function
            
        Returns:
            Number of rows updated
        """
        count = 0
        for idx, row in enumerate(self.rows):
            if where is None or where(row):
                # Validate constraints before updating
                new_row = row.copy()
                new_row.update(updates)
                ConstraintValidator.validate_row(
                    self.name, self.schema, new_row, self.rows, exclude_row_index=idx
                )
                
                # Update indexes
                for col, new_value in updates.items():
                    old_value = row.get(col)
                    if self.index_manager.has_index(col):
                        self.index_manager.get_index(col).update(old_value, new_value, idx)
                
                # Apply updates
                row.update(updates)
                row = self._convert_types(row)
                count += 1
        
        return count

    def delete(self, where: Optional[Callable[[Dict[str, Any]], bool]] = None) -> int:
        """
        Delete rows from the table.
        
        Args:
            where: Filter function
            
        Returns:
            Number of rows deleted
        """
        # Collect indices to delete (in reverse order to avoid index shifting)
        indices_to_delete = []
        for idx, row in enumerate(self.rows):
            if where is None or where(row):
                indices_to_delete.append(idx)
        
        # Delete in reverse order
        for idx in reversed(indices_to_delete):
            row = self.rows[idx]
            # Remove from indexes
            for col_name in self.schema.get("columns", {}).keys():
                if self.index_manager.has_index(col_name):
                    value = row.get(col_name)
                    self.index_manager.get_index(col_name).remove(value, idx)
            
            del self.rows[idx]
            
            # Rebuild indexes (simpler than updating all indices)
            self.index_manager.rebuild_all(self.rows)
        
        return len(indices_to_delete)

    def _convert_types(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert row values to appropriate types based on schema.
        
        Args:
            row: Row dictionary
            
        Returns:
            Row with converted types
        """
        converted = {}
        columns = self.schema.get("columns", {})
        
        for col, value in row.items():
            if col in columns:
                col_type = columns[col].upper()
                if value is None:
                    converted[col] = None
                elif col_type == "INT":
                    converted[col] = int(value)
                elif col_type == "FLOAT":
                    converted[col] = float(value)
                elif col_type == "BOOLEAN":
                    if isinstance(value, bool):
                        converted[col] = value
                    elif isinstance(value, str):
                        converted[col] = value.lower() in ("true", "1", "yes")
                    else:
                        converted[col] = bool(value)
                elif col_type == "VARCHAR":
                    converted[col] = str(value)
                else:
                    converted[col] = value
            else:
                converted[col] = value
        
        return converted

    def _update_indexes_for_insert(self, row: Dict[str, Any], row_index: int) -> None:
        """Update indexes after inserting a row."""
        for col_name, value in row.items():
            if self.index_manager.has_index(col_name):
                self.index_manager.get_index(col_name).add(value, row_index)

    def get_schema(self) -> Dict[str, Any]:
        """Get the table schema."""
        return self.schema.copy()

    def get_row_count(self) -> int:
        """Get the number of rows in the table."""
        return len(self.rows)

    def load_rows(self, rows: List[Dict[str, Any]]) -> None:
        """
        Load rows into the table (used when loading from storage).
        
        Args:
            rows: List of row dictionaries
        """
        self.rows = rows
        self.index_manager.rebuild_all(self.rows)
