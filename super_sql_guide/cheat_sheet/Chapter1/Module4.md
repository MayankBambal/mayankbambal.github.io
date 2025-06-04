# Module 4: HAVING Clause

## HAVING Basics

**Purpose**: Filters groups created by GROUP BY, typically using aggregate function results.

**Execution**: After GROUP BY (aggregates computed), before SELECT/ORDER BY.

```sql
-- Basic HAVING syntax
SELECT column_list, aggregate_functions
FROM table_name
[WHERE row_conditions]
GROUP BY column_list
HAVING group_conditions;
```

---

## HAVING vs WHERE - Critical Differences

| Feature | WHERE | HAVING |
|---------|-------|--------|
| **Filters** | Individual rows | Groups (summary rows) |
| **Timing** | Before GROUP BY | After GROUP BY |
| **Aggregate Functions** | Cannot directly use | Can (and typically does) use |
| **Prerequisite** | No GROUP BY needed | Typically requires GROUP BY |
| **Performance** | Reduces data before grouping | Filters after grouping |

### Practical Examples

```sql
-- WHERE: Filter rows before grouping
SELECT department, COUNT(*) AS emp_count
FROM employees
WHERE hire_date >= '2020-01-01'  -- Filter individual employees first
GROUP BY department;

-- HAVING: Filter groups after aggregation
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;             -- Only departments with >5 employees

-- BOTH: Filter rows first, then filter groups
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE status = 'Active'          -- Only active employees
GROUP BY department
HAVING AVG(salary) > 60000;      -- Only high-paying departments
```

---

## Common HAVING Use Cases

### Filtering by Aggregate Values

```sql
-- Departments with many employees
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

-- High-spending customers
SELECT customer_id, SUM(order_total) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(order_total) > 5000;

-- Products with high average ratings
SELECT product_id, AVG(rating) AS avg_rating, COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
HAVING AVG(rating) > 4.0 AND COUNT(*) >= 10;
```

### Multiple Aggregate Conditions

```sql
-- Complex department analysis
SELECT 
    department,
    COUNT(*) AS emp_count,
    AVG(salary) AS avg_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5                    -- At least 6 employees
   AND AVG(salary) > 50000             -- Good average salary
   AND MAX(salary) < 100000;           -- No extremely high salaries
```

### Date-Based Group Filtering

```sql
-- Months with high sales volume
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_revenue
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
HAVING COUNT(*) > 100               -- Busy months
   AND SUM(total_amount) > 50000;   -- High revenue months
```

---

## Advanced HAVING Patterns

### Using HAVING with Subqueries

```sql
-- Departments with above-average employee count
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > (
    SELECT AVG(dept_size)
    FROM (
        SELECT COUNT(*) AS dept_size
        FROM employees
        GROUP BY department
    ) AS dept_counts
);
```

### Conditional Aggregation in HAVING

```sql
-- Departments with high percentage of senior employees
SELECT 
    department,
    COUNT(*) AS total_employees,
    COUNT(CASE WHEN YEAR(CURRENT_DATE) - YEAR(hire_date) > 5 THEN 1 END) AS senior_count
FROM employees
GROUP BY department
HAVING COUNT(CASE WHEN YEAR(CURRENT_DATE) - YEAR(hire_date) > 5 THEN 1 END) 
       > COUNT(*) * 0.5;  -- More than 50% are senior
```

### HAVING with Ranking Functions

```sql
-- Top 3 departments by average salary
SELECT 
    department,
    AVG(salary) AS avg_salary,
    COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING AVG(salary) >= (
    SELECT MIN(top_salaries)
    FROM (
        SELECT AVG(salary) AS top_salaries
        FROM employees
        GROUP BY department
        ORDER BY AVG(salary) DESC
        LIMIT 3
    ) AS top_depts
);
```

---

## HAVING Without GROUP BY

**Use Case**: Treating entire result set as one group.

```sql
-- Only show results if company-wide average salary is above threshold
SELECT AVG(salary) AS company_average
FROM employees
HAVING AVG(salary) > 55000;

-- Summary statistics only if we have enough data
SELECT 
    COUNT(*) AS total_employees,
    AVG(salary) AS avg_salary,
    STDDEV(salary) AS salary_stddev
FROM employees
HAVING COUNT(*) >= 100;  -- Only if we have at least 100 employees
```

---

## Performance Considerations

### Efficient HAVING Usage

```sql
-- ✅ GOOD: Filter non-aggregate conditions in WHERE
SELECT department, AVG(salary)
FROM employees
WHERE department IN ('Sales', 'IT', 'Marketing')  -- Filter rows first
GROUP BY department
HAVING AVG(salary) > 60000;                       -- Then filter groups

-- ❌ LESS EFFICIENT: Using HAVING for non-aggregate filtering
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING department IN ('Sales', 'IT', 'Marketing') -- Works, but inefficient
   AND AVG(salary) > 60000;
```

### Index Considerations

```sql
-- Index supporting both WHERE and GROUP BY
CREATE INDEX idx_emp_status_dept ON employees(status, department);

-- Query benefits from the index
SELECT department, COUNT(*), AVG(salary)
FROM employees
WHERE status = 'Active'    -- Uses index for filtering
GROUP BY department        -- Uses index for grouping
HAVING COUNT(*) > 5;       -- Applied after grouping
```

---

## Common HAVING Patterns

### Finding Outliers

```sql
-- Customers with unusually high order frequency
SELECT 
    customer_id,
    COUNT(*) AS order_count,
    AVG(order_total) AS avg_order
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY customer_id
HAVING COUNT(*) > (
    SELECT AVG(orders_per_customer) * 2
    FROM (
        SELECT COUNT(*) AS orders_per_customer
        FROM orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
        GROUP BY customer_id
    ) AS customer_counts
);
```

### Data Quality Checks

```sql
-- Find potential duplicate customers
SELECT 
    email,
    COUNT(*) AS account_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Products with inconsistent pricing
SELECT 
    product_id,
    COUNT(DISTINCT price) AS price_variations,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM order_items
GROUP BY product_id
HAVING COUNT(DISTINCT price) > 1
   AND (MAX(price) - MIN(price)) / MIN(price) > 0.1; -- >10% variation
```

### Business Intelligence Queries

```sql
-- High-value customer segments
SELECT 
    customer_type,
    COUNT(*) AS customer_count,
    AVG(total_orders) AS avg_orders,
    AVG(total_spent) AS avg_spent
FROM (
    SELECT 
        c.customer_type,
        COUNT(o.order_id) AS total_orders,
        COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_type
) AS customer_summary
GROUP BY customer_type
HAVING COUNT(*) > 10                -- Significant segment size
   AND AVG(total_spent) > 1000;     -- High-value segment
```

---

## Database-Specific Features

### MySQL - HAVING with Variables

```sql
SET @min_count = 5;

SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > @min_count;
```

### SQL Server - HAVING with Window Functions

```sql
-- Departments above median size
SELECT 
    department,
    COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > (
    SELECT PERCENTILE_CONT(0.5) 
    WITHIN GROUP (ORDER BY dept_size)
    FROM (
        SELECT COUNT(*) AS dept_size
        FROM employees
        GROUP BY department
    ) AS sizes
);
```

### PostgreSQL - HAVING with Array Functions

```sql
-- Departments with diverse job titles
SELECT 
    department,
    COUNT(*) AS emp_count,
    COUNT(DISTINCT job_title) AS unique_titles
FROM employees
GROUP BY department
HAVING COUNT(DISTINCT job_title) >= 3;
```

---

## Quick Reference

### HAVING Checklist
- ✅ Use HAVING to filter groups based on aggregate values
- ✅ Put non-aggregate filters in WHERE, not HAVING
- ✅ HAVING comes after GROUP BY in query order
- ✅ Can use multiple conditions with AND/OR
- ✅ Can reference any aggregate function in HAVING
- ✅ Consider performance: WHERE filters before grouping

### When to Use HAVING
- **Filter by aggregate values**: COUNT(*) > 10, AVG(salary) > 50000
- **Complex group conditions**: Multiple aggregate criteria
- **Business rules**: "Show only departments with >5 employees"
- **Data quality**: Finding duplicates, outliers
- **Top/Bottom N groups**: Combined with ORDER BY and LIMIT

### Common Mistakes
- ❌ Using HAVING for row filtering instead of WHERE
- ❌ Forgetting that HAVING requires GROUP BY (usually)
- ❌ Putting HAVING before GROUP BY
- ❌ Not considering performance impact of complex HAVING conditions 