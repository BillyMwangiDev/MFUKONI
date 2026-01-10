"""
SQL parser module - converts SQL text to executable commands.
"""

import re
from typing import Dict, Any, List, Optional
from my_rdbms.exceptions import ParseError


class SQLParser:
    """Parses SQL statements into structured commands."""

    @staticmethod
    def parse(sql: str) -> Dict[str, Any]:
        """
        Parse a SQL statement.

        Args:
            sql: SQL statement string

        Returns:
            Dictionary with parsed command structure
        """
        sql = sql.strip()
        if not sql:
            raise ParseError("Empty SQL statement")

        sql_upper = sql.upper()

        if sql_upper.startswith("CREATE TABLE"):
            return SQLParser._parse_create_table(sql)
        elif sql_upper.startswith("INSERT INTO"):
            return SQLParser._parse_insert(sql)
        elif sql_upper.startswith("SELECT"):
            return SQLParser._parse_select(sql)
        elif sql_upper.startswith("UPDATE"):
            return SQLParser._parse_update(sql)
        elif sql_upper.startswith("DELETE FROM"):
            return SQLParser._parse_delete(sql)
        else:
            raise ParseError(f"Unsupported SQL statement: {sql[:50]}")

    @staticmethod
    def _parse_create_table(sql: str) -> Dict[str, Any]:
        """Parse CREATE TABLE statement."""
        # Pattern: CREATE TABLE table_name (col1 TYPE, col2 TYPE PRIMARY KEY, ...)
        pattern = r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\((.*?)\)"
        match = re.search(pattern, sql, re.IGNORECASE | re.DOTALL)

        if not match:
            raise ParseError("Invalid CREATE TABLE syntax")

        table_name = match.group(1)
        columns_str = match.group(2)

        columns = {}
        primary_key = None
        unique_cols = []

        # Parse column definitions
        col_defs = [col.strip() for col in columns_str.split(",")]
        for col_def in col_defs:
            col_def = col_def.strip()
            if not col_def:
                continue

            # Check for PRIMARY KEY
            if "PRIMARY KEY" in col_def.upper():
                parts = col_def.split()
                col_name = parts[0]
                col_type = parts[1] if len(parts) > 1 else "INT"
                primary_key = col_name
                columns[col_name] = col_type.upper()
            # Check for UNIQUE
            elif "UNIQUE" in col_def.upper():
                parts = col_def.split()
                col_name = parts[0]
                col_type = parts[1] if len(parts) > 1 else "VARCHAR"
                unique_cols.append(col_name)
                columns[col_name] = col_type.upper()
            else:
                parts = col_def.split()
                if len(parts) >= 2:
                    col_name = parts[0]
                    col_type = parts[1]
                    columns[col_name] = col_type.upper()

        return {
            "command": "CREATE_TABLE",
            "table_name": table_name,
            "columns": columns,
            "primary_key": primary_key,
            "unique": unique_cols,
        }

    @staticmethod
    def _parse_insert(sql: str) -> Dict[str, Any]:
        """Parse INSERT INTO statement."""
        # Pattern: INSERT INTO table VALUES (val1, val2, ...)
        # Also support: INSERT INTO table VALUES (NULL, val2, ...)
        pattern = r"INSERT\s+INTO\s+(\w+)\s+VALUES\s*\((.*?)\)"
        match = re.search(pattern, sql, re.IGNORECASE | re.DOTALL)

        if not match:
            raise ParseError("Invalid INSERT syntax")

        table_name = match.group(1)
        values_str = match.group(2)

        # Parse values
        values = SQLParser._parse_value_list(values_str)

        return {"command": "INSERT", "table_name": table_name, "values": values}

    @staticmethod
    def _parse_select(sql: str) -> Dict[str, Any]:
        """Parse SELECT statement."""
        # Pattern: SELECT cols FROM table [alias] [WHERE condition] [JOIN ...]
        # Support: FROM table or FROM table alias
        select_match = re.search(r"SELECT\s+(.*?)\s+FROM\s+(\w+)(?:\s+(\w+))?", sql, re.IGNORECASE)
        if not select_match:
            raise ParseError("Invalid SELECT syntax")

        columns_str = select_match.group(1).strip()
        table_name = select_match.group(2)
        left_alias = select_match.group(3)  # Left table alias (e.g., "u" in "FROM users u")

        # Parse columns
        if columns_str == "*":
            columns = None
        else:
            columns = [col.strip() for col in columns_str.split(",")]

        # Parse WHERE clause
        where_clause = None
        where_match = re.search(r"WHERE\s+(.+?)(?:\s+JOIN|\s*$)", sql, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1).strip()

        # Parse JOIN
        join_info = None
        join_match = re.search(
            r"(?:INNER\s+)?JOIN\s+(\w+)\s+(\w+)\s+ON\s+(\w+\.\w+)\s*=\s*(\w+\.\w+)",
            sql,
            re.IGNORECASE,
        )
        if join_match:
            join_table = join_match.group(1)
            join_alias = join_match.group(2)
            left_col = join_match.group(3)
            right_col = join_match.group(4)
            join_info = {
                "table": join_table,
                "alias": join_alias,
                "left_alias": left_alias,  # Left table alias for column prefixing
                "on": {"left": left_col, "right": right_col},
            }

        return {
            "command": "SELECT",
            "table_name": table_name,
            "table_alias": left_alias,  # Store left table alias
            "columns": columns,
            "where": where_clause,
            "join": join_info,
        }

    @staticmethod
    def _parse_update(sql: str) -> Dict[str, Any]:
        """Parse UPDATE statement."""
        # Pattern: UPDATE table SET col1=val1, col2=val2 [WHERE condition]
        update_match = re.search(
            r"UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE|\s*$)", sql, re.IGNORECASE | re.DOTALL
        )
        if not update_match:
            raise ParseError("Invalid UPDATE syntax")

        table_name = update_match.group(1)
        set_clause = update_match.group(2).strip()

        # Parse SET clause
        updates = {}
        for assignment in set_clause.split(","):
            assignment = assignment.strip()
            if "=" in assignment:
                col, val = assignment.split("=", 1)
                col = col.strip()
                val = SQLParser._parse_value(val.strip())
                updates[col] = val

        # Parse WHERE clause
        where_clause = None
        where_match = re.search(r"WHERE\s+(.+?)$", sql, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1).strip()

        return {
            "command": "UPDATE",
            "table_name": table_name,
            "updates": updates,
            "where": where_clause,
        }

    @staticmethod
    def _parse_delete(sql: str) -> Dict[str, Any]:
        """Parse DELETE FROM statement."""
        # Pattern: DELETE FROM table [WHERE condition]
        delete_match = re.search(r"DELETE\s+FROM\s+(\w+)(?:\s+WHERE|\s*$)", sql, re.IGNORECASE)
        if not delete_match:
            raise ParseError("Invalid DELETE syntax")

        table_name = delete_match.group(1)

        # Parse WHERE clause
        where_clause = None
        where_match = re.search(r"WHERE\s+(.+?)$", sql, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1).strip()

        return {"command": "DELETE", "table_name": table_name, "where": where_clause}

    @staticmethod
    def _parse_value_list(values_str: str) -> List[Any]:
        """Parse a list of values from SQL."""
        values = []
        current = ""
        in_quotes = False
        quote_char = None

        for char in values_str:
            if char in ("'", '"') and (not current or current[-1] != "\\"):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                current += char
            elif char == "," and not in_quotes:
                values.append(SQLParser._parse_value(current.strip()))
                current = ""
            else:
                current += char

        if current.strip():
            values.append(SQLParser._parse_value(current.strip()))

        return values

    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse a single SQL value."""
        value = value.strip()

        # Remove quotes
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            return value[1:-1]

        # Parse NULL
        if value.upper() == "NULL":
            return None

        # Parse boolean
        if value.upper() in ("TRUE", "FALSE"):
            return value.upper() == "TRUE"

        # Parse number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value
