# Module 3: GROUP BY and Aggregate Functions

## GROUP BY Basics

**Purpose**: Groups rows with identical values in specified columns into summary rows for use with aggregate functions.

**Execution**: After WHERE, before HAVING/SELECT.

```sql
-- Basic GROUP BY syntax
SELECT column_list, aggregate_functions
FROM table_name
[WHERE conditions]
GROUP BY column_list;
```

---

## Aggregate Functions Reference

| Function | Description | NULL Handling | Return Type |
|----------|-------------|---------------|-------------|
| `COUNT(*)` | Number of rows in group | Counts all rows | Integer |
| `COUNT(column)` | Number of non-NULL values | Ignores NULLs | Integer |
| `COUNT(DISTINCT column)` | Number of unique non-NULL values | Ignores NULLs | Integer |
| `SUM(column)` | Sum of numeric values | Ignores NULLs | Numeric |
| `AVG(column)` | Average of numeric values | Ignores NULLs | Numeric |
| `MIN(column)` | Minimum value | Ignores NULLs | Same as column |
| `MAX(column)` | Maximum value | Ignores NULLs | Same as column |

### Aggregate Function Examples
```sql
-- Basic aggregates
SELECT 
    department,
    COUNT(*) AS total_employees,
    COUNT(salary) AS employees_with_salary,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary,
    MIN(salary) AS lowest_salary,
    MAX(salary) AS highest_salary
FROM employees
GROUP BY department;

-- DISTINCT counting
SELECT 
    department,
    COUNT(DISTINCT job_title) AS unique_job_titles,
    COUNT(DISTINCT YEAR(hire_date)) AS hiring_years
FROM employees
GROUP BY department;
```

---

## GROUP BY Rules

### The Golden Rule
**Non-aggregated columns in SELECT must be in GROUP BY**

```sql
-- WRONG: name not in GROUP BY, not aggregated
SELECT department, name, COUNT(*)
FROM employees
GROUP BY department;

-- CORRECT: Only grouped columns and aggregates
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;

-- ALSO CORRECT: All non-aggregate columns in GROUP BY
SELECT department, job_title, COUNT(*)
FROM employees
GROUP BY department, job_title;
```

### Multiple Column Grouping
```sql
-- Groups by unique combinations of department AND job_title
SELECT 
    department, 
    job_title, 
    COUNT(*) AS count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department, job_title
ORDER BY department, job_title;
```

**Result creates groups like**:
- (Sales, Manager)
- (Sales, Associate) 
- (IT, Developer)
- (IT, Manager)

---

## Advanced GROUP BY Features

### Grouping by Expressions
```sql
-- Group by calculated values
SELECT 
    YEAR(hire_date) AS hire_year,
    COUNT(*) AS hires_count
FROM employees
GROUP BY YEAR(hire_date)
ORDER BY hire_year;

-- Group by CASE expressions
SELECT 
    CASE 
        WHEN salary < 50000 THEN 'Low'
        WHEN salary < 80000 THEN 'Medium'
        ELSE 'High'
    END AS salary_bracket,
    COUNT(*) AS employee_count
FROM employees
GROUP BY 
    CASE 
        WHEN salary < 50000 THEN 'Low'
        WHEN salary < 80000 THEN 'Medium'
        ELSE 'High'
    END;
```

### Conditional Aggregation
```sql
-- Count specific conditions within groups
SELECT 
    department,
    COUNT(*) AS total_employees,
    COUNT(CASE WHEN salary > 60000 THEN 1 END) AS high_earners,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS female_count,
    AVG(CASE WHEN job_title LIKE '%Manager%' THEN salary END) AS avg_manager_salary
FROM employees
GROUP BY department;
```

---

## NULL Handling in Aggregates

### How Aggregates Handle NULLs
```sql
-- Sample data:
-- Alice, Sales, 50000
-- Bob, Sales, NULL
-- Carol, Sales, 55000

SELECT 
    department,
    COUNT(*) AS all_rows,           -- Result: 3 (counts Bob)
    COUNT(salary) AS with_salary,   -- Result: 2 (ignores Bob)
    SUM(salary) AS total_salary,    -- Result: 105000 (ignores Bob)
    AVG(salary) AS avg_salary       -- Result: 52500 (ignores Bob)
FROM employees
WHERE department = 'Sales'
GROUP BY department;
```

### NULL Grouping
- All NULL values in a grouping column form **one group**
- Use `COALESCE()` or `ISNULL()` to replace NULLs with meaningful values

```sql
-- Group NULL departments as 'Unassigned'
SELECT 
    COALESCE(department, 'Unassigned') AS dept,
    COUNT(*) AS employee_count
FROM employees
GROUP BY COALESCE(department, 'Unassigned');
```

---

## Performance Optimization

### Indexing for GROUP BY
```sql
-- Create composite index for common GROUP BY columns
CREATE INDEX idx_emp_dept_title ON employees(department, job_title);

-- Covering index includes aggregated columns
CREATE INDEX idx_emp_dept_covering ON employees(department) INCLUDE (salary, hire_date);
```

### Filtering Before Grouping
```sql
-- EFFICIENT: Filter with WHERE before grouping
SELECT department, AVG(salary)
FROM employees
WHERE hire_date >= '2020-01-01'  -- Reduces rows before grouping
GROUP BY department;

-- LESS EFFICIENT: Filter after grouping
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING department IN ('Sales', 'IT');  -- Better to use WHERE
```

---

## Common GROUP BY Patterns

### Finding Duplicates
```sql
-- Find duplicate records
SELECT 
    email, 
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

### Top N per Group
```sql
-- Highest paid employee per department (using window functions)
WITH ranked_employees AS (
    SELECT 
        name, 
        department, 
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
    FROM employees
)
SELECT name, department, salary
FROM ranked_employees 
WHERE rank = 1;
```

### Summary Statistics
```sql
-- Comprehensive department statistics
SELECT 
    department,
    COUNT(*) AS employee_count,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    AVG(salary) AS avg_salary,
    STDDEV(salary) AS salary_stddev,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) AS male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) AS female_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC;
```

### Time-Based Grouping
```sql
-- Monthly sales summary
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;
```

---

## Database-Specific Features

### GROUP BY Extensions

**MySQL - GROUP BY with ROLLUP**:
```sql
-- Adds subtotals and grand total
SELECT department, job_title, COUNT(*)
FROM employees
GROUP BY department, job_title WITH ROLLUP;
```

**SQL Server - GROUPING SETS**:
```sql
-- Multiple grouping levels in one query
SELECT department, job_title, COUNT(*)
FROM employees
GROUP BY GROUPING SETS (
    (department, job_title),  -- Department + job title
    (department),             -- Department only
    ()                        -- Grand total
);
```

**PostgreSQL - CUBE and ROLLUP**:
```sql
-- All possible grouping combinations
SELECT department, job_title, COUNT(*)
FROM employees
GROUP BY CUBE(department, job_title);
```

### SELECT Alias Usage
```sql
-- Some databases allow aliases in GROUP BY
-- MySQL, PostgreSQL (sometimes)
SELECT 
    YEAR(hire_date) AS hire_year,
    COUNT(*) AS hire_count
FROM employees
GROUP BY hire_year;  -- Using alias

-- Always works (standard SQL)
SELECT 
    YEAR(hire_date) AS hire_year,
    COUNT(*) AS hire_count
FROM employees
GROUP BY YEAR(hire_date);  -- Repeat expression
```

---

## Quick Reference

### GROUP BY Checklist
- Non-aggregate SELECT columns must be in GROUP BY
- Use appropriate aggregate functions for your needs
- Consider NULL handling in your aggregates
- Filter with WHERE before grouping when possible
- Index GROUP BY columns for performance
- Use HAVING to filter groups, not rows

### Common Mistakes
- Selecting non-grouped, non-aggregate columns
- Using HAVING for row filtering instead of WHERE
- Forgetting that COUNT(*) includes NULLs, but COUNT(column) doesn't
- Not considering NULL values in grouping columns
- Poor indexing strategy for grouped queries

### When to Use GROUP BY
- **Counting** records by category
- **Summing/averaging** values by group
- **Finding duplicates** in data
- **Creating reports** with subtotals
- **Statistical analysis** by group 