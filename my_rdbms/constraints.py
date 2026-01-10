"""
Constraint validation module.
"""

from typing import Dict, Any, List, Optional
from my_rdbms.exceptions import PrimaryKeyError, UniqueConstraintError


class ConstraintValidator:
    """Validates constraints on table operations."""

    @staticmethod
    def validate_primary_key(
        table_name: str,
        primary_key_col: str,
        new_value: Any,
        existing_rows: List[Dict[str, Any]],
        exclude_row_index: Optional[int] = None
    ) -> None:
        """
        Validate PRIMARY KEY constraint.
        
        Args:
            table_name: Name of the table
            primary_key_col: Name of the primary key column
            new_value: The new primary key value
            existing_rows: Existing rows in the table
            exclude_row_index: Index of row to exclude (for UPDATE operations)
            
        Raises:
            PrimaryKeyError: If primary key already exists
        """
        if new_value is None:
            raise PrimaryKeyError(f"PRIMARY KEY column '{primary_key_col}' cannot be NULL")
        
        for idx, row in enumerate(existing_rows):
            if exclude_row_index is not None and idx == exclude_row_index:
                continue
            if row.get(primary_key_col) == new_value:
                raise PrimaryKeyError(
                    f"PRIMARY KEY violation: value {new_value} already exists in table '{table_name}'"
                )

    @staticmethod
    def validate_unique(
        table_name: str,
        unique_cols: List[str],
        new_row: Dict[str, Any],
        existing_rows: List[Dict[str, Any]],
        exclude_row_index: Optional[int] = None
    ) -> None:
        """
        Validate UNIQUE constraint.
        
        Args:
            table_name: Name of the table
            unique_cols: List of column names with UNIQUE constraint
            new_row: The new row being inserted/updated
            existing_rows: Existing rows in the table
            exclude_row_index: Index of row to exclude (for UPDATE operations)
            
        Raises:
            UniqueConstraintError: If unique constraint is violated
        """
        for col in unique_cols:
            new_value = new_row.get(col)
            if new_value is None:
                continue  # NULL values are allowed in UNIQUE columns
            
            for idx, row in enumerate(existing_rows):
                if exclude_row_index is not None and idx == exclude_row_index:
                    continue
                
                if row.get(col) == new_value:
                    raise UniqueConstraintError(
                        f"UNIQUE constraint violation: value '{new_value}' already exists "
                        f"in column '{col}' of table '{table_name}'"
                    )

    @staticmethod
    def validate_row(
        table_name: str,
        schema: Dict[str, Any],
        new_row: Dict[str, Any],
        existing_rows: List[Dict[str, Any]],
        exclude_row_index: Optional[int] = None
    ) -> None:
        """
        Validate all constraints for a row.
        
        Args:
            table_name: Name of the table
            schema: Table schema
            new_row: The new row being inserted/updated
            existing_rows: Existing rows in the table
            exclude_row_index: Index of row to exclude (for UPDATE operations)
        """
        primary_key = schema.get("primary_key")
        unique_cols = schema.get("unique", [])
        
        # Validate PRIMARY KEY
        if primary_key:
            ConstraintValidator.validate_primary_key(
                table_name, primary_key, new_row.get(primary_key), existing_rows, exclude_row_index
            )
        
        # Validate UNIQUE constraints
        if unique_cols:
            ConstraintValidator.validate_unique(
                table_name, unique_cols, new_row, existing_rows, exclude_row_index
            )
