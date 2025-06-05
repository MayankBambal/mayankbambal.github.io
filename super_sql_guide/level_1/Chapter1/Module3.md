# Module 3: Grouping and Counting - GROUP BY and Aggregate Functions

Sometimes you don't want to see individual rows - you want to see summaries. For example, instead of seeing every single employee, you might want to know "how many employees are in each department?" That's where GROUP BY and aggregate functions come in!

## 3.1. What GROUP BY Does

### The basic idea

GROUP BY takes rows that have something in common and groups them together so you can count, add up, or calculate averages for each group.

Think of it like sorting a deck of cards by suit - you group all the hearts together, all the spades together, etc. Then you can count how many cards are in each suit.

```sql
-- Instead of seeing every individual employee:
-- Alice, Sales
-- Bob, Sales  
-- Carol, Marketing
-- Dave, Marketing

-- GROUP BY lets you see summaries:
-- Sales: 2 employees
-- Marketing: 2 employees
```

### When it happens

GROUP BY comes after WHERE in our processing order:

```
📊 SQL Processing Flow:

┌─────────────┐
│    FROM     │ ── Get the data from tables
└─────────────┘
      ▼
┌─────────────┐
│   WHERE     │ ── Filter individual rows
└─────────────┘
      ▼
┌─────────────┐
│  GROUP BY   │ ── Group the remaining rows ⭐ (YOU ARE HERE)
└─────────────┘
      ▼
┌─────────────┐
│   SELECT    │ ── Show the summary for each group
└─────────────┘
```

## 3.2. Basic Aggregate Functions (Counting and Calculating)

These functions do the actual calculations on your groups:

### COUNT - How many?
- **COUNT(*)** - Counts all rows in each group
- **COUNT(column_name)** - Counts rows where that column isn't empty

```sql
-- How many employees are in each department?
SELECT department, COUNT(*) AS employee_count
FROM employees  
GROUP BY department
```

### SUM - Add them up
```sql
-- What's the total salary expense for each department?
SELECT department, SUM(salary) AS total_salary
FROM employees
GROUP BY department
```

### AVG - What's the average?
```sql
-- What's the average salary in each department?
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
```

### MIN and MAX - Smallest and largest
```sql
-- What are the lowest and highest salaries in each department?
SELECT department, MIN(salary) AS lowest_salary, MAX(salary) AS highest_salary
FROM employees
GROUP BY department
```

## 3.3. The Golden Rule of GROUP BY

**Important rule**: If you use GROUP BY, every column in your SELECT that isn't inside an aggregate function (COUNT, SUM, AVG, etc.) MUST be in your GROUP BY clause.

```sql
-- WRONG - name isn't in GROUP BY, but it's not in an aggregate function
SELECT department, name, COUNT(*)
FROM employees
GROUP BY department

-- RIGHT - only department and aggregate functions in SELECT
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department

-- ALSO RIGHT - both department and name are in GROUP BY
SELECT department, name, COUNT(*)
FROM employees  
GROUP BY department, name
```

Why this rule? When you group by department, SQL creates one row per department. But if there are multiple employees in each department, SQL doesn't know which employee name to show for that department row.

## 3.4. Common GROUP BY Examples

### Example 1: Counting by category
```sql
-- How many products are in each category?
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
```

**Sample Results:**
| category    | product_count |
|-------------|---------------|
| Electronics | 15            |
| Clothing    | 23            |
| Books       | 8             |

### Example 2: Sales totals by month
```sql
-- Total sales for each month in 2023
SELECT MONTH(order_date) AS month, SUM(sale_amount) AS total_sales
FROM orders
WHERE YEAR(order_date) = 2023
GROUP BY MONTH(order_date)
ORDER BY month
```

### Example 3: Multiple grouping columns
```sql
-- Average salary by department AND job title
SELECT department, job_title, AVG(salary) AS avg_salary
FROM employees
GROUP BY department, job_title
```

This creates groups for each unique combination of department and job title (like "Sales-Manager", "Sales-Associate", "IT-Developer", etc.).

## 3.5. Dealing with Empty Values (NULL)

Aggregate functions handle empty (NULL) values in a specific way:

- **COUNT(*)** counts all rows, including those with empty values
- **COUNT(column_name)** only counts rows where that column isn't empty
- **SUM, AVG, MIN, MAX** ignore empty values

```sql
-- employees table:
-- Alice, Sales, 50000
-- Bob, Sales, NULL (salary missing)
-- Carol, Marketing, 60000

SELECT department, COUNT(*), COUNT(salary), AVG(salary)
FROM employees
GROUP BY department
```

**Results:**
| department | COUNT(*) | COUNT(salary) | AVG(salary) |
|------------|----------|---------------|-------------|
| Sales      | 2        | 1             | 50000       |
| Marketing  | 1        | 1             | 60000       |

Notice how Bob is counted in COUNT(*) but not in COUNT(salary) or AVG(salary) because his salary is missing.

## 3.6. Common GROUP BY Mistakes

### 1. Forgetting to group by non-aggregate columns
```sql
-- WRONG - city isn't in an aggregate function but also not in GROUP BY
SELECT city, COUNT(*) 
FROM customers
GROUP BY country

-- RIGHT  
SELECT country, COUNT(*)
FROM customers
GROUP BY country

-- OR if you want city too:
SELECT country, city, COUNT(*)
FROM customers  
GROUP BY country, city
```

### 2. Misunderstanding what gets grouped
```sql
-- This groups by each unique combination of department AND salary
-- So employees with the same department but different salaries are in different groups
SELECT department, salary, COUNT(*)
FROM employees
GROUP BY department, salary

-- If you want to group just by department:
SELECT department, COUNT(*), AVG(salary)
FROM employees
GROUP BY department
```

### 3. Trying to filter groups with WHERE instead of HAVING
```sql
-- WRONG - you can't filter groups with WHERE
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department  
WHERE COUNT(*) > 5

-- RIGHT - use HAVING to filter groups (we'll learn this in the next module)
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
```

## 3.7. Practice Questions

### Basic Questions:

**"What does GROUP BY do?"**

GROUP BY groups rows that have the same values in specified columns, so you can calculate summaries (like counts, sums, averages) for each group instead of seeing individual rows.

**"What's the difference between COUNT(*) and COUNT(column_name)?"**

- COUNT(*) counts all rows in each group, including rows with missing (NULL) values
- COUNT(column_name) only counts rows where that specific column has a value (not NULL)

**"If you use GROUP BY, what rule must you follow for your SELECT clause?"**

Every column in your SELECT that isn't inside an aggregate function (COUNT, SUM, AVG, etc.) must also be listed in your GROUP BY clause.

### Practice Scenarios:

**"Count how many customers are in each city:"**

```sql
SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city
```

**"Find the total sales amount for each product:"**

```sql
SELECT product_name, SUM(sale_amount) AS total_sales
FROM sales
GROUP BY product_name
```

**"Calculate the average order value for each customer:"**

```sql
SELECT customer_id, AVG(order_total) AS average_order_value
FROM orders
GROUP BY customer_id
```

**"Find the earliest and latest hire date for each department:"**

```sql
SELECT department, MIN(hire_date) AS earliest_hire, MAX(hire_date) AS latest_hire
FROM employees
GROUP BY department
```

**"Count products by category and show the average price for each category:"**

```sql
SELECT category, COUNT(*) AS product_count, AVG(price) AS average_price
FROM products
GROUP BY category
```

## Summary

- **GROUP BY** groups rows with the same values together
- **Aggregate functions** calculate summaries for each group:
  - **COUNT(*)** - count all rows
  - **COUNT(column)** - count non-empty values
  - **SUM()** - add up numbers
  - **AVG()** - calculate average
  - **MIN()/MAX()** - find smallest/largest values
- **Golden rule**: Non-aggregate columns in SELECT must be in GROUP BY
- **NULL handling**: Most aggregate functions ignore empty (NULL) values
- Use GROUP BY when you want summaries instead of individual rows

GROUP BY is your tool for answering questions like "how many?", "what's the total?", and "what's the average?" for different categories in your data! 