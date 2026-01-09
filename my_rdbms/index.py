"""
Index module for fast lookups.
"""

from typing import Dict, Any, List, Optional, Set
from collections import defaultdict


class HashIndex:
    """Hash-based index for fast O(1) lookups."""

    def __init__(self, column_name: str):
        """
        Initialize a hash index.
        
        Args:
            column_name: Name of the column to index
        """
        self.column_name = column_name
        self.index: Dict[Any, Set[int]] = defaultdict(set)

    def build(self, rows: List[Dict[str, Any]]) -> None:
        """
        Build index from rows.
        
        Args:
            rows: List of row dictionaries
        """
        self.index.clear()
        for idx, row in enumerate(rows):
            value = row.get(self.column_name)
            if value is not None:
                self.index[value].add(idx)

    def add(self, value: Any, row_index: int) -> None:
        """
        Add a value to the index.
        
        Args:
            value: The indexed value
            row_index: Index of the row
        """
        if value is not None:
            self.index[value].add(row_index)

    def remove(self, value: Any, row_index: int) -> None:
        """
        Remove a value from the index.
        
        Args:
            value: The indexed value
            row_index: Index of the row
        """
        if value in self.index:
            self.index[value].discard(row_index)
            if not self.index[value]:
                del self.index[value]

    def update(self, old_value: Any, new_value: Any, row_index: int) -> None:
        """
        Update index when a value changes.
        
        Args:
            old_value: The old value
            new_value: The new value
            row_index: Index of the row
        """
        self.remove(old_value, row_index)
        self.add(new_value, row_index)

    def find(self, value: Any) -> Set[int]:
        """
        Find row indices matching a value.
        
        Args:
            value: The value to search for
            
        Returns:
            Set of row indices
        """
        return self.index.get(value, set())

    def clear(self) -> None:
        """Clear the index."""
        self.index.clear()


class IndexManager:
    """Manages indexes for a table."""

    def __init__(self):
        """Initialize index manager."""
        self.indexes: Dict[str, HashIndex] = {}

    def create_index(self, column_name: str) -> HashIndex:
        """
        Create a new index on a column.
        
        Args:
            column_name: Name of the column to index
            
        Returns:
            The created HashIndex
        """
        if column_name not in self.indexes:
            self.indexes[column_name] = HashIndex(column_name)
        return self.indexes[column_name]

    def get_index(self, column_name: str) -> Optional[HashIndex]:
        """
        Get an index for a column.
        
        Args:
            column_name: Name of the column
            
        Returns:
            HashIndex if exists, None otherwise
        """
        return self.indexes.get(column_name)

    def has_index(self, column_name: str) -> bool:
        """Check if an index exists for a column."""
        return column_name in self.indexes

    def rebuild_all(self, rows: List[Dict[str, Any]]) -> None:
        """
        Rebuild all indexes from rows.
        
        Args:
            rows: List of row dictionaries
        """
        for index in self.indexes.values():
            index.build(rows)

    def clear_all(self) -> None:
        """Clear all indexes."""
        for index in self.indexes.values():
            index.clear()
