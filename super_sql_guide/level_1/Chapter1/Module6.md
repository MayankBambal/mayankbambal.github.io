# Module 6: Sorting Your Results - The ORDER BY Clause

Once you've gotten your data and chosen what to display, you might want to put it in a specific order. That's what ORDER BY does - it sorts your results so they appear in the sequence you want.

## 6.1. Why ORDER BY Matters

### The basic idea

Without ORDER BY, the database returns rows in whatever order it feels like. This could be the order they were inserted, or some completely random order. If you want your results in a specific sequence, you MUST use ORDER BY.

Think of it like this: asking for data without ORDER BY is like asking someone to hand you a stack of photos. They might give them to you in any order. But with ORDER BY, it's like saying "give me those photos sorted by date" - now you know exactly what order you'll get them in.

```sql
-- Without ORDER BY - results could be in any order
SELECT name, salary FROM employees

-- With ORDER BY - results will be sorted by salary, lowest to highest  
SELECT name, salary FROM employees ORDER BY salary
```

### When it happens

ORDER BY happens near the very end of our processing sequence:
1. **FROM** - Get data from tables
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group the rows
4. **HAVING** - Filter the groups
5. **SELECT** - Choose what to show
6. **ORDER BY** - Sort the results
7. **LIMIT** - Show only a certain number of rows

This late timing means ORDER BY can use column aliases that you defined in your SELECT clause.

## 6.2. Basic Sorting

### Sorting by one column

```sql
-- Sort employees by salary (lowest to highest)
SELECT name, salary FROM employees ORDER BY salary

-- Sort products by name (A to Z)
SELECT product_name, price FROM products ORDER BY product_name
```

### ASC vs DESC - Choosing direction

- **ASC** (ascending) = lowest to highest, A to Z, oldest to newest (this is the default)
- **DESC** (descending) = highest to lowest, Z to A, newest to oldest

```sql
-- Highest salary first
SELECT name, salary FROM employees ORDER BY salary DESC

-- Alphabetical order (A to Z) - ASC is the default, so you don't need to write it
SELECT name FROM employees ORDER BY name ASC
-- Same as:
SELECT name FROM employees ORDER BY name
```

### Sorting by multiple columns

You can sort by several columns - the first one is the primary sort, the second breaks ties, etc.

```sql
-- First sort by department, then by salary within each department
SELECT name, department, salary 
FROM employees 
ORDER BY department, salary DESC
```

This means:
1. Group all people by department (alphabetically)
2. Within each department, sort by salary (highest first)

**Example results:**
| name | department | salary |
|------|------------|--------|
| Alice | HR | 60000 |
| Bob | HR | 55000 |
| Carol | IT | 75000 |
| Dave | IT | 70000 |
| Eve | Sales | 65000 |

## 6.3. Sorting by Different Things

### Sorting by column aliases
Since ORDER BY happens after SELECT, you can use column nicknames:

```sql
SELECT 
    name,
    salary * 12 AS annual_salary
FROM employees
ORDER BY annual_salary DESC  -- Using the alias we created
```

### Sorting by calculations
You can sort by calculated values:

```sql
-- Sort by total inventory value (price × quantity)
SELECT product_name, price, quantity
FROM products
ORDER BY (price * quantity) DESC
```

### Sorting by column position (not recommended)
Some databases let you sort by column number, but this is confusing:

```sql
-- This sorts by the 2nd column (salary), but it's hard to read
SELECT name, salary FROM employees ORDER BY 2

-- Better to be explicit:
SELECT name, salary FROM employees ORDER BY salary
```

## 6.4. Dealing with Missing Values (NULL)

When a column has missing (NULL) values, different databases handle them differently when sorting:

- Some databases put NULLs first (like SQL Server, MySQL)
- Others put NULLs last (like PostgreSQL, Oracle)

### Example with missing data:
```sql
-- employees table with some missing hire dates:
-- Alice, 2020-01-15
-- Bob, NULL (missing)  
-- Carol, 2019-03-10

SELECT name, hire_date 
FROM employees 
ORDER BY hire_date
```

Depending on your database, Bob (with the NULL hire_date) might appear first or last.

### Controlling where NULLs go
Some databases let you specify where to put NULLs:

```sql
-- PostgreSQL/Oracle - put missing values last
SELECT name, hire_date 
FROM employees 
ORDER BY hire_date NULLS LAST

-- For databases that don't support this, you can use a workaround:
SELECT name, hire_date
FROM employees
ORDER BY 
    CASE WHEN hire_date IS NULL THEN 1 ELSE 0 END,  -- NULLs last
    hire_date
```

## 6.5. Common Sorting Examples

### Example 1: Customer list alphabetically
```sql
SELECT customer_name, city
FROM customers
ORDER BY customer_name
```

### Example 2: Products by price, most expensive first
```sql
SELECT product_name, price
FROM products  
ORDER BY price DESC
```

### Example 3: Employees by department, then by hire date (newest first within each department)
```sql
SELECT name, department, hire_date
FROM employees
ORDER BY department, hire_date DESC
```

### Example 4: Orders by total value
```sql
SELECT order_id, quantity * unit_price AS total_value
FROM order_details
ORDER BY total_value DESC
```

## 6.6. Common ORDER BY Mistakes

### 1. Forgetting ORDER BY when order matters
```sql
-- BAD - might get results in any order
SELECT name FROM employees

-- GOOD - guaranteed alphabetical order
SELECT name FROM employees ORDER BY name
```

### 2. Expecting default ordering
```sql
-- DON'T assume the data will come back in ID order or insertion order
SELECT * FROM products

-- BE EXPLICIT about the order you want
SELECT * FROM products ORDER BY product_id
```

### 3. Using ORDER BY with the wrong column
```sql
-- If you want to sort by price but accidentally sort by name:
SELECT product_name, price 
FROM products 
ORDER BY product_name  -- Oops! Sorted by name, not price

-- Make sure you're sorting by what you actually want:
SELECT product_name, price 
FROM products 
ORDER BY price DESC
```

### 4. Mixing up ASC and DESC
```sql
-- If you want highest prices first but forget DESC:
SELECT product_name, price
FROM products
ORDER BY price  -- This gives LOWEST prices first

-- Remember DESC for highest-to-lowest:
SELECT product_name, price
FROM products
ORDER BY price DESC
```

## 6.7. Practice Questions

### Basic Questions:

**"What does ORDER BY do and why is it important?"**

ORDER BY sorts the rows in your result set based on one or more columns. It's important because without it, the database returns rows in an unpredictable order that might change between runs.

**"What's the difference between ASC and DESC?"**

- ASC (ascending) sorts from lowest to highest, A to Z, oldest to newest - this is the default
- DESC (descending) sorts from highest to lowest, Z to A, newest to oldest

**"Can you use column aliases in ORDER BY? Why?"**

Yes, you can use column aliases in ORDER BY because ORDER BY is processed after SELECT, so the aliases are already defined and available.

### Practice Scenarios:

**"Sort all customers alphabetically by last name:"**

```sql
SELECT customer_name
FROM customers
ORDER BY customer_name
```

**"Show products with highest prices first:"**

```sql
SELECT product_name, price
FROM products
ORDER BY price DESC
```

**"List employees by department, and within each department, by salary (highest first):"**

```sql
SELECT name, department, salary
FROM employees
ORDER BY department, salary DESC
```

**"Show orders by date, most recent first:"**

```sql
SELECT order_id, order_date, customer_id
FROM orders
ORDER BY order_date DESC
```

**"Sort products by their total inventory value (price × quantity in stock):"**

```sql
SELECT 
    product_name, 
    price, 
    quantity_in_stock,
    price * quantity_in_stock AS inventory_value
FROM products
ORDER BY inventory_value DESC
```

## Summary

- **ORDER BY** sorts your results in a specific order
- **ASC** = ascending (low to high, A to Z) - this is the default
- **DESC** = descending (high to low, Z to A)
- You can sort by multiple columns - first column is primary sort, second breaks ties, etc.
- You can sort by column aliases, calculations, or expressions
- Without ORDER BY, results come in unpredictable order
- **Processing order**: 
  ```
  SELECT ──➤ ORDER BY ──➤ LIMIT
  ```
- Different databases handle NULL values differently when sorting

Remember: if the order of your results matters, always use ORDER BY! 