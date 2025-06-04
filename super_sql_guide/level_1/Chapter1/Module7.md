# Chapter 7: Getting Just What You Need - Limiting Results

Sometimes your query might return thousands or millions of rows, but you only want to see a few. That's where LIMIT comes in - it lets you say "just show me the first 10 rows" or "skip the first 20 and show me the next 10."

## 7.1. Why Limit Your Results?

### The basic idea

Limiting results means telling the database to only return a certain number of rows, instead of returning everything. This is useful for:

- **Seeing a sample** of your data without overwhelming your screen
- **Creating "Top 10" lists** (like top 10 highest-paid employees)
- **Pagination** (showing results in pages, like search results)
- **Better performance** (less data to transfer and display)

Think of it like asking for a taste of soup before getting a full bowl - sometimes you just want a small sample!

### When it happens

LIMIT is processed at the very end, after everything else:
1. **FROM** - Get data from tables
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group the rows
4. **HAVING** - Filter the groups
5. **SELECT** - Choose what to show
6. **ORDER BY** - Sort the results
7. **LIMIT** - Show only a certain number of rows

This means LIMIT works on your final, sorted results - which is exactly what you want for "top N" queries.

## 7.2. Basic LIMIT Usage

### Getting the first N rows
```sql
-- Show only the first 5 employees
SELECT name, salary
FROM employees
LIMIT 5
```

This returns just the first 5 rows. But remember - without ORDER BY, "first" could mean any 5 random rows!

### LIMIT with ORDER BY - The powerful combination
```sql
-- Show the 5 highest-paid employees
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5
```

Now you get a meaningful "top 5" list because:
1. ORDER BY sorts by salary (highest first)
2. LIMIT takes the first 5 from this sorted list

## 7.3. LIMIT for Different Purposes

### Example 1: Top N lists
```sql
-- Top 10 most expensive products
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 10

-- 5 most recent orders
SELECT order_id, customer_id, order_date
FROM orders
ORDER BY order_date DESC
LIMIT 5
```

### Example 2: Data sampling
```sql
-- Just peek at some customer data
SELECT customer_name, city, country
FROM customers
LIMIT 20

-- Quick look at a large table
SELECT *
FROM sales_records
LIMIT 100
```

### Example 3: Preventing runaway queries
```sql
-- Even if there are millions of products, only show 1000
SELECT product_name, category
FROM products
WHERE category = 'Electronics'
LIMIT 1000
```

## 7.4. OFFSET - Skipping Rows for Pagination

OFFSET lets you skip a certain number of rows before taking your LIMIT. This is perfect for pagination (showing results in pages).

### Basic OFFSET usage
```sql
-- Skip the first 10 rows, then show the next 5
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5 OFFSET 10
```

This gets you rows 11-15 from your sorted results.

### Pagination examples
```sql
-- Page 1: First 10 products (rows 1-10)
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 10 OFFSET 0

-- Page 2: Next 10 products (rows 11-20)
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 10 OFFSET 10

-- Page 3: Next 10 products (rows 21-30)
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 10 OFFSET 20
```

**Pattern for pagination:**
- Page 1: `LIMIT 10 OFFSET 0`
- Page 2: `LIMIT 10 OFFSET 10`
- Page 3: `LIMIT 10 OFFSET 20`
- Page N: `LIMIT 10 OFFSET (N-1)*10`

## 7.5. Important Notes About Different Databases

Different database systems use slightly different syntax for limiting results:

### Common syntax variations:
```sql
-- MySQL, PostgreSQL, SQLite - LIMIT/OFFSET
SELECT name FROM employees ORDER BY name LIMIT 10 OFFSET 5

-- SQL Server - TOP
SELECT TOP 10 name FROM employees ORDER BY name

-- Oracle (older versions) - ROWNUM (more complex)
SELECT * FROM (
    SELECT name FROM employees ORDER BY name
) WHERE ROWNUM <= 10
```

**For beginners:** Start with the LIMIT syntax (MySQL/PostgreSQL style) as it's the most straightforward and widely supported.

## 7.6. Common LIMIT Mistakes

### 1. Forgetting ORDER BY with LIMIT
```sql
-- BAD - gives you 10 random employees
SELECT name, salary
FROM employees
LIMIT 10

-- GOOD - gives you the 10 highest-paid employees
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10
```

### 2. Wrong OFFSET calculation for pagination
```sql
-- If you want page 3 with 10 items per page:

-- WRONG - this would be page 4
LIMIT 10 OFFSET 30

-- RIGHT - page 3 starts at row 21, so offset is 20
LIMIT 10 OFFSET 20
```

Remember: Page N with X items per page = `OFFSET (N-1)*X`

### 3. Using LIMIT without considering performance
```sql
-- SLOW - if you're skipping thousands of rows
SELECT product_name
FROM products
ORDER BY product_name
LIMIT 10 OFFSET 50000

-- For very large offsets, consider other approaches
-- (like filtering by ID ranges)
```

## 7.7. Practical Examples

### Example 1: Dashboard showing recent activity
```sql
-- Show the 5 most recent orders for a dashboard
SELECT order_id, customer_name, order_date, total_amount
FROM orders
ORDER BY order_date DESC
LIMIT 5
```

### Example 2: Product catalog with pagination
```sql
-- Show products 21-30 (page 3, with 10 products per page)
SELECT product_name, price, category
FROM products
ORDER BY product_name
LIMIT 10 OFFSET 20
```

### Example 3: Finding the worst performers
```sql
-- Bottom 5 employees by sales
SELECT employee_name, total_sales
FROM employee_sales
ORDER BY total_sales ASC  -- ASC for lowest first
LIMIT 5
```

### Example 4: Random sampling
```sql
-- Get a sample of 100 customers for analysis
-- (Note: this isn't truly random, but it's a quick sample)
SELECT customer_id, customer_name, signup_date
FROM customers
LIMIT 100
```

## 7.8. Practice Questions

### Basic Questions:

**"What does LIMIT do?"**

LIMIT restricts the number of rows returned by a query. It lets you get just the first N rows from your result set instead of all rows.

**"Why is ORDER BY important when using LIMIT?"**

Without ORDER BY, LIMIT gives you an arbitrary set of rows that could be different each time you run the query. ORDER BY ensures you get a predictable, meaningful set of rows (like "top 10 highest values").

**"How do you show results in pages using LIMIT?"**

Use LIMIT with OFFSET. For page N with X items per page: `LIMIT X OFFSET (N-1)*X`

### Practice Scenarios:

**"Show the 10 most expensive products:"**

```sql
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 10
```

**"Show customers 11-20 when sorted alphabetically by name (page 2 with 10 per page):"**

```sql
SELECT customer_name, city
FROM customers
ORDER BY customer_name
LIMIT 10 OFFSET 10
```

**"Get a quick sample of 25 orders to examine:"**

```sql
SELECT order_id, customer_id, order_date, total_amount
FROM orders
LIMIT 25
```

**"Show the 5 employees with the lowest salaries:"**

```sql
SELECT employee_name, salary
FROM employees
ORDER BY salary ASC  -- ASC for lowest first
LIMIT 5
```

**"Display the 3rd page of products (items 21-30) sorted by category:"**

```sql
SELECT product_name, category, price
FROM products
ORDER BY category
LIMIT 10 OFFSET 20  -- Page 3: skip first 20, show next 10
```

## Summary

- **LIMIT** restricts the number of rows returned
- **Always use ORDER BY with LIMIT** for predictable results
- **OFFSET** lets you skip rows for pagination
- **Pagination formula**: Page N with X items = `LIMIT X OFFSET (N-1)*X`
- **Processing order**: LIMIT happens last, after ORDER BY
- Use LIMIT for:
  - Top N lists
  - Data sampling  
  - Pagination
  - Performance (avoiding huge result sets)
- Different databases have different syntax, but LIMIT is widely supported

LIMIT is your tool for getting "just the right amount" of data from your queries! 