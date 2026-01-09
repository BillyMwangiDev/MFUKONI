"""
Database manager for Mfukoni - wraps custom RDBMS for Django.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from functools import lru_cache

# Add parent directory to path to import my_rdbms
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from my_rdbms.database import Database
from my_rdbms.exceptions import DatabaseError
from .utils import sanitize_sql_string, handle_db_errors


class MfukoniDB:
    """High-level database interface for Mfukoni application."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize Mfukoni database.
        
        Args:
            db_path: Path to database directory (defaults to data/mfukoni.db)
        """
        if db_path is None:
            db_path = os.path.join(BASE_DIR, "data", "mfukoni.db")
        
        self.db = Database(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema with Mfukoni tables."""
        # Create categories table
        if not self.db.table_exists("categories"):
            self.db.execute("""
                CREATE TABLE categories (
                    id INT PRIMARY KEY,
                    name VARCHAR UNIQUE,
                    type VARCHAR
                )
            """)
            # No default categories - users create their own
        
        # Create transactions table
        if not self.db.table_exists("transactions"):
            self.db.execute("""
                CREATE TABLE transactions (
                    id INT PRIMARY KEY,
                    category_id INT,
                    amount FLOAT,
                    description VARCHAR,
                    date VARCHAR,
                    type VARCHAR
                )
            """)
        
        # Create budgets table (optional)
        if not self.db.table_exists("budgets"):
            self.db.execute("""
                CREATE TABLE budgets (
                    id INT PRIMARY KEY,
                    category_id INT,
                    monthly_limit FLOAT,
                    month VARCHAR
                )
            """)

    # Removed _seed_default_categories - users create all categories themselves

    @handle_db_errors
    def add_transaction(
        self,
        category_id: int,
        amount: float,
        description: str,
        date: str,
        trans_type: str
    ) -> None:
        """
        Add a new transaction.
        
        Args:
            category_id: ID of the category
            amount: Transaction amount
            description: Transaction description
            date: Transaction date (YYYY-MM-DD)
            trans_type: 'income' or 'expense'
        """
        # Get next ID
        transactions = self.get_all_transactions()
        next_id = max([t.get("id", 0) for t in transactions], default=0) + 1
        
        # Sanitize description to prevent SQL injection
        desc_escaped = sanitize_sql_string(description) if description else ""
        
        self.db.execute(f"""
            INSERT INTO transactions VALUES 
            ({next_id}, {category_id}, {amount}, '{desc_escaped}', '{date}', '{trans_type}')
        """)
        # Database auto-commits on INSERT - transaction is now saved

    def get_all_transactions(
        self,
        category_id: Optional[int] = None,
        trans_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all transactions with optional filtering.
        
        Args:
            category_id: Filter by category ID
            trans_type: Filter by type ('income' or 'expense')
            limit: Maximum number of results
            
        Returns:
            List of transaction dictionaries
        """
        where_parts = []
        if category_id:
            where_parts.append(f"category_id = {category_id}")
        if trans_type:
            where_parts.append(f"type = '{trans_type}'")
        
        where_clause = " AND ".join(where_parts) if where_parts else None
        
        sql = "SELECT * FROM transactions"
        if where_clause:
            sql += f" WHERE {where_clause}"
        sql += " ORDER BY date DESC, id DESC"
        if limit:
            sql += f" LIMIT {limit}"
        
        # Note: Our simple parser doesn't support ORDER BY or LIMIT yet
        # For now, we'll get all and filter in Python
        results = self.db.execute("SELECT * FROM transactions")
        
        # Apply filters
        if category_id:
            results = [r for r in results if r.get("category_id") == category_id]
        if trans_type:
            results = [r for r in results if r.get("type") == trans_type]
        
        # Sort by date DESC, id DESC
        results.sort(key=lambda x: (x.get("date", ""), x.get("id", 0)), reverse=True)
        
        if limit:
            results = results[:limit]
        
        return results

    def get_transaction(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """Get a single transaction by ID."""
        results = self.db.execute(f"SELECT * FROM transactions WHERE id = {transaction_id}")
        return results[0] if results else None

    @handle_db_errors
    def update_transaction(
        self,
        transaction_id: int,
        category_id: Optional[int] = None,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        date: Optional[str] = None,
        trans_type: Optional[str] = None
    ) -> None:
        """Update a transaction."""
        updates = []
        if category_id is not None:
            updates.append(f"category_id = {category_id}")
        if amount is not None:
            updates.append(f"amount = {amount}")
        if description is not None:
            # Sanitize description to prevent SQL injection
            desc_escaped = sanitize_sql_string(description)
            updates.append(f"description = '{desc_escaped}'")
        if date is not None:
            updates.append(f"date = '{date}'")
        if trans_type is not None:
            updates.append(f"type = '{trans_type}'")
        
        if updates:
            set_clause = ", ".join(updates)
            self.db.execute(f"UPDATE transactions SET {set_clause} WHERE id = {transaction_id}")
            self._clear_all_caches()

    @handle_db_errors
    def delete_transaction(self, transaction_id: int) -> None:
        """Delete a transaction."""
        self.db.execute(f"DELETE FROM transactions WHERE id = {transaction_id}")
        self._clear_all_caches()

    def get_summary(self) -> Dict[str, Any]:
        """Get financial summary."""
        all_transactions = self.get_all_transactions()
        
        total_income = sum(t.get("amount", 0) for t in all_transactions if t.get("type") == "income")
        total_expenses = sum(t.get("amount", 0) for t in all_transactions if t.get("type") == "expense")
        balance = total_income - total_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "transaction_count": len(all_transactions)
        }

    def get_spending_by_category(self) -> List[Dict[str, Any]]:
        """Get spending breakdown by category."""
        try:
            # Get all expense transactions
            expenses = self.get_all_transactions(trans_type="expense")
            
            # Group by category
            category_totals = {}
            for expense in expenses:
                try:
                    cat_id = expense.get("category_id")
                    amount = float(expense.get("amount", 0) or 0)
                    if cat_id:
                        category_totals[cat_id] = category_totals.get(cat_id, 0) + amount
                except (ValueError, TypeError):
                    # Skip invalid entries
                    continue
            
            # Get category names
            categories = self.get_all_categories()
            cat_dict = {cat.get("id"): cat.get("name") for cat in categories}
            
            # Build result
            result = []
            for cat_id, total in category_totals.items():
                result.append({
                    "category_id": cat_id,
                    "category_name": cat_dict.get(cat_id, "Unknown"),
                    "total": float(total)
                })
            
            # Sort by total descending
            result.sort(key=lambda x: x.get("total", 0), reverse=True)
            return result
        except Exception as e:
            # Return empty list on error
            return []

    @lru_cache(maxsize=128)
    def get_all_categories(self, cat_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all categories with caching.
        
        Note: Cache is cleared automatically on category modifications.
        """
        if cat_type:
            # Sanitize cat_type to prevent SQL injection
            cat_type_safe = sanitize_sql_string(cat_type)
            results = self.db.execute(f"SELECT * FROM categories WHERE type = '{cat_type_safe}'")
        else:
            results = self.db.execute("SELECT * FROM categories")
        return results
    
    def _clear_category_cache(self):
        """Clear category cache after modifications."""
        self.get_all_categories.cache_clear()
    
    def _clear_all_caches(self):
        """Clear all caches after data modifications."""
        self._clear_category_cache()
        # Add other cache clears here if more methods are cached in the future

    def get_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get a category by ID."""
        results = self.db.execute(f"SELECT * FROM categories WHERE id = {category_id}")
        return results[0] if results else None

    @handle_db_errors
    def add_category(self, name: str, cat_type: str) -> None:
        """Add a new category."""
        # Get next ID
        categories = self.get_all_categories()
        next_id = max([c.get("id", 0) for c in categories], default=0) + 1
        
        # Sanitize inputs to prevent SQL injection
        name_escaped = sanitize_sql_string(name)
        cat_type_safe = sanitize_sql_string(cat_type)
        
        self.db.execute(f"""
            INSERT INTO categories VALUES ({next_id}, '{name_escaped}', '{cat_type_safe}')
        """)
        # Clear cache after modification
        self._clear_category_cache()
        # Database auto-commits on INSERT

    @handle_db_errors
    def update_category(self, category_id: int, name: str, cat_type: str) -> None:
        """
        Update an existing category.
        
        Args:
            category_id: ID of category to update
            name: New category name
            cat_type: 'income' or 'expense'
        """
        # Sanitize inputs to prevent SQL injection
        name_escaped = sanitize_sql_string(name)
        cat_type_safe = sanitize_sql_string(cat_type)
        
        self.db.execute(f"""
            UPDATE categories SET name = '{name_escaped}', type = '{cat_type_safe}' WHERE id = {category_id}
        """)
        # Database auto-commits on UPDATE
        # Clear cache after modification
        self._clear_category_cache()

    @handle_db_errors
    def delete_category(self, category_id: int) -> None:
        """
        Delete a category.
        
        Args:
            category_id: ID of category to delete
        """
        self.db.execute(f"DELETE FROM categories WHERE id = {category_id}")
        # Database auto-commits on DELETE
        # Clear cache after modification
        self._clear_category_cache()

    def search_transactions(self, query: str) -> List[Dict[str, Any]]:
        """
        Search transactions by description.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching transactions
        """
        all_transactions = self.get_all_transactions()
        query_lower = query.lower()
        
        results = [
            t for t in all_transactions
            if query_lower in str(t.get("description", "")).lower()
        ]
        
        return results

    def get_transactions_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get transactions within a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of transactions in date range
        """
        all_transactions = self.get_all_transactions()
        results = [
            t for t in all_transactions
            if start_date <= t.get("date", "") <= end_date
        ]
        return results

    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get monthly financial summary.
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
            
        Returns:
            Dictionary with monthly summary
        """
        try:
            month_str = f"{year}-{month:02d}"
            all_transactions = self.get_all_transactions()
            
            monthly_transactions = [
                t for t in all_transactions
                if t.get("date", "") and str(t.get("date", "")).startswith(month_str)
            ]
            
            income = sum(
                float(t.get("amount", 0) or 0) 
                for t in monthly_transactions 
                if t.get("type") == "income"
            )
            expenses = sum(
                float(t.get("amount", 0) or 0) 
                for t in monthly_transactions 
                if t.get("type") == "expense"
            )
            
            return {
                "year": year,
                "month": month,
                "income": float(income),
                "expenses": float(expenses),
                "balance": float(income - expenses),
                "transaction_count": len(monthly_transactions)
            }
        except Exception as e:
            # Return safe defaults on error
            return {
                "year": year,
                "month": month,
                "income": 0.0,
                "expenses": 0.0,
                "balance": 0.0,
                "transaction_count": 0
            }

    @handle_db_errors
    def set_budget(self, category_id: int, monthly_limit: float, month: str) -> None:
        """
        Set a monthly budget for a category.
        
        Args:
            category_id: ID of the category
            monthly_limit: Budget limit amount
            month: Month string (e.g., "2026-01")
        """
        # Get next ID
        budgets = self.get_all_budgets()
        next_id = max([b.get("id", 0) for b in budgets], default=0) + 1
        
        # Sanitize month to prevent SQL injection
        month_safe = sanitize_sql_string(month)
        
        self.db.execute(f"""
            INSERT INTO budgets VALUES ({next_id}, {category_id}, {monthly_limit}, '{month_safe}')
        """)
        # Database auto-commits on INSERT, so no need to call commit() explicitly

    def get_all_budgets(self) -> List[Dict[str, Any]]:
        """Get all budgets."""
        results = self.db.execute("SELECT * FROM budgets")
        return results

    def get_budget_for_category(self, category_id: int, month: str) -> Optional[Dict[str, Any]]:
        """Get budget for a specific category and month."""
        # Sanitize month to prevent SQL injection
        month_safe = sanitize_sql_string(month)
        results = self.db.execute(f"""
            SELECT * FROM budgets WHERE category_id = {category_id} AND month = '{month_safe}'
        """)
        return results[0] if results else None

    @handle_db_errors
    def update_budget(self, budget_id: int, monthly_limit: float) -> None:
        """
        Update an existing budget.
        
        Args:
            budget_id: ID of budget to update
            monthly_limit: New monthly limit
        """
        self.db.execute(f"""
            UPDATE budgets SET monthly_limit = {monthly_limit} WHERE id = {budget_id}
        """)
        # Database auto-commits on UPDATE

    @handle_db_errors
    def delete_budget(self, budget_id: int) -> None:
        """
        Delete a budget.
        
        Args:
            budget_id: ID of budget to delete
        """
        self.db.execute(f"DELETE FROM budgets WHERE id = {budget_id}")
        # Database auto-commits on DELETE

    def get_budget(self, budget_id: int) -> Optional[Dict[str, Any]]:
        """Get a single budget by ID."""
        results = self.db.execute(f"SELECT * FROM budgets WHERE id = {budget_id}")
        return results[0] if results else None

    def get_budget_status(self, month: str) -> List[Dict[str, Any]]:
        """
        Get budget status for all categories in a month.
        
        Args:
            month: Month string (e.g., "2026-01")
            
        Returns:
            List of budget status dictionaries
        """
        budgets = [b for b in self.get_all_budgets() if b.get("month") == month]
        expenses = [t for t in self.get_all_transactions(trans_type="expense") 
                   if t.get("date", "").startswith(month)]
        
        # Group expenses by category
        category_expenses = {}
        for expense in expenses:
            cat_id = expense.get("category_id")
            amount = expense.get("amount", 0)
            category_expenses[cat_id] = category_expenses.get(cat_id, 0) + amount
        
        # Get category names
        categories = {c.get("id"): c.get("name") for c in self.get_all_categories()}
        
        # Build status list
        status_list = []
        for budget in budgets:
            cat_id = budget.get("category_id")
            budget_id = budget.get("id")
            limit = budget.get("monthly_limit", 0)
            spent = category_expenses.get(cat_id, 0)
            remaining = limit - spent
            
            status_list.append({
                "budget_id": budget_id,
                "category_id": cat_id,
                "category_name": categories.get(cat_id, "Unknown"),
                "budget_limit": limit,
                "spent": spent,
                "remaining": remaining,
                "percentage_used": (spent / limit * 100) if limit > 0 else 0
            })
        
        return status_list


# Singleton instance
_db_instance: Optional[MfukoniDB] = None


def get_db() -> MfukoniDB:
    """Get the singleton database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = MfukoniDB()
    return _db_instance
