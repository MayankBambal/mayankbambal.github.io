# Chapter 5: Choosing Your Output - The SELECT Clause

The SELECT clause is the most recognizable part of an SQL query - it's where you specify exactly what information you want to see in your results. Think of it like deciding which items to put on a shopping list from all the things available in a store.

## 5.1. What SELECT Does

### The basic idea

SELECT tells the database which columns or information you want to see from your data. You can choose specific columns, create calculations, or even show all columns at once.

Here's a simple example:
```sql
SELECT name, salary
FROM employees
```

This says "I want to see just the name and salary columns from the employees table."

### When it happens

Remember our processing order? SELECT comes quite late in the process:
1. **FROM** - Get data from tables
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group the rows
4. **HAVING** - Filter the groups  
5. **SELECT** - Choose what to show
6. **ORDER BY** - Sort the results

This timing is important because it means you can't use column nicknames (aliases) from SELECT in earlier clauses like WHERE.

## 5.2. Ways to Select Your Data

### SELECT * - Show everything
The asterisk (*) means "show me all columns":

```sql
SELECT *
FROM employees
```

This is convenient when exploring data, but it's usually better to specify exactly which columns you need.

**Why specify columns instead of using *?**
- Faster performance (less data to process)
- Clearer code (you know exactly what you're getting)
- More reliable (if someone adds columns to the table, your query won't break)

### SELECT specific columns - Show exactly what you need
```sql
SELECT name, department, salary
FROM employees
```

This only shows the three columns you specified, in the order you listed them.

### Giving columns better names with AS (aliases)
Sometimes column names aren't very readable. You can give them better names:

```sql
SELECT 
    name AS employee_name,
    salary AS annual_salary,
    department AS dept
FROM employees
```

Now your results will show "employee_name" instead of "name" as the column header.

## 5.3. Simple Calculations in SELECT

You can do math and other calculations right in your SELECT clause:

### Basic math
```sql
SELECT 
    name,
    salary,
    salary * 12 AS annual_salary,
    salary / 52 AS weekly_salary
FROM employees
```

### Combining text (concatenation)
```sql
-- This might work differently depending on your database
SELECT 
    name,
    department,
    name + ' works in ' + department AS description  -- SQL Server style
FROM employees

-- Or in MySQL/PostgreSQL:
SELECT 
    name,
    department,
    CONCAT(name, ' works in ', department) AS description
FROM employees
```

### Basic conditional logic with CASE
Sometimes you want to show different text based on values:

```sql
SELECT 
    name,
    salary,
    CASE 
        WHEN salary > 60000 THEN 'High'
        WHEN salary > 40000 THEN 'Medium' 
        ELSE 'Low'
    END AS salary_category
FROM employees
```

This creates a new column called "salary_category" that shows "High", "Medium", or "Low" based on each person's salary.

## 5.4. SELECT DISTINCT - Remove Duplicates

Sometimes your results have duplicate rows, and you only want to see each unique combination once:

### DISTINCT with one column
```sql
-- Show each department only once
SELECT DISTINCT department
FROM employees
```

If you have 100 employees but only 5 departments, this will show just 5 rows (one for each department).

### DISTINCT with multiple columns
```sql
-- Show each unique combination of department and job title
SELECT DISTINCT department, job_title
FROM employees  
```

This shows unique combinations. So if you have multiple "Sales Managers" in the Sales department, you'll only see "Sales, Manager" once.

### Important: DISTINCT affects the whole row
DISTINCT looks at ALL the columns you've selected to determine if a row is unique:

```sql
-- This might still show duplicates if salaries are different!
SELECT DISTINCT name, salary
FROM employees
```

If two people named "John Smith" have different salaries, you'll see both rows because the combination of (name, salary) is different.

## 5.5. Dealing with Missing Data (NULL)

Sometimes data is missing (NULL). You can handle this in your SELECT:

### Show a default value when data is missing
```sql
SELECT 
    name,
    COALESCE(phone, 'No phone number') AS contact_phone
FROM employees
```

COALESCE shows the phone number if it exists, otherwise it shows "No phone number".

### Check if data is missing
```sql
SELECT 
    name,
    phone,
    CASE 
        WHEN phone IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS phone_status
FROM employees
```

## 5.6. Common SELECT Mistakes

### 1. Using column aliases in WHERE
```sql
-- WRONG - age_category doesn't exist yet when WHERE runs
SELECT 
    name,
    age,
    CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END AS age_category
FROM employees
WHERE age_category = 'Senior'  -- ERROR!

-- RIGHT - repeat the calculation in WHERE
SELECT 
    name,
    age,
    CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END AS age_category
FROM employees
WHERE CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END = 'Senior'
```

### 2. Forgetting to handle NULL values
```sql
-- This might give unexpected results if some salaries are NULL
SELECT name, salary * 12 AS annual_salary
FROM employees

-- Better - handle the NULL case
SELECT 
    name, 
    COALESCE(salary, 0) * 12 AS annual_salary
FROM employees
```

### 3. Selecting too much data with SELECT *
```sql
-- Not ideal - gets all columns even if you only need a few
SELECT * FROM employees WHERE department = 'Sales'

-- Better - be specific about what you need
SELECT name, salary, hire_date FROM employees WHERE department = 'Sales'
```

## 5.7. Practice Questions

### Basic Questions:

**"What does the SELECT clause do?"**

The SELECT clause specifies which columns and information you want to see in your query results. It determines the structure and content of your output.

**"When can you use column aliases from SELECT in other parts of your query?"**

You can use SELECT column aliases in the ORDER BY clause because ORDER BY happens after SELECT. You usually can't use them in WHERE, GROUP BY, or HAVING because those happen before SELECT.

**"What's the difference between SELECT name and SELECT DISTINCT name?"**

- SELECT name shows the name column for every row, including duplicates
- SELECT DISTINCT name shows each unique name only once, removing duplicates

### Practice Scenarios:

**"Show employee names and their salaries, with a new column showing salary in thousands:"**

```sql
SELECT 
    name,
    salary,
    salary / 1000 AS salary_in_thousands
FROM employees
```

**"List all unique combinations of department and job title:"**

```sql
SELECT DISTINCT department, job_title
FROM employees
```

**"Show product names and create a category based on price (over $100 = 'Expensive', $50-100 = 'Medium', under $50 = 'Cheap'):"**

```sql
SELECT 
    product_name,
    price,
    CASE 
        WHEN price > 100 THEN 'Expensive'
        WHEN price >= 50 THEN 'Medium'
        ELSE 'Cheap'
    END AS price_category
FROM products
```

**"Show customer names and their phone numbers, but display 'No phone' if the phone number is missing:"**

```sql
SELECT 
    customer_name,
    COALESCE(phone, 'No phone') AS contact_phone
FROM customers
```

**"Show all unique departments from the employees table:"**

```sql
SELECT DISTINCT department
FROM employees
```

## Summary

- **SELECT** chooses what columns and information to show in your results
- **Column aliases** (AS) give columns better names for display
- **SELECT *** gets all columns, but it's usually better to specify exactly what you need
- **Calculations** can be done right in SELECT (math, text combinations, conditional logic)
- **DISTINCT** removes duplicate rows from your results
- **CASE** statements let you show different values based on conditions
- **COALESCE** helps handle missing (NULL) data
- **Processing order**: SELECT happens after FROM, WHERE, GROUP BY, and HAVING

The SELECT clause is where you craft the exact output you want from your data! 