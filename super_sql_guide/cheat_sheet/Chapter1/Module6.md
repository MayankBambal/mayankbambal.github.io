# Module 6: ORDER BY Clause

## ORDER BY Basics

**Purpose**: Sorts rows in the result set. **Only way to guarantee order** - without it, order is arbitrary.

**Execution**: After SELECT (aliases usable), before LIMIT.

```sql
-- Basic ORDER BY syntax
SELECT column_list
FROM table_name
[WHERE conditions]
[GROUP BY columns]
[HAVING conditions]
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...
[LIMIT number];
```

---

## Sorting Fundamentals

### Basic Sorting Options

```sql
-- Single column sorting
SELECT name, salary FROM employees ORDER BY salary;           -- ASC (default)
SELECT name, salary FROM employees ORDER BY salary ASC;       -- Explicit ascending
SELECT name, salary FROM employees ORDER BY salary DESC;      -- Descending

-- Multiple column sorting (hierarchical)
SELECT name, department, salary 
FROM employees 
ORDER BY department ASC, salary DESC;  -- Department A-Z, then salary high-low within each dept
```

### What You Can Sort By

```sql
-- Column names
ORDER BY last_name, first_name;

-- Column aliases from SELECT
SELECT first_name + ' ' + last_name AS full_name
FROM employees
ORDER BY full_name;

-- Expressions
ORDER BY LEN(last_name), last_name;

-- Column positions (not recommended - brittle)
ORDER BY 2, 1;  -- Sort by 2nd column, then 1st column
```

---

## NULL Handling in ORDER BY

**Critical Database Differences**:

| DBMS | Default ASC | Default DESC | NULLS FIRST/LAST Support |
|------|-------------|--------------|--------------------------|
| **PostgreSQL, Oracle** | NULLS LAST | NULLS FIRST | ✅ Yes |
| **SQL Server, MySQL** | NULLS FIRST | NULLS LAST | ❌ No (SQL Server/MySQL) |
| **SQLite** | NULLS FIRST | NULLS LAST | ✅ Yes (3.30.0+) |

### Controlling NULL Position

```sql
-- PostgreSQL/Oracle - Direct control
SELECT name, phone
FROM customers
ORDER BY phone NULLS LAST;   -- Put NULLs at end regardless of ASC/DESC

-- SQL Server/MySQL - Workaround
SELECT name, phone
FROM customers
ORDER BY 
    CASE WHEN phone IS NULL THEN 1 ELSE 0 END,  -- NULLs last
    phone;

-- Alternative workaround for NULLs first
ORDER BY 
    CASE WHEN phone IS NULL THEN 0 ELSE 1 END,  -- NULLs first
    phone;
```

### NULL Examples

```sql
-- Sample data with NULLs:
-- Alice, 2020-01-15
-- Bob, NULL
-- Carol, 2019-03-10

-- PostgreSQL: ORDER BY hire_date
-- Result: Carol (2019), Alice (2020), Bob (NULL) - NULLS LAST

-- SQL Server: ORDER BY hire_date  
-- Result: Bob (NULL), Carol (2019), Alice (2020) - NULLS FIRST
```

---

## Advanced ORDER BY Features

### Complex Expressions

```sql
-- Date calculations
SELECT name, hire_date
FROM employees
ORDER BY YEAR(CURRENT_DATE) - YEAR(hire_date) DESC;  -- Years of service

-- String transformations
SELECT product_name, category
FROM products
ORDER BY UPPER(category), LENGTH(product_name);

-- Mathematical operations
SELECT product_name, price, discount_pct
FROM products
ORDER BY (price * (1 - discount_pct/100)) DESC;  -- Final price after discount
```

### Conditional Sorting

```sql
-- Different sort logic based on conditions
SELECT name, department, salary
FROM employees
ORDER BY 
    CASE department
        WHEN 'Sales' THEN salary  -- Sales by salary
        ELSE name                 -- Others by name
    END DESC;

-- Priority-based sorting
SELECT task_name, priority, due_date
FROM tasks
ORDER BY 
    CASE priority
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
        ELSE 4
    END,
    due_date;
```

### Custom Sort Orders

```sql
-- Custom order for specific values
SELECT product_name, size
FROM products
ORDER BY 
    CASE size
        WHEN 'Small' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Large' THEN 3
        WHEN 'Extra Large' THEN 4
        ELSE 5
    END,
    product_name;

-- Day of week ordering
SELECT event_name, day_of_week
FROM events
ORDER BY 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;
```

---

## Performance Optimization

### Indexing for ORDER BY

```sql
-- Single column index
CREATE INDEX idx_employee_salary ON employees(salary);

-- Composite index for multiple ORDER BY columns
CREATE INDEX idx_employee_dept_salary ON employees(department, salary);

-- Query that benefits from composite index
SELECT name, department, salary
FROM employees
ORDER BY department, salary DESC;  -- Uses idx_employee_dept_salary efficiently
```

### Covering Indexes

```sql
-- Index includes all columns needed by query
CREATE INDEX idx_employee_covering 
ON employees(department, salary) 
INCLUDE (name, hire_date);

-- Query satisfied entirely from index
SELECT name, salary, hire_date
FROM employees
WHERE department = 'Sales'
ORDER BY salary DESC;
```

### Performance Considerations

```sql
-- ✅ EFFICIENT: Sorting uses index
SELECT name, salary FROM employees ORDER BY employee_id;

-- ❌ SLOWER: Expression prevents index usage
SELECT name, salary FROM employees ORDER BY UPPER(name);

-- ✅ BETTER: Use computed column or expression index
-- Option 1: Computed column
ALTER TABLE employees ADD name_upper AS UPPER(name);
CREATE INDEX idx_name_upper ON employees(name_upper);
SELECT name, salary FROM employees ORDER BY name_upper;

-- Option 2: Expression index (PostgreSQL)
CREATE INDEX idx_upper_name ON employees(UPPER(name));
SELECT name, salary FROM employees ORDER BY UPPER(name);
```

---

## Common ORDER BY Patterns

### Top N Queries

```sql
-- Top 10 highest paid employees
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10;

-- Bottom 5 performers
SELECT name, performance_score
FROM employees
ORDER BY performance_score ASC
LIMIT 5;
```

### Pagination

```sql
-- Page 1 (first 20 records)
SELECT name, email
FROM customers
ORDER BY customer_id
LIMIT 20 OFFSET 0;

-- Page 2 (records 21-40)
SELECT name, email
FROM customers
ORDER BY customer_id
LIMIT 20 OFFSET 20;
```

### Date-Based Sorting

```sql
-- Most recent first
SELECT order_id, order_date, customer_name
FROM orders
ORDER BY order_date DESC, order_id DESC;

-- Chronological order
SELECT event_name, event_date
FROM events
ORDER BY event_date ASC;

-- Custom date sorting (current year first, then others)
SELECT event_name, event_date
FROM events
ORDER BY 
    CASE WHEN YEAR(event_date) = YEAR(CURRENT_DATE) THEN 0 ELSE 1 END,
    event_date DESC;
```

---

## Stable Sorting and Determinism

### The Stability Problem

```sql
-- Without ORDER BY - results are non-deterministic
SELECT name FROM employees LIMIT 10;  -- Could return different results each time

-- With incomplete ORDER BY - still non-deterministic if duplicates exist
SELECT name, salary FROM employees ORDER BY salary LIMIT 10;  -- If multiple people have same salary

-- Deterministic ORDER BY - includes unique identifier
SELECT name, salary FROM employees ORDER BY salary DESC, employee_id ASC LIMIT 10;
```

### Ensuring Deterministic Results

```sql
-- Always include a unique column for deterministic results
SELECT product_name, price
FROM products
ORDER BY price DESC, product_id ASC;  -- product_id breaks ties

-- For pagination, deterministic ordering is crucial
SELECT customer_name, signup_date
FROM customers
ORDER BY signup_date DESC, customer_id ASC  -- Prevents missing/duplicate records across pages
LIMIT 50 OFFSET 100;
```

---

## Database-Specific Features

### SQL Server Specific

```sql
-- OFFSET/FETCH (SQL Server 2012+)
SELECT name, salary
FROM employees
ORDER BY salary DESC
OFFSET 10 ROWS FETCH NEXT 20 ROWS ONLY;

-- WITH TIES
SELECT TOP 10 WITH TIES name, salary
FROM employees
ORDER BY salary DESC;  -- Includes all employees tied for 10th place salary
```

### MySQL Specific

```sql
-- FIELD() function for custom ordering
SELECT name, department
FROM employees
ORDER BY FIELD(department, 'CEO', 'VP', 'Director', 'Manager', 'Staff');

-- Mixing ASC/DESC with expressions
SELECT product_name, price
FROM products
ORDER BY (price IS NULL), price DESC;  -- NULLs last, then price descending
```

### PostgreSQL Specific

```sql
-- USING operator for custom sorting
SELECT name FROM employees ORDER BY name USING <;  -- Custom operator

-- Array ordering
SELECT customer_name, favorite_products
FROM customers
ORDER BY array_length(favorite_products, 1) DESC;
```

### Oracle Specific

```sql
-- ROWNUM with ORDER BY (requires subquery)
SELECT * FROM (
    SELECT name, salary FROM employees ORDER BY salary DESC
) WHERE ROWNUM <= 10;

-- Advanced NULL handling
SELECT name, commission
FROM employees
ORDER BY commission DESC NULLS LAST;
```

---

## Quick Reference

### ORDER BY Checklist
- ✅ Always use ORDER BY when order matters
- ✅ Include unique column for deterministic results
- ✅ Consider NULL handling across databases
- ✅ Index ORDER BY columns for performance
- ✅ Use column aliases when helpful
- ✅ Be explicit about ASC/DESC for clarity

### Common Patterns
- **Basic sorting**: `ORDER BY column ASC/DESC`
- **Multiple columns**: `ORDER BY col1, col2 DESC`
- **Custom order**: `ORDER BY CASE WHEN...`
- **NULL control**: `ORDER BY column NULLS LAST` (if supported)
- **Deterministic**: `ORDER BY main_column, unique_id`

### Performance Tips
- Create indexes on ORDER BY columns
- Use covering indexes when possible
- Avoid functions in ORDER BY if performance matters
- Consider expression indexes for computed sorts
- Be aware that large OFFSET values can be slow

### Critical Notes
- **No ORDER BY = unpredictable order**
- **NULL handling varies by database**
- **Include unique columns for pagination**
- **ORDER BY happens after SELECT (can use aliases)** 