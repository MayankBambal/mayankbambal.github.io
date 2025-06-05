# Module 2: WHERE Clause and Filtering

## WHERE Clause Basics

**Purpose**: Filters individual rows from the FROM clause result.

**Execution Timing**: After FROM/JOINs, before GROUP BY/HAVING/SELECT.
- Column aliases from SELECT **cannot** be used here (not yet processed)

```sql
-- Basic WHERE syntax
SELECT column_list
FROM table_name
WHERE condition;
```

---

## Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal to | `WHERE age = 25` |
| `!=` or `<>` | Not equal to | `WHERE status != 'inactive'` |
| `<` | Less than | `WHERE price < 100` |
| `>` | Greater than | `WHERE salary > 50000` |
| `<=` | Less than or equal | `WHERE quantity <= 10` |
| `>=` | Greater than or equal | `WHERE score >= 80` |

```sql
-- Multiple comparison examples
WHERE price BETWEEN 10 AND 50;       -- Range (inclusive)
WHERE name LIKE 'John%';              -- Pattern matching  
WHERE category IN ('A', 'B', 'C');   -- List membership
WHERE phone IS NULL;                  -- NULL check
```

---

## Logical Operators

### AND / OR / NOT
```sql
-- AND (higher precedence than OR)
WHERE salary > 50000 AND department = 'IT';

-- OR  
WHERE department = 'Sales' OR department = 'Marketing';

-- NOT
WHERE NOT (status = 'inactive' OR salary IS NULL);

-- Complex logic with parentheses (recommended for clarity)
WHERE (department = 'Sales' AND salary > 60000) 
   OR (department = 'IT' AND experience > 5);
```

**Precedence Order**: NOT → AND → OR
- Always use parentheses for complex conditions to ensure correct logic

---

## Advanced WHERE Operators

### BETWEEN - Range Queries
```sql
WHERE salary BETWEEN 40000 AND 80000;    -- Inclusive range
WHERE hire_date BETWEEN '2020-01-01' AND '2023-12-31';
WHERE NOT quantity BETWEEN 1 AND 10;     -- Outside range
```

### LIKE - Pattern Matching
| Wildcard | Meaning | Example | Matches |
|----------|---------|---------|---------|
| `%` | Any sequence of characters | `'John%'` | John, Johnson, Johnny |
| `_` | Single character | `'Jo_n'` | John, Joan (but not Joann) |

```sql
WHERE name LIKE 'Smith%';              -- Starts with 'Smith'
WHERE email LIKE '%@gmail.com';        -- Ends with '@gmail.com'  
WHERE code LIKE 'A_B_';                -- A + any char + B + any char
WHERE product LIKE '%apple%';          -- Contains 'apple'

-- Escape special characters
WHERE filename LIKE '90\%' ESCAPE '\'; -- Literal % character
```

### IN - List Membership
```sql
WHERE department IN ('Sales', 'Marketing', 'IT');
WHERE customer_id IN (SELECT customer_id FROM vip_customers);

-- NOT IN pitfall with NULLs
WHERE customer_id NOT IN (1, 2, NULL);   -- May return no rows!
-- Better: Use NOT EXISTS or handle NULLs explicitly
```

---

## NULL Handling

### Critical NULL Rules
- `NULL = NULL` is **FALSE** (actually UNKNOWN)
- `NULL != NULL` is **FALSE** 
- Any comparison with NULL returns UNKNOWN
- UNKNOWN in WHERE clause excludes the row

```sql
-- WRONG: Will never find NULL values
WHERE phone_number = NULL;

-- CORRECT: Use IS NULL / IS NOT NULL
WHERE phone_number IS NULL;
WHERE phone_number IS NOT NULL;

-- Complex NULL conditions
WHERE (salary IS NULL OR salary < 30000);
WHERE COALESCE(phone, 'none') = 'none';
```

---

## Query Performance: Sargability

**Sargable** (Search ARGument Able) predicates can use indexes effectively.

### Non-Sargable Examples (Avoid These)
```sql
-- Functions on columns prevent index usage
WHERE UPPER(last_name) = 'SMITH';
WHERE YEAR(order_date) = 2023;
WHERE SUBSTRING(product_code, 1, 3) = 'ABC';
WHERE salary * 12 > 100000;

-- Leading wildcards can't use indexes
WHERE product_name LIKE '%apple%';
```

### Sargable Alternatives
```sql
-- Keep columns "bare" for index usage
WHERE last_name = 'SMITH';                    -- Case-insensitive collation
WHERE order_date >= '2023-01-01' 
  AND order_date < '2024-01-01';              -- Range instead of function
WHERE product_code LIKE 'ABC%';               -- Leading characters known
WHERE salary > 100000/12;                     -- Move calculation to constant

-- Computed columns for complex transformations
-- Create: ALTER TABLE ADD computed_column AS UPPER(last_name);
-- Then: WHERE computed_column = 'SMITH';
```

### Performance Tips
- **Index WHERE columns** - Especially those in frequent queries
- **Most selective conditions first** - Though optimizer usually reorders
- **Avoid OR with different columns** - Consider UNION instead
- **Use EXISTS instead of IN with subqueries** - Often more efficient

---

## Common WHERE Patterns

### Date Range Queries
```sql
-- Last 30 days
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Specific year (sargable)
WHERE order_date >= '2023-01-01' 
  AND order_date < '2024-01-01';

-- This month
WHERE YEAR(order_date) = YEAR(CURRENT_DATE)
  AND MONTH(order_date) = MONTH(CURRENT_DATE);
```

### String Matching
```sql
-- Case-insensitive search (database-dependent)
WHERE LOWER(name) LIKE LOWER('%john%');
-- Or use case-insensitive collation
WHERE name COLLATE SQL_Latin1_General_CP1_CI_AS LIKE '%john%';
```

### Handling Optional Parameters
```sql
-- Dynamic filtering (all conditions optional)
WHERE (@dept_filter IS NULL OR department = @dept_filter)
  AND (@min_salary IS NULL OR salary >= @min_salary)
  AND (@status_filter IS NULL OR status = @status_filter);
```

### Exclusion Patterns
```sql
-- Find customers with no orders
WHERE customer_id NOT IN (
    SELECT customer_id 
    FROM orders 
    WHERE customer_id IS NOT NULL  -- Handle NULLs
);

-- Or using NOT EXISTS (often better performance)
WHERE NOT EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = customers.customer_id
);
```

---

## Database-Specific Features

### Regular Expressions
```sql
-- PostgreSQL
WHERE email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- MySQL  
WHERE email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';

-- SQL Server
WHERE email LIKE '%_@_%._%';  -- Basic pattern only
```

### Full-Text Search
```sql
-- SQL Server
WHERE CONTAINS(description, 'database AND performance');

-- MySQL
WHERE MATCH(title, content) AGAINST('database performance' IN BOOLEAN MODE);

-- PostgreSQL
WHERE to_tsvector('english', content) @@ to_tsquery('database & performance');
```

---

## Quick Reference

### WHERE Clause Checklist
- Use proper comparison operators
- Handle NULL values with IS NULL/IS NOT NULL
- Use parentheses for complex logic
- Write sargable conditions when possible
- Index columns used in WHERE clauses
- Be careful with NOT IN and NULL values
- Consider EXISTS vs IN for subqueries

### Common Mistakes
- Using `= NULL` instead of `IS NULL`
- Forgetting precedence: NOT, AND, OR
- Functions on indexed columns
- NOT IN with potentially NULL lists
- Missing parentheses in complex conditions 