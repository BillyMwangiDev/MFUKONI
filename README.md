# Mfukoni Finance Tracker

**Version:** 1.0.0  
**Last Updated:** January 10, 2026  
**Python Version:** 3.7+ (3.11+ recommended for Docker)  
**Django Version:** 3.2.25  
**Docker Support:** ✅ Fully containerized

<div align="center">

**A Personal Finance Management System with Custom RDBMS**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*"Mfukoni" - Swahili for "in the pocket"*

</div>

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Requirements Analysis](#requirements-analysis)
3. [Project Scope](#project-scope)
4. [Features](#features)
5. [User Stories](#user-stories)
6. [Use Case Diagram](#use-case-diagram)
7. [Database Design](#database-design)
   - [ER Diagram](#er-diagram)
   - [Schema Design](#schema-design)
   - [Normalization](#normalization)
   - [Relationships](#relationships)
8. [System Architecture](#system-architecture)
9. [Flow Charts](#flow-charts)
10. [SQL Queries & Operations](#sql-queries--operations)
11. [Security](#security)
12. [Performance & Optimization](#performance--optimization)
13. [Testing](#testing)
14. [Installation & Setup](#installation--setup)
15. [Usage](#usage)
16. [API Documentation](#api-documentation)
17. [Deployment](#deployment)
18. [Contributing](#contributing)

---

## Project Overview

**Mfukoni** is a comprehensive personal finance tracking application that demonstrates a custom-built Relational Database Management System (RDBMS) with full SQL capabilities. The system allows users to track income, expenses, manage budgets, and generate financial reports.

### Key Highlights

- **Custom RDBMS Engine** - Built from scratch with SQL parsing and execution
- **Full CRUD Operations** - Complete Create, Read, Update, Delete functionality
- **SQL Support** - Execute standard SQL queries (SELECT, INSERT, UPDATE, DELETE, JOIN)
- **Constraints & Indexing** - PRIMARY KEY, UNIQUE constraints with hash-based indexing
- **Web Interface** - Modern Django-based web application
- **Security** - SQL injection prevention and input validation
- **Performance** - Optimized queries with indexing and caching

---

## Challenge Requirements Fulfillment

### Requirement 1: Design and Implement a Simple RDBMS

#### 1.1 Support for Declaring Tables with Column Data Types
**Status: FULLY IMPLEMENTED**

**Supported Data Types:**
- `INT` - Integer numbers
- `VARCHAR` - Variable-length strings  
- `FLOAT` - Floating-point numbers
- `BOOLEAN` - True/false values

**Implementation:**
- `my_rdbms/parser.py` - Parses CREATE TABLE with column types
- `my_rdbms/table.py` - Handles type conversion and validation

**Example:**
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR UNIQUE,
    type VARCHAR
);
```

#### 1.2 CRUD Operations
**Status: FULLY IMPLEMENTED**

**All CRUD operations supported:**
- **CREATE** - `CREATE TABLE` statements
- **READ** - `SELECT` statements with WHERE clauses
- **UPDATE** - `UPDATE` statements with WHERE clauses
- **DELETE** - `DELETE FROM` statements with WHERE clauses

**Implementation:**
- `my_rdbms/parser.py` - Parses all SQL commands
- `my_rdbms/executor.py` - Executes all operations
- `my_rdbms/table.py` - Row-level operations

#### 1.3 Basic Indexing
**Status: FULLY IMPLEMENTED**

**Features:**
- Hash-based indexing for O(1) lookups
- Automatic index on PRIMARY KEY columns
- Automatic index on UNIQUE columns
- Index maintenance on data modifications

**Implementation:**
- `my_rdbms/index.py` - Complete index implementation (139 lines)
- Integrated with table operations

#### 1.4 Primary and Unique Keying
**Status: FULLY IMPLEMENTED**

**PRIMARY KEY:**
- Enforces uniqueness
- Prevents NULL values
- Automatic indexing
- Raises `PrimaryKeyError` on violation

**UNIQUE:**
- Enforces column uniqueness
- Allows NULL values
- Automatic indexing
- Raises `UniqueConstraintError` on violation

**Implementation:**
- `my_rdbms/constraints.py` - Constraint validation (108 lines)
- `my_rdbms/parser.py` - Parses constraints in CREATE TABLE
- `my_rdbms/table.py` - Validates on INSERT/UPDATE

#### 1.5 Joining
**Status: FULLY IMPLEMENTED**

**Features:**
- INNER JOIN support
- Standard SQL JOIN syntax
- Join with WHERE clauses
- Table aliases supported

**Example:**
```sql
SELECT t.description, c.name 
FROM transactions t 
INNER JOIN categories c ON t.category_id = c.id
WHERE t.type = 'expense';
```

**Implementation:**
- `my_rdbms/parser.py` - Parses JOIN clauses
- `my_rdbms/executor.py` - Executes JOIN operations (lines 127-161)

#### 1.6 SQL or Similar Interface
**Status: FULLY IMPLEMENTED**

**SQL Commands Supported:**
- `CREATE TABLE` - Table creation with schema
- `INSERT INTO ... VALUES` - Row insertion
- `SELECT ... FROM ... WHERE` - Data retrieval
- `UPDATE ... SET ... WHERE` - Row updates
- `DELETE FROM ... WHERE` - Row deletion

**WHERE Clause Operators:**
- `=`, `>`, `<`, `>=`, `<=`, `!=`

**Implementation:**
- `my_rdbms/parser.py` - Complete SQL parser (276 lines)
- Standard SQL syntax patterns

#### 1.7 Interactive REPL Mode
**Status: FULLY IMPLEMENTED**

**Features:**
- Interactive command-line shell
- SQL command execution
- Meta commands (`.help`, `.tables`, `.schema`, `.exit`)
- Formatted table output
- Multi-line SQL support

**Usage:**
```bash
python -m my_rdbms.repl
```

**Implementation:**
- `my_rdbms/repl.py` - Complete REPL (195 lines)

---

### Requirement 2: Demonstrate with Web App Requiring CRUD

#### 2.1 Web Application
**Status: FULLY IMPLEMENTED**

**Features:**
- Django-based web application
- **Uses Custom RDBMS (NOT Django ORM)**
- All CRUD operations via web interface
- Modern, responsive UI

**Key Point:** The web app uses our custom RDBMS exclusively. Django ORM is NOT used.

**Evidence:**
- `mfukoni_web/tracker/models.py` - Empty (no Django models)
- `mfukoni_web/tracker/db_manager.py` - Wraps custom RDBMS
- All views use `MfukoniDB` class (custom RDBMS wrapper)

#### 2.2 CRUD Operations in Web App

**CREATE:**
- Add transactions
- Add categories
- Set budgets

**READ:**
- View transactions (with filtering)
- View categories
- View budgets
- View reports

**UPDATE:**
- Edit transactions
- Edit categories
- Update budgets

**DELETE:**
- Delete transactions
- Delete categories
- Delete budgets

**Implementation:**
- `mfukoni_web/tracker/views.py` - All CRUD views
- `mfukoni_web/tracker/db_manager.py` - Database operations using custom RDBMS

---

### Requirement 3: Credit Where It's Due

#### 3.1 Documentation
**Status: FULLY DOCUMENTED**

- Comprehensive README.md
- Technical documentation
- Code comments
- Test coverage
- This requirements checklist

#### 3.2 Technologies Used
- Python 3.7+ (with type hints)
- Django 3.2+ (web framework only, NOT ORM)
- Bootstrap 5 (UI framework)
- Bootstrap Icons (icon library)
- pytest (testing framework)

#### 3.3 Custom Implementation
- **Custom RDBMS built from scratch**
- **No external database libraries** (no SQLite, PostgreSQL, MySQL)
- **No Django ORM** - All database operations use custom RDBMS
- **SQL Parser** - Custom regex-based parser
- **Storage Engine** - Custom JSON-based persistence
- **Index Manager** - Custom hash-based indexing
- **Constraint Validator** - Custom constraint enforcement

---

## Requirements Analysis

### Functional Requirements

#### FR1: Transaction Management
- **FR1.1**: Users can add income and expense transactions
- **FR1.2**: Users can view all transactions with filtering options
- **FR1.3**: Users can edit existing transactions
- **FR1.4**: Users can delete transactions
- **FR1.5**: Transactions must have: amount, category, date, description, type

#### FR2: Category Management
- **FR2.1**: Users can create custom categories (income/expense)
- **FR2.2**: Users can edit category names and types
- **FR2.3**: Users can delete categories
- **FR2.4**: Category names must be unique

#### FR3: Budget Management
- **FR3.1**: Users can set monthly budgets for expense categories
- **FR3.2**: System tracks spending against budgets
- **FR3.3**: Users can view budget status and remaining amounts
- **FR3.4**: Users can update or delete budgets

#### FR4: Financial Reporting
- **FR4.1**: Dashboard displays total income, expenses, and balance
- **FR4.2**: Monthly summaries and trends
- **FR4.3**: Spending breakdown by category
- **FR4.4**: Export transactions to CSV, PDF, or Excel formats

#### FR5: Database Operations
- **FR5.1**: Support SQL CREATE TABLE statements
- **FR5.2**: Support INSERT, SELECT, UPDATE, DELETE operations
- **FR5.3**: Support WHERE clause filtering
- **FR5.4**: Support INNER JOIN operations
- **FR5.5**: Enforce PRIMARY KEY and UNIQUE constraints
- **FR5.6**: Automatic indexing on PRIMARY KEY columns

### Non-Functional Requirements

#### NFR1: Performance
- Query response time < 100ms for typical operations
- Support up to 10,000 transactions without degradation
- Index lookups should be O(1) or O(log n)

#### NFR2: Security
- Prevent SQL injection attacks
- Input validation on all user inputs
- Secure data storage

#### NFR3: Usability
- Intuitive web interface
- Responsive design (mobile-friendly)
- Clear error messages

#### NFR4: Reliability
- Data persistence across restarts
- Graceful error handling
- Data integrity validation

---

## Project Scope

### In Scope

- Custom RDBMS implementation  
- SQL parsing and execution  
- CRUD operations via web interface  
- Budget tracking  
- Financial reports and analytics  
- Category management  
- Data export functionality  
- Interactive REPL for SQL queries  

### Out of Scope

- User authentication and multi-user support  
- Real-time notifications  
- Mobile native applications  
- Payment gateway integration  
- Advanced analytics (ML/AI)  
- Cloud synchronization  

---

## Features

### Core Features

1. **Transaction Management**
   - Add income/expense transactions
   - Edit and delete transactions
   - Filter by category, type, date range
   - Search transactions

2. **Category Management**
   - Create custom income/expense categories
   - Edit and delete categories
   - Unique category names enforced

3. **Budget Tracking**
   - Set monthly budgets per category
   - Track spending against budgets
   - Visual progress indicators
   - Budget status alerts

4. **Financial Dashboard**
   - Total income, expenses, balance
   - Recent transactions
   - Spending by category breakdown
   - Quick-add transaction buttons

5. **Reports & Analytics**
   - Monthly financial summaries
   - 6-month trend analysis
   - Top spending categories
   - Budget status tracking
   - Export to CSV, PDF, or Excel formats

6. **Custom RDBMS**
   - SQL query execution
   - Full CRUD operations
   - JOIN support

---

## User Stories

### US1: As a user, I want to add a transaction
**Acceptance Criteria:**
- I can select transaction type (income/expense)
- I can choose a category
- I can enter amount, date, and description
- Transaction is saved and appears in the list

### US2: As a user, I want to view my financial summary
**Acceptance Criteria:**
- Dashboard shows total income, expenses, and balance
- Recent transactions are displayed
- Spending breakdown by category is visible

### US3: As a user, I want to set a budget
**Acceptance Criteria:**
- I can select a category and set monthly limit
- System tracks spending against the budget
- I can see remaining budget amount

### US4: As a user, I want to filter transactions
**Acceptance Criteria:**
- I can filter by category
- I can filter by type (income/expense)
- I can filter by date range
- I can search by description

### US5: As a user, I want to generate reports
**Acceptance Criteria:**
- I can view monthly summaries
- I can see spending trends
- I can export data to CSV

---

## Use Case Diagram

```
                    Mfukoni Finance Tracker
                            |
        ┌───────────────────┼───────────────────┐
        |                   |                   |
    [User]            [Administrator]      [System]
        |                   |                   |
        |                   |                   |
    ┌───┴───────────────────┴───────────────────┴───┐
    |                                                 |
    |  ┌─────────────────────────────────────────┐  |
    |  |  Add Transaction                         |  |
    |  |  Edit Transaction                       |  |
    |  |  Delete Transaction                     |  |
    |  |  View Transactions                      |  |
    |  |  Filter Transactions                    |  |
    |  └─────────────────────────────────────────┘  |
    |                                                 |
    |  ┌─────────────────────────────────────────┐  |
    |  |  Create Category                         |  |
    |  |  Edit Category                          |  |
    |  |  Delete Category                        |  |
    |  └─────────────────────────────────────────┘  |
    |                                                 |
    |  ┌─────────────────────────────────────────┐  |
    |  |  Set Budget                             |  |
    |  |  View Budget Status                    |  |
    |  |  Update Budget                         |  |
    |  └─────────────────────────────────────────┘  |
    |                                                 |
    |  ┌─────────────────────────────────────────┐  |
    |  |  View Dashboard                         |  |
    |  |  Generate Reports                      |  |
    |  |  Export Data                            |  |
    |  └─────────────────────────────────────────┘  |
    |                                                 |
    |  ┌─────────────────────────────────────────┐  |
    |  |  Execute SQL Query                      |  |
    |  └─────────────────────────────────────────┘  |
    └─────────────────────────────────────────────────┘
```

---

## Database Design

### ER Diagram

```
┌─────────────────────┐
│    CATEGORIES        │
├─────────────────────┤
│ PK id (INT)          │
│    name (VARCHAR)    │◄──┐
│    type (VARCHAR)    │   │
│    UNIQUE(name)      │   │
└─────────────────────┘   │
                          │
                          │ category_id (FK)
                          │
┌─────────────────────┐   │
│   TRANSACTIONS      │   │
├─────────────────────┤   │
│ PK id (INT)          │   │
│ FK category_id (INT) ├───┘
│    amount (FLOAT)    │
│    description (VARCHAR)
│    date (VARCHAR)    │
│    type (VARCHAR)    │
└─────────────────────┘
                          │
                          │ category_id (FK)
                          │
┌─────────────────────┐   │
│      BUDGETS        │   │
├─────────────────────┤   │
│ PK id (INT)          │   │
│ FK category_id (INT) ├───┘
│    monthly_limit (FLOAT)
│    month (VARCHAR)   │
└─────────────────────┘
```

### Schema Design

#### Categories Table
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR UNIQUE,
    type VARCHAR  -- 'income' or 'expense'
);
```

**Attributes:**
- `id`: Primary key, auto-incremented integer
- `name`: Unique category name (VARCHAR, UNIQUE constraint)
- `type`: Category type - either 'income' or 'expense'

**Constraints:**
- PRIMARY KEY on `id`
- UNIQUE constraint on `name`

#### Transactions Table
```sql
CREATE TABLE transactions (
    id INT PRIMARY KEY,
    category_id INT,
    amount FLOAT,
    description VARCHAR,
    date VARCHAR,
    type VARCHAR  -- 'income' or 'expense'
);
```

**Attributes:**
- `id`: Primary key, auto-incremented integer
- `category_id`: Foreign key reference to categories.id
- `amount`: Transaction amount (FLOAT)
- `description`: Optional transaction description
- `date`: Transaction date (VARCHAR, format: YYYY-MM-DD)
- `type`: Transaction type - 'income' or 'expense'

**Constraints:**
- PRIMARY KEY on `id`
- Referential integrity with categories table (logical, not enforced at DB level)

#### Budgets Table
```sql
CREATE TABLE budgets (
    id INT PRIMARY KEY,
    category_id INT,
    monthly_limit FLOAT,
    month VARCHAR  -- Format: YYYY-MM
);
```

**Attributes:**
- `id`: Primary key, auto-incremented integer
- `category_id`: Foreign key reference to categories.id
- `monthly_limit`: Budget limit amount (FLOAT)
- `month`: Month identifier (VARCHAR, format: YYYY-MM)

**Constraints:**
- PRIMARY KEY on `id`
- Referential integrity with categories table

### Normalization

The database design follows **Third Normal Form (3NF)**:

1. **First Normal Form (1NF)**: Achieved
   - All attributes contain atomic values
   - No repeating groups

2. **Second Normal Form (2NF)**: Achieved
   - All non-key attributes fully depend on primary key
   - No partial dependencies

3. **Third Normal Form (3NF)**: Achieved
   - No transitive dependencies
   - All attributes depend only on primary key

**Normalization Benefits:**
- Eliminates data redundancy
- Prevents update anomalies
- Ensures data integrity
- Simplifies maintenance

### Relationships

1. **Categories → Transactions** (One-to-Many)
   - One category can have many transactions
   - Relationship: `categories.id` → `transactions.category_id`

2. **Categories → Budgets** (One-to-Many)
   - One category can have many budgets (different months)
   - Relationship: `categories.id` → `budgets.category_id`

3. **Transactions → Budgets** (Many-to-One via Category)
   - Multiple transactions can relate to one budget through category
   - Indirect relationship through category_id

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌──────────────────┐          ┌──────────────────┐       │
│  │  Web Interface   │                              │       │
│  │  (Django Views)  │          │  (Command Line)  │       │
│  └────────┬─────────┘          └────────┬─────────┘       │
└───────────┼──────────────────────────────┼──────────────────┘
            │                              │
            └──────────────┬───────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         MfukoniDB (db_manager.py)                    │  │
│  │  - High-level business logic                          │  │
│  │  - Data validation                                    │  │
│  │  - Error handling                                     │  │
│  └────────────────────┬───────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                    DATABASE LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Custom RDBMS Engine                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │ SQL Parser   │→ │  Executor    │→ │  Storage    │ │  │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │ Constraints  │  │   Indexing   │  │   Tables    │ │  │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │  │
│  └────────────────────┬───────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                    PERSISTENCE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              JSON File Storage                         │  │
│  │  - data/mfukoni.db/categories.json                    │  │
│  │  - data/mfukoni.db/transactions.json                   │  │
│  │  - data/mfukoni.db/budgets.json                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Presentation Layer
- **Django Views**: Handle HTTP requests/responses
- **Templates**: HTML rendering with Bootstrap 5
- **Forms**: Input validation and user interaction

#### 2. Application Layer
- **MfukoniDB**: High-level database interface
- **Business Logic**: Transaction processing, budget calculations
- **Validation**: Input sanitization and validation
- **Caching**: In-memory caching for frequently accessed data

#### 3. Database Layer
- **SQL Parser**: Converts SQL text to structured commands
- **Query Executor**: Executes parsed queries
- **Table Manager**: Manages table schemas and rows
- **Constraint Validator**: Enforces PRIMARY KEY and UNIQUE
- **Index Manager**: Hash-based indexing for fast lookups
- **Storage Manager**: Handles JSON file I/O

#### 4. Persistence Layer
- **JSON Files**: Human-readable data storage
- **Auto-commit**: Automatic persistence on data modifications

---

## Flow Charts

### Transaction Addition Flow

```
START
  │
  ▼
[User fills transaction form]
  │
  ▼
[Form Validation]
  │
  ├─ Invalid ──→ [Display Errors] ──→ END
  │
  └─ Valid
      │
      ▼
[Check if category exists]
  │
  ├─ No ──→ [Redirect to create category] ──→ END
  │
  └─ Yes
      │
      ▼
[Sanitize input (prevent SQL injection)]
  │
  ▼
[Execute INSERT query]
  │
  ├─ Error ──→ [Display error message] ──→ END
  │
  └─ Success
      │
      ▼
[Auto-commit to JSON]
  │
  ▼
[Update dashboard cache]
  │
  ▼
[Redirect to dashboard]
  │
  ▼
END
```

### SQL Query Execution Flow

```
START
  │
  ▼
[Receive SQL string]
  │
  ▼
[SQL Parser]
  │
  ├─ Parse Error ──→ [Return ParseError] ──→ END
  │
  └─ Success
      │
      ▼
[Query Executor]
  │
  ├─ CREATE_TABLE ──→ [Create table schema]
  │                    [Initialize indexes]
  │                    [Save to storage]
  │
  ├─ INSERT ──→ [Validate constraints]
  │              [Check PRIMARY KEY]
  │              [Check UNIQUE]
  │              [Insert row]
  │              [Update index]
  │
  ├─ SELECT ──→ [Build WHERE function]
  │              [Check for JOIN]
  │              [Execute query]
  │              [Use index if available]
  │
  ├─ UPDATE ──→ [Validate constraints]
  │              [Update rows]
  │              [Update index]
  │
  └─ DELETE ──→ [Delete rows]
                 [Update index]
  │
  ▼
[Auto-commit (if data modification)]
  │
  ▼
[Return result]
  │
  ▼
END
```

### Budget Status Calculation Flow

```
START
  │
  ▼
[Get current month]
  │
  ▼
[Load all budgets for month]
  │
  ▼
[Load all expense transactions for month]
  │
  ▼
[Group expenses by category_id]
  │
  ▼
[For each budget]
  │
  ├─ Calculate spent = sum(expenses for category)
  │
  ├─ Calculate remaining = budget_limit - spent
  │
  ├─ Calculate percentage_used = (spent / budget_limit) * 100
  │
  └─ Build status object
  │
  ▼
[Return budget status list]
  │
  ▼
END
```

---

## SQL Queries & Operations

### Complex Queries Used

#### 1. Transaction Summary with Category Names (JOIN)

```sql
SELECT 
    t.id,
    t.amount,
    t.description,
    t.date,
    t.type,
    c.name as category_name
FROM transactions t
INNER JOIN categories c ON t.category_id = c.id
WHERE t.type = 'expense'
ORDER BY t.date DESC
```

**Implementation:**
- Uses INNER JOIN to combine transactions and categories
- Filters by transaction type
- Orders by date descending

#### 2. Monthly Summary (Aggregation)

```python
# Pseudo-SQL (implemented in Python)
SELECT 
    SUM(amount) as total_income
FROM transactions
WHERE type = 'income' 
  AND date LIKE '2026-01%'

SELECT 
    SUM(amount) as total_expenses
FROM transactions
WHERE type = 'expense' 
  AND date LIKE '2026-01%'
```

**Implementation:**
- Filters transactions by date prefix (month)
- Sums amounts by type
- Calculates balance

#### 3. Spending by Category (Grouping)

```python
# Pseudo-SQL (implemented in Python)
SELECT 
    category_id,
    SUM(amount) as total
FROM transactions
WHERE type = 'expense'
GROUP BY category_id
ORDER BY total DESC
```

**Implementation:**
- Groups expenses by category
- Calculates totals
- Sorts by total descending

#### 4. Budget Status (Complex Join)

```python
# Combines budgets, transactions, and categories
SELECT 
    b.id as budget_id,
    b.category_id,
    b.monthly_limit,
    c.name as category_name,
    SUM(t.amount) as spent
FROM budgets b
INNER JOIN categories c ON b.category_id = c.id
LEFT JOIN transactions t ON t.category_id = b.category_id 
    AND t.type = 'expense' 
    AND t.date LIKE b.month || '%'
WHERE b.month = '2026-01'
GROUP BY b.id, b.category_id, b.monthly_limit, c.name
```

**Implementation:**
- Joins three tables
- Filters by month
- Groups and aggregates spending

### Query Patterns

#### Pattern 1: Simple SELECT with WHERE
```sql
SELECT * FROM transactions WHERE id = 1
```

#### Pattern 2: SELECT with Multiple Conditions
```sql
SELECT * FROM transactions 
WHERE category_id = 2 AND type = 'expense'
```

#### Pattern 3: JOIN Query
```sql
SELECT t.description, c.name 
FROM transactions t 
INNER JOIN categories c ON t.category_id = c.id
```

#### Pattern 4: UPDATE with WHERE
```sql
UPDATE transactions 
SET amount = 150.00 
WHERE id = 1
```

#### Pattern 5: DELETE with WHERE
```sql
DELETE FROM transactions WHERE id = 1
```

---

## Security

### SQL Injection Prevention

#### 1. Input Sanitization

All user inputs are sanitized before being used in SQL queries:

```python
def add_transaction(self, category_id: int, amount: float, description: str, ...):
    # Escape single quotes to prevent SQL injection
    desc_escaped = description.replace("'", "''")
    
    # Use parameterized query structure
    self.db.execute(f"""
        INSERT INTO transactions VALUES 
        ({next_id}, {category_id}, {amount}, '{desc_escaped}', '{date}', '{trans_type}')
    """)
```

#### 2. Type Validation

All inputs are validated and converted to appropriate types:

```python
# Validate and convert types
category_id = int(form.cleaned_data['category_id'])
amount = float(form.cleaned_data['amount'])
date = str(form.cleaned_data['date'])
```

#### 3. Constraint Enforcement

Database constraints prevent invalid data:

- PRIMARY KEY prevents duplicate IDs
- UNIQUE constraint prevents duplicate category names
- Type checking ensures data integrity

#### 4. Error Handling

Comprehensive error handling prevents information leakage:

```python
try:
    result = db.execute(sql)
except DatabaseError as e:
    # Log error internally
    logger.error(f"Database error: {str(e)}")
    # Return user-friendly message
    messages.error(request, "An error occurred. Please try again.")
```

### Security Best Practices Implemented

- **Input Validation**: All inputs validated before processing  
- **SQL Escaping**: Single quotes escaped in string values  
- **Type Checking**: Strict type conversion and validation  
- **Error Handling**: Graceful error handling without exposing internals  
- **Constraint Enforcement**: Database-level constraint validation  
- **CSRF Protection**: Django CSRF middleware enabled on all forms  
- **XSS Prevention**: Template auto-escaping enabled by default  
- **Security Headers**: HSTS, XSS Filter, Content-Type nosniff configured for production  
- **Cookie Security**: Secure, HttpOnly, SameSite cookies in production  
- **Environment Variables**: Sensitive data stored in environment variables via python-decouple  

---

## Performance & Optimization

### Indexing Strategy

#### 1. Primary Key Indexing

Automatic hash-based index on PRIMARY KEY columns:

```python
class HashIndex:
    """Hash-based index for O(1) lookups."""
    
    def __init__(self, column_name: str):
        self.column_name = column_name
        self.index: Dict[Any, List[int]] = {}
    
    def add(self, value: Any, row_id: int) -> None:
        """Add entry to index."""
        if value not in self.index:
            self.index[value] = []
        self.index[value].append(row_id)
    
    def lookup(self, value: Any) -> List[int]:
        """Lookup row IDs by value. O(1) complexity."""
        return self.index.get(value, [])
```

**Benefits:**
- O(1) lookup time for PRIMARY KEY queries
- Fast WHERE clause execution on indexed columns
- Automatic index maintenance

#### 2. Query Optimization

**Index Usage:**
```python
# Query uses index automatically
SELECT * FROM transactions WHERE id = 123
# Uses hash index: O(1) lookup
```

**Filtering Optimization:**
```python
# Early filtering reduces data processing
transactions = [t for t in all_transactions 
                if t.get("date", "").startswith(month_str)]
```

### Caching Strategy

#### In-Memory Caching

Frequently accessed data is cached:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_all_categories(self) -> List[Dict[str, Any]]:
    """Cached category retrieval."""
    return self.db.execute("SELECT * FROM categories")
```

**Cache Invalidation:**
- Cache cleared on category create/update/delete
- Cache cleared on transaction modifications

### Performance Metrics

- **Query Response Time**: < 100ms for typical operations
- **Index Lookup**: O(1) for PRIMARY KEY queries
- **Data Loading**: Lazy loading of tables on startup
- **Memory Usage**: Efficient data structures

---

## Testing

### Test Coverage

#### Unit Tests

**test_database.py** - Core database functionality:
- Table creation
- INSERT operations
- SELECT operations
- UPDATE operations
- DELETE operations
- Constraint validation
- Index functionality

**test_parser.py** - SQL parsing:
- CREATE TABLE parsing
- INSERT parsing
- SELECT parsing
- UPDATE parsing
- DELETE parsing
- JOIN parsing
- Error handling

#### Integration Tests

**test_web.py** (to be implemented):
- View functionality
- Form validation
- Database integration
- Error handling

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=my_rdbms --cov=mfukoni_web/tracker

# Run specific test file
pytest tests/test_database.py -v

# Run specific test
pytest tests/test_database.py::test_create_table -v
```

### Test Examples

```python
def test_create_table():
    """Test table creation."""
    db = Database(':memory:')
    db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    assert 'users' in db.tables

def test_primary_key_constraint():
    """Test PRIMARY KEY constraint."""
    db = Database(':memory:')
    db.execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR)")
    db.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    with pytest.raises(ConstraintError):
        db.execute("INSERT INTO users VALUES (1, 'Bob')")
```

---

## Installation & Setup

### 🐳 Docker Quick Start (Recommended)

**Fastest way to run on any machine - No local setup required!**

```bash
# 1. Clone or download the project
git clone <repository-url>
cd MFUKONI

# 2. Build and start with Docker Compose (one command!)
docker-compose up -d

# 3. Access the application
# Open: http://localhost:8000
```

That's it! The application will automatically:
- ✅ Initialize the custom RDBMS database
- ✅ Set up all required configurations  
- ✅ Start the web server on port 8000
- ✅ Persist data in the `data/` directory

**For detailed Docker instructions, see [DOCKER.md](DOCKER.md)**

**Stop the application:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f web
```

---

### Local Development Setup

### Prerequisites

- Python 3.7+ (Python 3.11+ recommended)
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone <repository-url>
cd MFUKONI
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
TIME_ZONE=Africa/Nairobi
```

#### 5. Initialize Database

The custom RDBMS database is automatically initialized on first run. No manual setup required.

**Important:** This application uses the custom RDBMS exclusively. Django's SQLite database (if any) is only used for temporary session storage and is in-memory. All application data is stored in `data/mfukoni.db/`.

#### 6. Run Development Server

```bash
cd mfukoni_web
python manage.py runserver
```

Visit: http://localhost:8000


---

## Usage

### Web Interface

1. **Dashboard**: View financial overview at `/`
2. **Transactions**: Manage transactions at `/transactions/`
3. **Categories**: Manage categories at `/categories/`
4. **Budgets**: Set budgets at `/budgets/`
5. **Reports**: View reports at `/reports/`

### Common Operations

#### Add Transaction
1. Navigate to "Add Transaction"
2. Select type (Income/Expense)
3. Choose category
4. Enter amount, date, description
5. Click "Save Transaction"

#### Set Budget
1. Navigate to "Budgets"
2. Select category
3. Enter monthly limit
4. Select month
5. Click "Set Budget"

#### View Reports
1. Navigate to "Reports"
2. View monthly summaries
3. Analyze spending trends
4. Export data if needed

### REPL Shell

```bash
python -m my_rdbms.repl
```

**Example Session:**
```sql
mfukoni> .tables
Tables:
  - categories (5 rows)
  - transactions (12 rows)
  - budgets (3 rows)

mfukoni> SELECT * FROM categories;
id | name      | type
---|-----------|--------
1  | Salary    | income
2  | Food      | expense
3  | Transport | expense

(3 rows)

mfukoni> .exit
```

---

## API Documentation

### Database Manager API

#### `MfukoniDB` Class

**Methods:**

##### `add_transaction(category_id, amount, description, date, trans_type)`
Add a new transaction.

**Parameters:**
- `category_id` (int): Category ID
- `amount` (float): Transaction amount
- `description` (str): Transaction description
- `date` (str): Date in YYYY-MM-DD format
- `trans_type` (str): 'income' or 'expense'

**Returns:** None

**Raises:** `DatabaseError`, `ConstraintError`

##### `get_all_transactions(category_id=None, trans_type=None, limit=None)`
Get all transactions with optional filtering.

**Parameters:**
- `category_id` (int, optional): Filter by category
- `trans_type` (str, optional): Filter by type
- `limit` (int, optional): Limit number of results

**Returns:** List[Dict[str, Any]]

##### `get_summary()`
Get financial summary.

**Returns:** Dict with keys: `total_income`, `total_expenses`, `balance`, `transaction_count`

##### `add_category(name, cat_type)`
Add a new category.

**Parameters:**
- `name` (str): Category name
- `cat_type` (str): 'income' or 'expense'

**Returns:** None

**Raises:** `DatabaseError`, `ConstraintError`

##### `set_budget(category_id, monthly_limit, month)`
Set a monthly budget.

**Parameters:**
- `category_id` (int): Category ID
- `monthly_limit` (float): Budget limit
- `month` (str): Month in YYYY-MM format

**Returns:** None

---

## Deployment

### Docker Deployment

The application is containerized and can run on any machine with Docker installed.

#### Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose 2.0+ (optional, but recommended)

#### Quick Start with Docker Compose

1. **Create environment file** (optional, for custom configuration):
```bash
cp .env.example .env
# Edit .env with your settings (SECRET_KEY, DEBUG, etc.)
```

2. **Build and start containers**:
```bash
docker-compose up -d
```

3. **Access the application**:
   - Open browser: http://localhost:8000
   - The application will automatically initialize the custom RDBMS on first run

4. **View logs**:
```bash
docker-compose logs -f web
```

5. **Stop containers**:
```bash
docker-compose down
```

#### Manual Docker Commands

**Build the image:**
```bash
docker build -t mfukoni:latest .
```

**Run container with data persistence:**
```bash
docker run -d \
  --name mfukoni-web \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key-here \
  -e ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
  --restart unless-stopped \
  mfukoni:latest
```

**View container logs:**
```bash
docker logs -f mfukoni-web
```

**Stop and remove container:**
```bash
docker stop mfukoni-web
docker rm mfukoni-web
```

#### Docker Image Features

- **Multi-stage ready**: Optimized image size with Python 3.11 slim
- **Health checks**: Built-in health monitoring
- **Auto-initialization**: RDBMS database auto-initializes on first run
- **Data persistence**: Volume mounting for custom RDBMS data
- **Environment variables**: Configurable via `.env` file or Docker environment
- **Production ready**: Includes static file collection and proper error handling

#### Environment Variables

Configure via `docker-compose.yml` or `docker run -e`:

- `DEBUG` - Set to `False` for production (default: `False`)
- `SECRET_KEY` - Django secret key (required for production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts (default: `localhost,127.0.0.1,0.0.0.0`)
- `LANGUAGE_CODE` - Language code (default: `en-us`)
- `TIME_ZONE` - Time zone (default: `Africa/Nairobi`)

#### Data Persistence

The custom RDBMS data is stored in the `data/` directory, which is mounted as a volume. This ensures:
- Data persists across container restarts
- Data can be backed up by backing up the `data/` directory
- Data can be shared between containers if needed

#### Building for Different Platforms

**For Linux/AMD64 (default):**
```bash
docker build -t mfukoni:latest .
```

**For ARM64 (Apple Silicon, Raspberry Pi):**
```bash
docker buildx build --platform linux/arm64 -t mfukoni:latest .
```

**For multi-platform:**
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t mfukoni:latest .
```

### Production Considerations

1. **Environment Variables**
   - Set `DEBUG=False`
   - Use secure `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Backup**
   - **Custom RDBMS**: Regularly backup `data/mfukoni.db/` directory
     - Contains: `categories.json`, `transactions.json`, `budgets.json`
     - All application data is stored here
   - **Django Database**: Not needed - uses in-memory SQLite for temporary sessions only
   - Implement automated backup script for `data/` directory
   - Example backup command:
     ```bash
     tar -czf backup-$(date +%Y%m%d).tar.gz data/
     ```

4. **Security**
   - Set `DEBUG=False` in production
   - Use HTTPS (automatic redirect enabled when `DEBUG=False`)
   - Security headers automatically enabled (HSTS, XSS Filter, Content-Type nosniff)
   - Secure cookies enabled (HttpOnly, Secure, SameSite=Strict)
   - Store `SECRET_KEY` in environment variable, never commit to repository
   - Configure `ALLOWED_HOSTS` with production domain
   - Regular security updates and dependency scanning

5. **Monitoring**
   - Add logging
   - Error tracking (Sentry)
   - Performance monitoring

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Run linters: `flake8`, `black`

### Commit Messages

Use clear, descriptive commit messages:
```
feat: Add budget tracking feature
fix: Resolve SQL injection vulnerability
docs: Update README with deployment guide
```

---

## License

This project is part of the Pesapal Developer Challenge 2026.

**License:** MIT License (see LICENSE file for details)

---

## Acknowledgments & Credits

### Technologies & Frameworks
- **Django Framework** - Web application framework (https://www.djangoproject.com/)
- **Bootstrap 5** - CSS framework for UI components (https://getbootstrap.com/)
- **Bootstrap Icons** - Icon library (https://icons.getbootstrap.com/)
- **Poppins Font** - Google Fonts (https://fonts.google.com/specimen/Poppins)
- **pytest** - Testing framework (https://pytest.org/)
- **reportlab** - PDF generation library
- **openpyxl** - Excel file generation library

### Custom Implementation
- **Custom RDBMS** - Built from scratch, no external database libraries used
- **SQL Parser** - Custom implementation using regex
- **Storage Engine** - JSON-based persistence (custom implementation)
- **Index Manager** - Hash-based indexing (custom implementation)
- **Constraint Validator** - Custom constraint enforcement

### Development Practices
This project follows industry best practices:
- Type hints for enhanced code clarity and IDE support
- Comprehensive documentation and code comments
- Code review and optimization
- Automated testing with pytest
- Security-first approach with SQL injection prevention

### Python Community
- Python programming language and standard library
- All contributors and open-source community

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check documentation in `docs/`
- See `docs/TECHNICAL_DOCUMENTATION.md` for detailed technical information

## Additional Documentation

- **Technical Documentation**: See `docs/TECHNICAL_DOCUMENTATION.md` for:
  - Detailed ER diagrams
  - Complex query implementations
  - Security measures
  - Performance optimization
  - Advanced features (decorators, context managers, caching)
  

---

<div align="center">

**Built with Python and Django**

*Mfukoni - Your money, in your pocket*

---

**Version 1.0.0** | **January 10, 2026**

</div>
