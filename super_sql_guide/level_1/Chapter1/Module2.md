# Module 2: Filtering Your Data - The WHERE Clause

Now that you know how to get data from tables (FROM clause), let's learn how to filter that data to show only what you need. The WHERE clause is like a filter that lets only certain rows pass through.

## 2.1. What WHERE Does and When It Happens

### What it does

The WHERE clause filters rows based on conditions you specify. Think of it like a bouncer at a club - only rows that meet your requirements get to stay in the results.

For example:
```sql
SELECT name, age
FROM employees
WHERE age > 25
```

This says "Show me names and ages, but only for employees older than 25."

### When it happens

Remember our processing order? WHERE comes AFTER FROM but BEFORE SELECT:
1. **FROM** - Get all data from the employees table
2. **WHERE** - Filter to keep only employees over 25
3. **SELECT** - Show just the name and age columns

This order is important! Since WHERE happens before SELECT, you can't use column nicknames (aliases) from your SELECT clause in your WHERE clause.

```sql
-- This WON'T work!
SELECT name, age * 2 AS double_age
FROM employees
WHERE double_age > 50

-- This WILL work!
SELECT name, age * 2 AS double_age
FROM employees
WHERE age * 2 > 50
```

## 2.2. Basic Comparison Operators

These are the building blocks for filtering your data:

### Equal and Not Equal
- **=** means "equal to"
- **!=** or **<>** means "not equal to"

```sql
-- Find employees in the Sales department
SELECT name FROM employees WHERE department = 'Sales'

-- Find employees NOT in the Sales department  
SELECT name FROM employees WHERE department != 'Sales'
```

### Greater Than and Less Than
- **>** means "greater than"
- **<** means "less than"
- **>=** means "greater than or equal to"
- **<=** means "less than or equal to"

```sql
-- Find employees earning more than $50,000
SELECT name, salary FROM employees WHERE salary > 50000

-- Find employees 30 or younger
SELECT name, age FROM employees WHERE age <= 30
```

### Special Case: Dealing with Empty Values (NULL)

Sometimes data is missing. In databases, missing data is called NULL. You can't use = or != with NULL values. Instead, use special operators:

- **IS NULL** - finds empty/missing values
- **IS NOT NULL** - finds values that are NOT empty

```sql
-- Find employees who don't have a phone number listed
SELECT name FROM employees WHERE phone IS NULL

-- Find employees who DO have a phone number
SELECT name FROM employees WHERE phone IS NOT NULL
```

## 2.3. Combining Conditions with AND/OR

You can combine multiple conditions to create more specific filters:

### AND - All conditions must be true
```sql
-- Find employees in Sales who earn more than $50,000
SELECT name, department, salary 
FROM employees 
WHERE department = 'Sales' AND salary > 50000
```

Both conditions must be true for a row to be included.

### OR - At least one condition must be true
```sql
-- Find employees in either Sales or Marketing
SELECT name, department 
FROM employees 
WHERE department = 'Sales' OR department = 'Marketing'
```

If either condition is true, the row is included.

### Using Parentheses for Complex Logic

When combining AND and OR, use parentheses to make your logic clear:

```sql
-- Find employees in Sales OR (Marketing employees who earn more than $60,000)
SELECT name, department, salary
FROM employees 
WHERE department = 'Sales' OR (department = 'Marketing' AND salary > 60000)
```

Without parentheses, SQL might interpret your logic differently than you intended!

## 2.4. Useful WHERE Clause Tools

### BETWEEN - Finding values in a range
Instead of writing `age >= 25 AND age <= 35`, you can use BETWEEN:

```sql
-- Find employees between 25 and 35 years old (inclusive)
SELECT name, age FROM employees WHERE age BETWEEN 25 AND 35
```

BETWEEN includes both the start and end values (25 and 35 in this example).

### IN - Checking against a list of values
Instead of writing many OR conditions, use IN:

```sql
-- Find employees in specific departments
SELECT name, department 
FROM employees 
WHERE department IN ('Sales', 'Marketing', 'HR')

-- This is easier than:
-- WHERE department = 'Sales' OR department = 'Marketing' OR department = 'HR'
```

### LIKE - Pattern matching for text
Use LIKE when you want to find text that matches a pattern:

- **%** means "any number of characters"
- **_** means "exactly one character"

```sql
-- Find employees whose names start with 'A'
SELECT name FROM employees WHERE name LIKE 'A%'

-- Find employees whose names end with 'son'  
SELECT name FROM employees WHERE name LIKE '%son'

-- Find employees whose names contain 'ann'
SELECT name FROM employees WHERE name LIKE '%ann%'

-- Find 4-letter names starting with 'J'
SELECT name FROM employees WHERE name LIKE 'J___'
```

## 2.5. Common WHERE Clause Mistakes

### 1. Using = with NULL values
```sql
-- WRONG - This won't find NULL values!
SELECT name FROM employees WHERE phone = NULL

-- RIGHT - Use IS NULL instead
SELECT name FROM employees WHERE phone IS NULL
```

### 2. Forgetting quotes around text
```sql
-- WRONG - SQL thinks Sales is a column name
SELECT name FROM employees WHERE department = Sales

-- RIGHT - Use quotes for text values
SELECT name FROM employees WHERE department = 'Sales'
```

### 3. Confusing AND/OR logic
```sql
-- This might not do what you think!
SELECT name FROM employees WHERE age > 25 AND department = 'Sales' OR salary > 60000

-- Clearer with parentheses:
SELECT name FROM employees WHERE (age > 25 AND department = 'Sales') OR salary > 60000
```

## 2.6. Performance Tip: Keep It Simple

For better performance, avoid doing calculations on your column names in WHERE clauses:

```sql
-- SLOWER - Database has to calculate YEAR for every row
SELECT name FROM employees WHERE YEAR(hire_date) = 2023

-- FASTER - Let the database use its indexes efficiently  
SELECT name FROM employees WHERE hire_date >= '2023-01-01' AND hire_date < '2024-01-01'
```

## 2.7. Practice Questions

### Basic Questions:

**"What does the WHERE clause do?"**

The WHERE clause filters rows from your data based on conditions you specify. Only rows that meet these conditions are included in your results.

**"What's the difference between = and LIKE?"**

- **=** is for exact matches: `WHERE name = 'John'` finds only exactly "John"
- **LIKE** is for pattern matching: `WHERE name LIKE 'J%'` finds any name starting with "J"

**"How do you check if a value is missing (NULL)?"**

Use `IS NULL` to find missing values, or `IS NOT NULL` to find non-missing values. You cannot use = or != with NULL.

**"What's the difference between AND and OR?"**

- **AND** means ALL conditions must be true
- **OR** means AT LEAST ONE condition must be true

### Practice Scenarios:

**"Find all products that cost between $10 and $50:"**

```sql
SELECT product_name, price 
FROM products 
WHERE price BETWEEN 10 AND 50
```

**"Find customers whose names start with 'A' or 'B':"**

```sql
SELECT customer_name 
FROM customers 
WHERE customer_name LIKE 'A%' OR customer_name LIKE 'B%'
```

**"Find employees in the IT department who earn more than $70,000:"**

```sql
SELECT name, department, salary
FROM employees 
WHERE department = 'IT' AND salary > 70000
```

**"Find orders from 2023 that are either completed or shipped:"**

```sql
SELECT order_id, order_date, status
FROM orders 
WHERE order_date >= '2023-01-01' 
  AND order_date < '2024-01-01'
  AND (status = 'Completed' OR status = 'Shipped')
```

**"Find customers who haven't provided a phone number:"**

```sql
SELECT customer_name, email
FROM customers 
WHERE phone IS NULL
```

## Summary

- **WHERE** filters rows based on conditions
- **=, !=, >, <, >=, <=** for basic comparisons
- **IS NULL, IS NOT NULL** for checking missing values
- **AND** requires all conditions to be true
- **OR** requires at least one condition to be true
- **BETWEEN** for ranges
- **IN** for checking against lists
- **LIKE** with % and _ for pattern matching
- Use parentheses to clarify complex logic
- Always use quotes around text values

The WHERE clause is your main tool for getting exactly the data you need from your tables! 