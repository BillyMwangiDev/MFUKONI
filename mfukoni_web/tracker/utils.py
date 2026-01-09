"""
Utility functions and decorators for Mfukoni tracker.
"""

import functools
import time
from typing import Callable, Any, Dict
from django.core.cache import cache
from my_rdbms.exceptions import DatabaseError


def cache_result(timeout: int = 300):
    """
    Decorator to cache function results.
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
    
    Usage:
        @cache_result(timeout=600)
        def get_summary():
            return expensive_operation()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator


def handle_db_errors(func: Callable) -> Callable:
    """
    Decorator to handle database errors gracefully.
    
    Usage:
        @handle_db_errors
        def add_transaction(...):
            db.execute(...)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseError as e:
            # Re-raise database errors for proper handling
            raise
        except Exception as e:
            # Wrap unexpected errors in DatabaseError
            raise DatabaseError(f"Error in {func.__name__}: {str(e)}")
    return wrapper


def validate_input_types(**type_map: type):
    """
    Decorator to validate function argument types.
    
    Args:
        type_map: Dictionary mapping parameter names to expected types
    
    Usage:
        @validate_input_types(category_id=int, amount=float)
        def add_transaction(category_id, amount, ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in type_map.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if value is not None and not isinstance(value, expected_type):
                        raise TypeError(
                            f"{param_name} must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


class DatabaseTransaction:
    """
    Context manager for database transactions.
    Ensures data consistency by committing on success or rolling back on error.
    
    Usage:
        with DatabaseTransaction(db) as tx:
            db.execute("INSERT INTO ...")
            db.execute("UPDATE ...")
        # Auto-commits on successful exit
    """
    
    def __init__(self, db):
        self.db = db
        self.committed = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, commit changes
            try:
                self.db.commit()
                self.committed = True
            except Exception as e:
                # If commit fails, raise the error
                raise DatabaseError(f"Failed to commit transaction: {str(e)}")
        else:
            # Exception occurred - transaction would be rolled back in a real database
            # For JSON storage, changes are not persisted on error
            pass
        return False  # Don't suppress exceptions


def sanitize_sql_string(value: str) -> str:
    """
    Sanitize string for use in SQL queries to prevent SQL injection.
    
    Args:
        value: String value to sanitize
    
    Returns:
        Sanitized string with single quotes escaped
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Escape single quotes (SQL injection prevention)
    return value.replace("'", "''")


def format_currency(amount: float) -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Numeric amount
    
    Returns:
        Formatted currency string (KES X,XXX.XX)
    """
    return f"KES {amount:,.2f}"


def parse_date(date_str: str) -> str:
    """
    Parse and validate date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
    
    Returns:
        Validated date string
    
    Raises:
        ValueError: If date format is invalid
    """
    from datetime import datetime
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")
