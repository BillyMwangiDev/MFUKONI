"""
RDBMS Migration Script - Apply schema to custom RDBMS only.

This script initializes or updates the Mfukoni custom RDBMS schema.
It does NOT affect Django migrations.
"""

import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from my_rdbms.database import Database
from my_rdbms.exceptions import DatabaseError


def apply_migrations():
    """Apply schema migrations to the custom RDBMS."""
    print("=" * 60)
    print("Mfukoni RDBMS Migration Script")
    print("=" * 60)
    
    # Database path
    db_path = os.path.join(BASE_DIR, "data", "mfukoni.db")
    print(f"\nDatabase path: {db_path}")
    
    try:
        # Initialize database
        print("\n[1/4] Initializing database connection...")
        db = Database(db_path)
        print("[OK] Database connection established")
        
        # Check existing tables
        print("\n[2/4] Checking existing tables...")
        existing_tables = db.list_tables()
        print(f"[OK] Found {len(existing_tables)} existing table(s): {', '.join(existing_tables) if existing_tables else 'None'}")
        
        # Create categories table
        print("\n[3/4] Applying schema migrations...")
        if not db.table_exists("categories"):
            print("  - Creating 'categories' table...")
            db.execute("""
                CREATE TABLE categories (
                    id INT PRIMARY KEY,
                    name VARCHAR UNIQUE,
                    type VARCHAR
                )
            """)
            print("  [OK] 'categories' table created")
        else:
            print("  [OK] 'categories' table already exists")
        
        # Create transactions table
        if not db.table_exists("transactions"):
            print("  - Creating 'transactions' table...")
            db.execute("""
                CREATE TABLE transactions (
                    id INT PRIMARY KEY,
                    category_id INT,
                    amount FLOAT,
                    description VARCHAR,
                    date VARCHAR,
                    type VARCHAR
                )
            """)
            print("  [OK] 'transactions' table created")
        else:
            print("  [OK] 'transactions' table already exists")
        
        # Create budgets table
        if not db.table_exists("budgets"):
            print("  - Creating 'budgets' table...")
            db.execute("""
                CREATE TABLE budgets (
                    id INT PRIMARY KEY,
                    category_id INT,
                    monthly_limit FLOAT,
                    month VARCHAR
                )
            """)
            print("  [OK] 'budgets' table created")
        else:
            print("  [OK] 'budgets' table already exists")
        
        # Verify final state
        print("\n[4/4] Verifying migration...")
        final_tables = db.list_tables()
        required_tables = ["categories", "transactions", "budgets"]
        missing_tables = [t for t in required_tables if t not in final_tables]
        
        if missing_tables:
            print(f"  [ERROR] Missing tables: {', '.join(missing_tables)}")
            sys.exit(1)
        else:
            print("  [OK] All required tables exist")
        
        # Display table information
        print("\n" + "=" * 60)
        print("Migration Summary:")
        print("=" * 60)
        for table_name in final_tables:
            table = db.get_table(table_name)
            if table:
                row_count = len(table.rows)
                print(f"  - {table_name}: {row_count} row(s)")
        
        print("\n[OK] RDBMS migration completed successfully!")
        print("=" * 60)
        
    except DatabaseError as e:
        print(f"\n[ERROR] Database Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    apply_migrations()
