# Module 1: FROM Clause and JOIN Operations

## FROM Clause Basics

**Purpose**: Specifies the source table(s) or views, defining the initial dataset.

### Table Aliases
```sql
FROM employees e                    -- Simple alias
FROM employees AS e                 -- Explicit AS keyword  
FROM very_long_table_name vlt       -- Shorter alias for readability
```

**Rules**:
- Essential for readability and **required** for self-joins
- Once defined, the alias **must** be used consistently throughout the query
- Cannot switch back to original table name after defining alias

### Derived Tables (Subqueries in FROM)
```sql
SELECT d.department, d.avg_salary
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS d                              -- Alias is REQUIRED
WHERE d.avg_salary > 50000;
```

**Key Points**:
- Subquery in FROM clause, treated as temporary virtual table
- **Must be aliased** - required by SQL standard
- Useful for multi-stage processing and complex transformations
- Exists only for the query's duration

---

## JOIN Operations Quick Reference

JOINs combine rows from multiple tables based on related columns. Processed as part of the FROM clause.

### JOIN Types Summary

| JOIN Type | Syntax | Returns | Use Case |
|-----------|--------|---------|----------|
| **INNER JOIN** | `FROM a INNER JOIN b ON a.id = b.id` | Only matching rows from both tables | Standard relationships |
| **LEFT JOIN** | `FROM a LEFT JOIN b ON a.id = b.id` | All left + matched right (NULL if no match) | All primary + related data |
| **RIGHT JOIN** | `FROM a RIGHT JOIN b ON a.id = b.id` | All right + matched left (NULL if no match) | All secondary + related data |
| **FULL OUTER JOIN** | `FROM a FULL OUTER JOIN b ON a.id = b.id` | All rows from both tables | Complete data comparison |
| **CROSS JOIN** | `FROM a CROSS JOIN b` | Cartesian product (every × every) | All combinations |
| **SELF JOIN** | `FROM table a JOIN table b ON a.mgr_id = b.emp_id` | Table joined to itself with aliases | Hierarchical data |

### JOIN Examples

```sql
-- INNER JOIN - only employees with departments
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

-- LEFT JOIN - all employees, department info if available
SELECT e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;

-- SELF JOIN - employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- Multiple JOINs
SELECT e.name, d.department_name, l.location
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
INNER JOIN locations l ON d.location_id = l.location_id;
```

---

## Advanced JOIN Concepts

### Joining on Multiple Columns
```sql
FROM orders o
INNER JOIN order_items oi 
    ON o.order_id = oi.order_id 
    AND o.order_version = oi.order_version;
```

### NULL Handling in JOINs
```sql
-- Standard equality won't match NULLs
ON t1.col = t2.col                    -- NULL ≠ NULL

-- To match NULLs explicitly:
ON (t1.col = t2.col OR (t1.col IS NULL AND t2.col IS NULL))

-- PostgreSQL: IS NOT DISTINCT FROM
ON t1.col IS NOT DISTINCT FROM t2.col

-- MySQL: NULL-safe equality
ON t1.col <=> t2.col
```

### ON vs WHERE in OUTER JOINs

**Critical Difference**:

```sql
-- Condition in ON clause (CORRECT for outer join behavior)
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'shipped';
-- Returns ALL customers, orders only if status = 'shipped'

-- Condition in WHERE clause (May turn into INNER JOIN)
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'shipped';
-- Returns ONLY customers with shipped orders (filters out NULLs)
```

---

## Performance Tips

### Indexing for JOINs
```sql
-- Index the join columns for performance
CREATE INDEX idx_employee_dept ON employees(dept_id);
CREATE INDEX idx_department_id ON departments(dept_id);
```

### Avoiding Non-Sargable Conditions
```sql
-- ❌ Avoid functions in ON clause
ON UPPER(t1.name) = UPPER(t2.name)

-- ✅ Better alternatives
ON t1.name = t2.name                  -- If case doesn't matter
-- Or normalize data at insert/update time
```

### JOIN Order Optimization
- Filter tables with WHERE before joining when possible
- Join most selective tables first (though optimizer usually handles this)
- Consider using subqueries to pre-filter large tables

---

## Common JOIN Patterns

### Finding Unmatched Records
```sql
-- Customers with no orders (anti-join pattern)
SELECT c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;
```

### Existence Checks
```sql
-- Alternative to EXISTS
SELECT DISTINCT c.customer_name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### Update with JOIN
```sql
-- Update based on joined data
UPDATE employees e
SET e.department_name = d.department_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```

---

## Quick Tips

- **Always specify join conditions** - Missing ON clause creates Cartesian product
- **Use table aliases** - Essential for readability and disambiguation  
- **Index join columns** - Critical for performance on large tables
- **OUTER JOIN placement matters** - Condition in ON vs WHERE affects results
- **NULL = NULL is FALSE** - Use IS NULL or special NULL-safe operators
- **Left table = "driving" table** in LEFT JOIN - all its rows are preserved 