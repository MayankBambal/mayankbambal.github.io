# Module 5: SELECT Clause and Expressions

## SELECT Basics

**Purpose**: Specifies columns, expressions, and computed values for the final result set.

**Execution**: After FROM, WHERE, GROUP BY, HAVING; before ORDER BY, LIMIT.

```sql
-- Basic SELECT syntax
SELECT [DISTINCT] expression_list
FROM table_name
[WHERE conditions]
[GROUP BY columns]
[HAVING conditions]
[ORDER BY columns]
[LIMIT number];
```

---

## SELECT Best Practices

### Avoid SELECT *

```sql
-- AVOID: SELECT * problems
SELECT * FROM employees;
```

**Issues with SELECT ***:
- **Performance**: Unnecessary data transfer, prevents covering index optimization
- **Maintainability**: Brittle to schema changes
- **Unpredictable**: Column order may change
- **Bandwidth**: Wastes network resources

```sql
-- BETTER: Be explicit about needed columns
SELECT employee_id, name, department, salary
FROM employees;
```

**Exception**: SELECT * is acceptable for:
- Ad-hoc queries and development
- Small result sets
- When you genuinely need all columns

### Column Aliases

```sql
-- Basic alias syntax
SELECT 
    first_name AS "First Name",           -- Quoted for spaces
    last_name AS surname,                 -- Simple alias
    salary * 12 AS annual_salary,         -- Calculated alias
    department AS dept                    -- Shorter name
FROM employees;

-- Alternative syntax (some databases)
SELECT 
    first_name "First Name",              -- Without AS
    last_name surname
FROM employees;
```

**Alias Rules**:
- Can be used in ORDER BY (processed after SELECT)
- Cannot be used in WHERE, GROUP BY, HAVING (processed before SELECT)
- Use quotes for aliases with spaces or special characters

---

## SELECT DISTINCT

**Purpose**: Returns unique rows based on all selected columns.

```sql
-- Remove duplicate departments
SELECT DISTINCT department
FROM employees;

-- Unique combinations of department and job title
SELECT DISTINCT department, job_title
FROM employees;

-- DISTINCT with expressions
SELECT DISTINCT 
    department,
    CASE 
        WHEN salary > 60000 THEN 'High'
        ELSE 'Standard'
    END AS salary_category
FROM employees;
```

### DISTINCT Considerations

**Performance**: Can be resource-intensive due to sorting/hashing required.

**NULL Handling**: NULLs are treated as equal for distinctness.

**Scope**: DISTINCT applies to the entire SELECT list, not individual columns.

```sql
-- This finds distinct combinations of (name, salary)
SELECT DISTINCT name, salary FROM employees;

-- If you want distinct names only:
SELECT DISTINCT name FROM employees;
```

---

## Expressions in SELECT

### Arithmetic Operations

```sql
SELECT 
    product_name,
    price,
    quantity,
    price * quantity AS total_value,           -- Multiplication
    price * 1.1 AS price_with_tax,            -- Addition
    (price * quantity) * 0.1 AS discount,     -- Parentheses for precedence
    ROUND(price / quantity, 2) AS unit_price   -- Division with rounding
FROM order_items;
```

**Operator Precedence**: `()` → `*`, `/`, `%` → `+`, `-`

### String Functions

```sql
SELECT 
    -- Concatenation (database-specific)
    first_name + ' ' + last_name AS full_name,        -- SQL Server
    CONCAT(first_name, ' ', last_name) AS full_name,  -- MySQL, PostgreSQL
    first_name || ' ' || last_name AS full_name,      -- PostgreSQL, Oracle
    
    -- String manipulation
    UPPER(last_name) AS surname_upper,
    LOWER(email) AS email_lower,
    SUBSTRING(phone, 1, 3) AS area_code,
    TRIM(description) AS clean_description,
    LENGTH(product_name) AS name_length,
    LEFT(product_code, 2) AS category_code             -- SQL Server
FROM employees;
```

### Date Functions

```sql
SELECT 
    hire_date,
    -- Current date/time (database-specific)
    GETDATE() AS current_datetime,                     -- SQL Server
    NOW() AS current_datetime,                         -- MySQL
    CURRENT_TIMESTAMP AS current_datetime,             -- Standard SQL
    
    -- Date arithmetic
    DATEADD(YEAR, 1, hire_date) AS anniversary,       -- SQL Server
    DATE_ADD(hire_date, INTERVAL 1 YEAR) AS anniversary, -- MySQL
    hire_date + INTERVAL '1 year' AS anniversary,     -- PostgreSQL
    
    -- Date parts
    YEAR(hire_date) AS hire_year,
    MONTH(hire_date) AS hire_month,
    EXTRACT(YEAR FROM hire_date) AS hire_year,         -- Standard SQL
    
    -- Date formatting
    FORMAT(hire_date, 'yyyy-MM-dd') AS formatted_date -- SQL Server
FROM employees;
```

### Numeric Functions

```sql
SELECT 
    salary,
    ROUND(salary, -3) AS salary_rounded_thousands,     -- Round to nearest 1000
    ABS(budget_variance) AS absolute_variance,
    CEILING(3.14) AS ceiling_value,                    -- 4
    FLOOR(3.99) AS floor_value,                        -- 3
    POWER(2, 3) AS power_result,                       -- 8
    SQRT(16) AS square_root                            -- 4
FROM financial_data;
```

---

## Conditional Logic with CASE

### Simple CASE Expression

```sql
SELECT 
    employee_name,
    department,
    CASE department
        WHEN 'Sales' THEN 'Revenue Generator'
        WHEN 'IT' THEN 'Technology Support'
        WHEN 'HR' THEN 'People Operations'
        ELSE 'Other Department'
    END AS department_description
FROM employees;
```

### Searched CASE Expression (More Flexible)

```sql
SELECT 
    employee_name,
    salary,
    CASE 
        WHEN salary > 80000 THEN 'High'
        WHEN salary > 50000 THEN 'Medium'
        WHEN salary > 30000 THEN 'Low'
        ELSE 'Entry Level'
    END AS salary_category,
    
    CASE 
        WHEN hire_date >= CURRENT_DATE - INTERVAL '1 year' THEN 'New'
        WHEN hire_date >= CURRENT_DATE - INTERVAL '5 years' THEN 'Experienced'
        ELSE 'Veteran'
    END AS tenure_category
FROM employees;
```

### Complex CASE Logic

```sql
SELECT 
    product_name,
    category,
    price,
    inventory_count,
    CASE 
        WHEN inventory_count = 0 THEN 'Out of Stock'
        WHEN inventory_count < 10 AND price > 100 THEN 'Low Stock - High Value'
        WHEN inventory_count < 10 THEN 'Low Stock'
        WHEN inventory_count > 100 THEN 'Overstocked'
        ELSE 'Normal Stock'
    END AS inventory_status
FROM products;
```

---

## NULL Handling in SELECT

### Common NULL Functions

```sql
SELECT 
    customer_name,
    phone,
    -- Replace NULL with default value (database-specific)
    COALESCE(phone, 'No phone provided') AS contact_phone,  -- Standard SQL
    ISNULL(phone, 'No phone') AS contact_phone,            -- SQL Server
    IFNULL(phone, 'No phone') AS contact_phone,            -- MySQL
    NVL(phone, 'No phone') AS contact_phone,               -- Oracle
    
    -- Check for NULL
    CASE 
        WHEN phone IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS phone_status
FROM customers;
```

### COALESCE with Multiple Values

```sql
SELECT 
    customer_name,
    -- Use first non-NULL value
    COALESCE(mobile_phone, home_phone, work_phone, 'No phone') AS best_contact,
    
    -- Complex NULL handling
    CASE 
        WHEN email IS NOT NULL AND phone IS NOT NULL THEN 'Complete Contact'
        WHEN email IS NOT NULL THEN 'Email Only'
        WHEN phone IS NOT NULL THEN 'Phone Only'
        ELSE 'No Contact Info'
    END AS contact_completeness
FROM customers;
```

---

## Advanced SELECT Features

### Type Conversion

```sql
SELECT 
    order_id,
    -- Explicit type casting
    CAST(order_total AS INTEGER) AS total_rounded,
    CAST(order_date AS VARCHAR(10)) AS date_string,
    
    -- Database-specific conversion
    CONVERT(VARCHAR(10), order_date, 120) AS iso_date,     -- SQL Server
    TO_CHAR(order_date, 'YYYY-MM-DD') AS formatted_date,  -- Oracle/PostgreSQL
    DATE_FORMAT(order_date, '%Y-%m-%d') AS formatted_date -- MySQL
FROM orders;
```

### Scalar Subqueries

```sql
SELECT 
    e.employee_name,
    e.department,
    e.salary,
    -- Correlated scalar subquery
    (SELECT AVG(salary) 
     FROM employees e2 
     WHERE e2.department = e.department) AS dept_avg_salary,
     
    -- Performance consideration: this runs for each row!
    e.salary - (SELECT AVG(salary) 
                FROM employees e2 
                WHERE e2.department = e.department) AS salary_vs_dept_avg
FROM employees e;
```

**Performance Warning**: Scalar subqueries can be slow. Consider JOINs or window functions instead.

### Window Functions (Advanced)

```sql
SELECT 
    employee_name,
    department,
    salary,
    -- Ranking within department
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    
    -- Running totals
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date) as running_payroll,
    
    -- Comparisons
    LAG(salary) OVER (ORDER BY hire_date) as previous_hire_salary
FROM employees;
```

---

## Performance Considerations

### Covering Indexes for SELECT

```sql
-- Index includes all columns needed by query
CREATE INDEX idx_emp_covering 
ON employees(department) 
INCLUDE (employee_name, salary, hire_date);

-- Query can be satisfied entirely from index
SELECT employee_name, salary, hire_date
FROM employees
WHERE department = 'Sales';
```

### Function Usage Impact

```sql
-- SLOWER: Functions in SELECT can be CPU-intensive
SELECT 
    UPPER(CONCAT(first_name, ' ', last_name)) AS full_name_upper,
    COMPLEX_UDF(salary) AS processed_salary  -- User-defined functions are slow
FROM employees;

-- FASTER: Pre-computed or simpler alternatives
SELECT 
    full_name_upper,  -- Computed column or view
    salary * 1.1 AS processed_salary  -- Simple expression
FROM employees;
```

---

## Database-Specific Features

### SQL Server Specific

```sql
SELECT 
    employee_id,
    -- XML operations
    personal_data.value('(/person/age)[1]', 'int') AS age,
    
    -- JSON operations (SQL Server 2016+)
    JSON_VALUE(preferences, '$.theme') AS preferred_theme,
    
    -- String aggregation
    STRING_AGG(skill, ', ') WITHIN GROUP (ORDER BY skill) AS skills_list
FROM employees;
```

### PostgreSQL Specific

```sql
SELECT 
    customer_name,
    -- Array operations
    favorite_products[1] AS top_product,
    array_length(favorite_products, 1) AS product_count,
    
    -- JSON operations
    profile->>'age' AS age,
    profile->'preferences'->>'theme' AS theme
FROM customers;
```

### MySQL Specific

```sql
SELECT 
    product_name,
    -- Group concatenation
    GROUP_CONCAT(DISTINCT category ORDER BY category SEPARATOR '; ') AS categories,
    
    -- Regular expressions
    REGEXP_REPLACE(description, '[0-9]+', 'X') AS cleaned_description
FROM products
GROUP BY product_name;
```

---

## Quick Reference

### SELECT Checklist
- Specify only needed columns (avoid SELECT *)
- Use meaningful aliases for expressions
- Handle NULL values appropriately
- Consider performance impact of functions
- Use CASE for conditional logic
- Be aware of expression evaluation order

### Common Patterns
- **Calculations**: `price * quantity`, `salary * 12`
- **String building**: `CONCAT(first_name, ' ', last_name)`
- **Categorization**: `CASE WHEN...THEN...END`
- **NULL handling**: `COALESCE(column, default_value)`
- **Type conversion**: `CAST(column AS data_type)`

### Performance Tips
- Use covering indexes for frequently selected columns
- Avoid complex functions in SELECT when possible
- Consider computed columns for expensive expressions
- Use window functions instead of correlated subqueries
- Be mindful of DISTINCT performance on large result sets 