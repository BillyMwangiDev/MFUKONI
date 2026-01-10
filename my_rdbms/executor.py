"""
Query executor module - executes parsed SQL commands.
"""

import operator
from typing import Dict, Any, List, Optional, Callable
from my_rdbms.table import Table
from my_rdbms.exceptions import TableError, ParseError


class QueryExecutor:
    """Executes parsed SQL queries."""

    def __init__(self, tables: Dict[str, Table]):
        """
        Initialize executor with table dictionary.
        
        Args:
            tables: Dictionary of table_name -> Table objects
        """
        self.tables = tables

    def execute(self, parsed_query: Dict[str, Any]) -> Any:
        """
        Execute a parsed query.
        
        Args:
            parsed_query: Parsed query dictionary
            
        Returns:
            Query result (varies by command type)
        """
        command = parsed_query.get("command")
        
        if command == "CREATE_TABLE":
            return self._execute_create_table(parsed_query)
        elif command == "INSERT":
            return self._execute_insert(parsed_query)
        elif command == "SELECT":
            return self._execute_select(parsed_query)
        elif command == "UPDATE":
            return self._execute_update(parsed_query)
        elif command == "DELETE":
            return self._execute_delete(parsed_query)
        else:
            raise ParseError(f"Unknown command: {command}")

    def _execute_create_table(self, query: Dict[str, Any]) -> None:
        """Execute CREATE TABLE command."""
        table_name = query["table_name"]
        if table_name in self.tables:
            raise TableError(f"Table '{table_name}' already exists")
        
        schema = {
            "columns": query["columns"],
            "primary_key": query.get("primary_key"),
            "unique": query.get("unique", [])
        }
        
        table = Table(table_name, schema)
        self.tables[table_name] = table

    def _execute_insert(self, query: Dict[str, Any]) -> None:
        """Execute INSERT command."""
        table_name = query["table_name"]
        table = self._get_table(table_name)
        
        # Get column names from schema
        columns = list(table.schema["columns"].keys())
        values = query["values"]
        
        # Create row dictionary
        row = {}
        for i, col in enumerate(columns):
            if i < len(values):
                # Handle NULL values
                val = values[i]
                if val is None or (isinstance(val, str) and val.upper() == "NULL"):
                    row[col] = None
                else:
                    row[col] = val
            else:
                row[col] = None
        
        table.insert(row)

    def _execute_select(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute SELECT command."""
        table_name = query["table_name"]
        table = self._get_table(table_name)
        
        # Build WHERE function
        where_func = None
        if query.get("where"):
            where_func = self._build_where_function(query["where"], table_name)
        
        # Handle JOIN
        if query.get("join"):
            return self._execute_join(query, table, where_func)
        
        # Regular SELECT
        return table.select(columns=query.get("columns"), where=where_func)

    def _execute_update(self, query: Dict[str, Any]) -> int:
        """Execute UPDATE command."""
        table_name = query["table_name"]
        table = self._get_table(table_name)
        
        updates = query["updates"]
        where_func = None
        if query.get("where"):
            where_func = self._build_where_function(query["where"], table_name)
        
        return table.update(updates, where=where_func)

    def _execute_delete(self, query: Dict[str, Any]) -> int:
        """Execute DELETE command."""
        table_name = query["table_name"]
        table = self._get_table(table_name)
        
        where_func = None
        if query.get("where"):
            where_func = self._build_where_function(query["where"], table_name)
        
        return table.delete(where=where_func)

    def _execute_join(self, query: Dict[str, Any], left_table: Table, where_func: Optional[Callable]) -> List[Dict[str, Any]]:
        """Execute JOIN operation."""
        join_info = query["join"]
        right_table_name = join_info["table"]
        right_table = self._get_table(right_table_name)
        
        # Parse join condition
        left_col = join_info["on"]["left"].split(".")[1]  # table.col -> col
        right_col = join_info["on"]["right"].split(".")[1]
        
        # Get aliases for column prefixing
        left_alias = join_info.get("left_alias")  # Left table alias (e.g., "u")
        right_alias = join_info["alias"]  # Right table alias (e.g., "o")
        
        # Perform INNER JOIN
        results = []
        for left_row in left_table.rows:
            left_value = left_row.get(left_col)
            if left_value is None:
                continue
            
            # Find matching rows in right table
            for right_row in right_table.rows:
                right_value = right_row.get(right_col)
                if left_value == right_value:
                    # Merge rows with proper alias prefixing
                    merged = {}
                    # Prefix left table columns with alias if provided
                    if left_alias:
                        merged.update({f"{left_alias}.{k}": v for k, v in left_row.items()})
                    else:
                        merged.update(left_row)
                    
                    # Prefix right table columns with alias
                    merged.update({f"{right_alias}.{k}": v for k, v in right_row.items()})
                    
                    # Apply WHERE clause if present
                    if where_func is None or where_func(merged):
                        # Select columns - handle both aliased (u.name) and non-aliased (name) column names
                        if query.get("columns"):
                            filtered = {}
                            for col in query["columns"]:
                                col = col.strip()
                                # Try aliased name first (e.g., "u.name")
                                if col in merged:
                                    filtered[col] = merged[col]
                                elif "." in col:
                                    # Column has alias (e.g., "u.name")
                                    alias_part, col_part = col.split(".", 1)
                                    # Check if we have the aliased version
                                    if col in merged:
                                        filtered[col] = merged[col]
                                    else:
                                        # Fallback: find value from appropriate table based on alias
                                        if alias_part == left_alias and col_part in left_row:
                                            filtered[col] = left_row[col_part]
                                        elif alias_part == right_alias and col_part in right_row:
                                            filtered[col] = right_row[col_part]
                                else:
                                    # Non-aliased column name - try to find in either table
                                    # First try left table, then right table
                                    if col in left_row:
                                        filtered[col] = left_row[col]
                                    elif col in right_row:
                                        filtered[col] = right_row[col]
                            results.append(filtered)
                        else:
                            results.append(merged)
        
        return results

    def _build_where_function(self, where_clause: str, table_name: str) -> Callable[[Dict[str, Any]], bool]:
        """
        Build a WHERE function from a WHERE clause string.
        
        Args:
            where_clause: WHERE clause string (e.g., "amount > 100")
            table_name: Name of the table
            
        Returns:
            Function that returns True if row matches condition
        """
        # Simple WHERE clause parser
        # Supports: col = value, col > value, col < value, col >= value, col <= value, col != value
        operators = {
            ">=": operator.ge,
            "<=": operator.le,
            "!=": operator.ne,
            "=": operator.eq,
            ">": operator.gt,
            "<": operator.lt,
        }
        
        where_clause = where_clause.strip()
        
        # Find operator
        op_func = None
        op_str = None
        for op in operators.keys():
            if op in where_clause:
                op_func = operators[op]
                op_str = op
                break
        
        if op_func is None:
            raise ParseError(f"Unsupported operator in WHERE clause: {where_clause}")
        
        # Split into column and value
        parts = where_clause.split(op_str, 1)
        col_name = parts[0].strip()
        value_str = parts[1].strip()
        
        # Parse value
        from my_rdbms.parser import SQLParser
        value = SQLParser._parse_value(value_str)
        
        def where_func(row: Dict[str, Any]) -> bool:
            row_value = row.get(col_name)
            if row_value is None:
                return False
            return op_func(row_value, value)
        
        return where_func

    def _get_table(self, table_name: str) -> Table:
        """Get a table by name, raising error if not found."""
        if table_name not in self.tables:
            raise TableError(f"Table '{table_name}' does not exist")
        return self.tables[table_name]
