# Module 4: Filtering Groups - The HAVING Clause

In the previous chapter, you learned how to group data and calculate totals, averages, and counts. But what if you only want to see certain groups? For example, what if you want to see only departments with more than 10 employees? That's where HAVING comes in!

## 4.1. What HAVING Does

### The basic idea

HAVING filters groups AFTER they've been created by GROUP BY. It's like WHERE, but for groups instead of individual rows.

Think of it this way:
- **WHERE** is like a filter that stops individual people from entering a room
- **HAVING** is like a filter that only lets certain groups stay in the room after they've formed

```sql
-- WHERE filters individual rows first
-- GROUP BY groups the remaining rows  
-- HAVING filters the groups
-- SELECT shows the final results
```

### When it happens

HAVING comes after GROUP BY in our processing order:
1. **FROM** - Get the data from tables
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group the remaining rows
4. **HAVING** - Filter the groups
5. **SELECT** - Show the results

## 4.2. WHERE vs HAVING - What's the Difference?

This is super important to understand:

| WHERE | HAVING |
|-------|---------|
| Filters individual rows | Filters groups |
| Happens BEFORE grouping | Happens AFTER grouping |
| Can't use COUNT(), SUM(), etc. | CAN use COUNT(), SUM(), etc. |
| Filters people before they form groups | Filters groups after they're formed |

### Example to show the difference:

```sql
-- WHERE example: Filter individual employees first
SELECT 
    department, 
    COUNT(*) AS employee_count
FROM employees
WHERE salary > 50000    -- Only include employees earning over $50k
GROUP BY department;

-- HAVING example: Filter departments after counting
SELECT 
    department, 
    COUNT(*) AS employee_count  
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;    -- Only show departments with more than 5 employees
```

## 4.3. Common HAVING Examples

### Example 1: Departments with many employees
```sql
-- Show only departments that have more than 10 employees
SELECT 
    department, 
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;
```

### Example 2: High-value customer groups  
```sql
-- Show only customers who have spent more than $1000 total
SELECT 
    customer_id, 
    SUM(order_amount) AS total_spent
FROM orders
GROUP BY customer_id  
HAVING SUM(order_amount) > 1000;
```

### Example 3: Popular product categories
```sql
-- Show only categories that have an average price over $25
SELECT 
    category, 
    COUNT(*) AS product_count, 
    AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 25;
```

### Example 4: Multiple conditions
```sql
-- Departments with many employees AND high average salary
SELECT 
    department, 
    COUNT(*) AS emp_count, 
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5 
   AND AVG(salary) > 60000;
```

## 4.4. Combining WHERE and HAVING

You can use both WHERE and HAVING in the same query:

```sql
-- Find departments (excluding interns) that have more than 3 people
SELECT 
    department, 
    COUNT(*) AS employee_count
FROM employees  
WHERE job_title != 'Intern'    -- Filter out interns first
GROUP BY department            -- Group remaining employees by department
HAVING COUNT(*) > 3;           -- Only show departments with more than 3 people
```

**Processing order:**
1. WHERE removes all interns from consideration
2. GROUP BY groups the remaining employees by department  
3. HAVING only keeps departments with more than 3 employees
4. SELECT shows the final results

## 4.5. Common HAVING Mistakes

### 1. Using WHERE when you should use HAVING
```sql
-- WRONG - You can't use aggregate functions in WHERE
SELECT 
    department, 
    COUNT(*) AS emp_count
FROM employees
WHERE COUNT(*) > 5    -- ERROR! WHERE can't use COUNT()
GROUP BY department;

-- RIGHT - Use HAVING for aggregate functions
SELECT 
    department, 
    COUNT(*) AS emp_count
FROM employees  
GROUP BY department
HAVING COUNT(*) > 5;
```

### 2. Using HAVING when you should use WHERE
```sql
-- INEFFICIENT - Filtering departments in HAVING
SELECT 
    department, 
    COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING department = 'Sales';   -- This works, but it's better to use WHERE

-- BETTER - Filter departments in WHERE (more efficient)
SELECT 
    department, 
    COUNT(*) AS emp_count
FROM employees
WHERE department = 'Sales'    -- Filter first, then group
GROUP BY department;
```

**Why is WHERE better?** Because it filters data before grouping, so there's less data to process.

### 3. Wrong clause order
```sql
-- WRONG - HAVING must come after GROUP BY
SELECT department, COUNT(*)
FROM employees
HAVING COUNT(*) > 5
GROUP BY department;    -- ERROR! HAVING can't come before GROUP BY

-- RIGHT - Correct order
SELECT 
    department, 
    COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

## 4.6. HAVING Without GROUP BY

You can use HAVING without GROUP BY, but it's not common. In this case, it treats all your data as one big group:

```sql
-- Only show results if the overall average salary is above $55,000
SELECT AVG(salary) AS company_average
FROM employees
HAVING AVG(salary) > 55000;
```

If the average is $55,000 or less, you get no results. If it's above $55,000, you see the average.

## 4.7. Practice Questions

### Basic Questions:

**"What's the difference between WHERE and HAVING?"**

- WHERE filters individual rows before grouping and can't use aggregate functions like COUNT() or SUM()
- HAVING filters groups after GROUP BY and CAN use aggregate functions

**"When would you use HAVING instead of WHERE?"**

Use HAVING when you need to filter based on calculated values like COUNT(), SUM(), AVG(), etc. For example, "show only departments with more than 10 employees" requires HAVING because you need to count employees per department first.

**"Can you use both WHERE and HAVING in the same query?"**

Yes! WHERE filters individual rows first, then GROUP BY groups them, then HAVING filters the groups.

### Practice Scenarios:

**"Find all customers who have placed more than 3 orders:"**

```sql
-- Customers with more than 3 orders
SELECT 
    customer_id, 
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 3;
```

**"Show product categories where the average price is over $50:"**

```sql
-- Categories with average price over $50
SELECT 
    category, 
    AVG(price) AS average_price
FROM products
GROUP BY category
HAVING AVG(price) > 50;
```

**"Find departments with more than 5 employees, but exclude part-time workers from the count:"**

```sql
SELECT department, COUNT(*) AS fulltime_employee_count
FROM employees
WHERE employment_type = 'Full-time'    -- Filter first
GROUP BY department                    -- Then group
HAVING COUNT(*) > 5                   -- Then filter groups
```

**"Show salespeople who have total sales over $100,000:"**

```sql
SELECT salesperson_id, SUM(sale_amount) AS total_sales
FROM sales
GROUP BY salesperson_id
HAVING SUM(sale_amount) > 100000
```

**"Find product categories with more than 10 products AND average price over $30:"**

```sql
SELECT category, COUNT(*) AS product_count, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 10 AND AVG(price) > 30
```

## Summary

- **HAVING** filters groups created by GROUP BY
- **WHERE** filters individual rows before grouping
- Use **HAVING** when you need to filter based on:
  - COUNT() - "more than X items"
  - SUM() - "total over X amount"  
  - AVG() - "average above X"
  - MIN()/MAX() - "smallest/largest value meets criteria"
- **Processing order**: WHERE → GROUP BY → HAVING → SELECT
- You can use both WHERE and HAVING in the same query
- Always put HAVING after GROUP BY

HAVING is your tool for answering questions like "which groups have more than X?" or "which categories average above Y?" 