"""
REPL (Read-Eval-Print Loop) for interactive SQL queries.
"""

import sys
from typing import Optional, List, Dict, Any
from my_rdbms.database import Database
from my_rdbms.exceptions import DatabaseError


class REPL:
    """Interactive SQL shell."""

    def __init__(self, db_path: str = "data/mfukoni.db"):
        """
        Initialize REPL.
        
        Args:
            db_path: Path to database
        """
        self.db = Database(db_path)
        self.running = True

    def run(self) -> None:
        """Start the REPL."""
        print("=" * 60)
        print("Mfukoni RDBMS - Interactive SQL Shell")
        print("=" * 60)
        print("Type SQL commands or '.help' for help")
        print("Type '.exit' or '.quit' to exit")
        print("=" * 60)
        print()
        
        while self.running:
            try:
                line = input("mfukoni> ").strip()
                
                if not line:
                    continue
                
                # Handle meta commands
                if line.startswith("."):
                    self._handle_meta_command(line)
                    continue
                
                # Handle multi-line SQL
                sql = line
                while sql.endswith("\\"):
                    sql = sql[:-1] + " "
                    next_line = input("...> ").strip()
                    sql += next_line
                
                # Execute SQL
                try:
                    result = self.db.execute(sql)
                    self._display_result(result, sql)
                except DatabaseError as e:
                    print(f"ERROR: {e}")
                except Exception as e:
                    print(f"ERROR: {e}")
                
            except EOFError:
                print("\nExiting...")
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    def _handle_meta_command(self, command: str) -> None:
        """Handle meta commands (starting with .)."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == ".help":
            self._print_help()
        elif cmd == ".exit" or cmd == ".quit":
            self.running = False
        elif cmd == ".tables":
            self._list_tables()
        elif cmd == ".schema":
            if len(parts) > 1:
                self._show_schema(parts[1])
            else:
                print("Usage: .schema <table_name>")
        else:
            print(f"Unknown command: {cmd}")
            print("Type .help for available commands")

    def _print_help(self) -> None:
        """Print help message."""
        print("\nAvailable Commands:")
        print("  .help              - Show this help message")
        print("  .tables            - List all tables")
        print("  .schema <table>    - Show schema for a table")
        print("  .exit / .quit      - Exit the REPL")
        print("\nSQL Commands:")
        print("  CREATE TABLE ...   - Create a new table")
        print("  INSERT INTO ...    - Insert a row")
        print("  SELECT ...         - Query data")
        print("  UPDATE ...         - Update rows")
        print("  DELETE FROM ...    - Delete rows")
        print()

    def _list_tables(self) -> None:
        """List all tables."""
        tables = self.db.list_tables()
        if not tables:
            print("No tables found.")
        else:
            print("\nTables:")
            for table_name in tables:
                table = self.db.get_table(table_name)
                row_count = table.get_row_count() if table else 0
                print(f"  - {table_name} ({row_count} rows)")
        print()

    def _show_schema(self, table_name: str) -> None:
        """Show schema for a table."""
        table = self.db.get_table(table_name)
        if not table:
            print(f"Table '{table_name}' does not exist.")
            return
        
        schema = table.get_schema()
        print(f"\nSchema for '{table_name}':")
        print("  Columns:")
        for col_name, col_type in schema.get("columns", {}).items():
            constraints = []
            if schema.get("primary_key") == col_name:
                constraints.append("PRIMARY KEY")
            if col_name in schema.get("unique", []):
                constraints.append("UNIQUE")
            constraint_str = " " + " ".join(constraints) if constraints else ""
            print(f"    {col_name}: {col_type}{constraint_str}")
        print()

    def _display_result(self, result: Any, sql: str) -> None:
        """Display query result."""
        if result is None:
            # Command executed successfully (CREATE, INSERT, UPDATE, DELETE)
            sql_upper = sql.upper()
            if "CREATE" in sql_upper:
                print("Table created successfully.")
            elif "INSERT" in sql_upper:
                print("Row inserted successfully.")
            elif "UPDATE" in sql_upper:
                print(f"{result} row(s) updated." if isinstance(result, int) else "Row(s) updated.")
            elif "DELETE" in sql_upper:
                print(f"{result} row(s) deleted." if isinstance(result, int) else "Row(s) deleted.")
        elif isinstance(result, list):
            # SELECT result
            if not result:
                print("(0 rows)")
            else:
                self._print_table(result)
        else:
            print(result)

    def _print_table(self, rows: List[dict]) -> None:
        """Print rows in a formatted table."""
        if not rows:
            return
        
        # Get all column names
        columns = list(rows[0].keys())
        
        # Calculate column widths
        widths = {col: len(str(col)) for col in columns}
        for row in rows:
            for col in columns:
                widths[col] = max(widths[col], len(str(row.get(col, ""))))
        
        # Print header
        header = " | ".join(str(col).ljust(widths[col]) for col in columns)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows:
            values = [str(row.get(col, "")).ljust(widths[col]) for col in columns]
            print(" | ".join(values))
        
        print(f"\n({len(rows)} row(s))")


def main():
    """Main entry point for REPL."""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mfukoni.db"
    repl = REPL(db_path)
    repl.run()


if __name__ == "__main__":
    main()
