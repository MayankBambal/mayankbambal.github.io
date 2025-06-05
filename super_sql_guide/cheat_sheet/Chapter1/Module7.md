# Module 7: LIMIT and Result Set Control

## LIMIT Basics

**Purpose**: Restrict number of rows returned for pagination, Top-N queries, or sampling.

**Execution**: Typically last, after ORDER BY.

```sql
-- Basic syntax varies by database
SELECT column_list
FROM table_name
[WHERE conditions]
[ORDER BY columns]
[LIMIT number] [OFFSET number];
```

---

## Database-Specific Syntax

### Cross-Database Comparison

| DBMS | Basic Limit | With Offset | Special Features |
|------|-------------|-------------|------------------|
| **MySQL, PostgreSQL, SQLite** | `LIMIT n` | `LIMIT n OFFSET m` (PG/SQLite)<br>`LIMIT m, n` (MySQL) | - |
| **SQL Server** | `TOP (n)` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `WITH TIES`, `PERCENT` |
| **Oracle** | Subquery with `ROWNUM <= n` | Complex nested subquery | `ROWNUM` assigned before ORDER BY |
| **Standard SQL** | `FETCH FIRST n ROWS ONLY` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `WITH TIES`, `PERCENT` |

### Syntax Examples

**MySQL/PostgreSQL/SQLite**:
```sql
-- Basic limiting
SELECT * FROM products ORDER BY price DESC LIMIT 10;

-- With offset
SELECT * FROM products ORDER BY name LIMIT 20 OFFSET 40;  -- PostgreSQL/SQLite
SELECT * FROM products ORDER BY name LIMIT 40, 20;       -- MySQL (offset, limit)
```

**SQL Server**:
```sql
-- Basic limiting
SELECT TOP (10) * FROM products ORDER BY price DESC;

-- With offset (SQL Server 2012+)
SELECT * FROM products 
ORDER BY name 
OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;

-- With ties (includes all tied values)
SELECT TOP (10) WITH TIES * FROM products ORDER BY price DESC;

-- Percentage
SELECT TOP (25) PERCENT * FROM products ORDER BY price DESC;
```

**Oracle**:
```sql
-- Basic limiting (older versions)
SELECT * FROM (
    SELECT * FROM products ORDER BY price DESC
) WHERE ROWNUM <= 10;

-- With offset (complex)
SELECT * FROM (
    SELECT p.*, ROW_NUMBER() OVER (ORDER BY price DESC) as rn
    FROM products p
) WHERE rn BETWEEN 41 AND 60;

-- Oracle 12c+ (standard SQL)
SELECT * FROM products ORDER BY price DESC FETCH FIRST 10 ROWS ONLY;
```

**Standard SQL (newer versions)**:
```sql
-- Basic limiting
SELECT * FROM products ORDER BY price DESC FETCH FIRST 10 ROWS ONLY;

-- With offset
SELECT * FROM products ORDER BY name 
OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;

-- With ties
SELECT * FROM products ORDER BY price DESC FETCH FIRST 10 ROWS WITH TIES;
```

---

## Common Use Cases

### Top N Queries

```sql
-- Top 10 most expensive products
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 10;

-- Bottom 5 rated items
SELECT product_name, average_rating
FROM products
ORDER BY average_rating ASC
LIMIT 5;

-- Most recent orders
SELECT order_id, customer_id, order_date
FROM orders
ORDER BY order_date DESC
LIMIT 20;
```

### Data Sampling

```sql
-- Quick peek at table structure and data
SELECT * FROM large_table LIMIT 100;

-- Sample for analysis (not truly random, but quick)
SELECT customer_id, total_purchases
FROM customer_summary
LIMIT 1000;

-- Every nth row (pseudo-sampling)
SELECT * FROM products 
WHERE product_id % 10 = 0  -- Every 10th product
LIMIT 500;
```

### Preventing Runaway Queries

```sql
-- Safety limit for potentially large result sets
SELECT * 
FROM user_activity_log 
WHERE activity_date >= '2023-01-01'
LIMIT 10000;  -- Prevent accidentally returning millions of rows

-- Development queries with safety nets
SELECT p.*, c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.status = 'active'
LIMIT 500;  -- Reasonable limit for testing
```

---

## Pagination Strategies

### Basic OFFSET Pagination

```sql
-- Page 1 (first 20 records)
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 20 OFFSET 0;

-- Page 2 (records 21-40)
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 20 OFFSET 20;

-- Page N formula: LIMIT page_size OFFSET (page_number - 1) * page_size
-- Page 5 with 20 items per page:
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 20 OFFSET 80;  -- (5-1) * 20 = 80
```

### Keyset Pagination (Cursor-Based)

**Better for large datasets** - avoids performance issues with large OFFSET values.

```sql
-- First page (no WHERE clause needed)
SELECT product_id, product_name, price
FROM products
ORDER BY product_id
LIMIT 20;

-- Next page (use last product_id from previous page)
SELECT product_id, product_name, price
FROM products
WHERE product_id > 12345  -- Last ID from previous page
ORDER BY product_id
LIMIT 20;

-- For complex ordering (e.g., by price, then ID)
SELECT product_id, product_name, price
FROM products
WHERE (price < 99.99) OR (price = 99.99 AND product_id > 12345)
ORDER BY price DESC, product_id
LIMIT 20;
```

### Pagination with Count

```sql
-- Get both results and total count
-- Method 1: Two queries
SELECT COUNT(*) FROM products WHERE category = 'Electronics';

SELECT product_name, price
FROM products
WHERE category = 'Electronics'
ORDER BY product_name
LIMIT 20 OFFSET 40;

-- Method 2: Window function (PostgreSQL, SQL Server)
SELECT 
    product_name, 
    price,
    COUNT(*) OVER() AS total_count
FROM products
WHERE category = 'Electronics'
ORDER BY product_name
LIMIT 20 OFFSET 40;
```

---

## Performance Considerations

### OFFSET Performance Problem

```sql
-- SLOW: Large offset requires scanning many rows
SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT 20 OFFSET 50000;  -- Has to skip 50,000 rows!

-- FASTER: Keyset pagination
SELECT product_name, price
FROM products
WHERE product_name > 'Widget X'  -- Where last page ended
ORDER BY product_name
LIMIT 20;
```

### Indexing for LIMIT

```sql
-- Create index on ORDER BY columns
CREATE INDEX idx_products_name ON products(product_name);

-- Covering index for better performance
CREATE INDEX idx_products_covering 
ON products(product_name) 
INCLUDE (price, category);

-- Query benefits from covering index
SELECT product_name, price, category
FROM products
ORDER BY product_name
LIMIT 50;
```

### When OFFSET is Acceptable

```sql
-- SMALL offsets are fine
LIMIT 20 OFFSET 100;  -- No problem

-- Known limited result sets
SELECT * FROM recent_orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY order_date DESC
LIMIT 50 OFFSET 100;  -- Limited by date filter

-- AVOID large offsets on big tables
LIMIT 20 OFFSET 100000;  -- Very slow!
```

---

## Advanced LIMIT Patterns

### Random Sampling

```sql
-- PostgreSQL - True random sample
SELECT * FROM products ORDER BY RANDOM() LIMIT 100;

-- MySQL - Random sample
SELECT * FROM products ORDER BY RAND() LIMIT 100;

-- SQL Server - Random sample
SELECT TOP (100) * FROM products ORDER BY NEWID();

-- Performance note: Random sampling can be slow on large tables
-- Consider pre-computed samples or approximate methods for production
```

### Conditional Limiting

```sql
-- Different limits based on conditions
SELECT 
    product_name, 
    price,
    category
FROM products
WHERE category = 'Electronics'
ORDER BY price DESC
LIMIT CASE 
    WHEN @user_type = 'premium' THEN 100
    ELSE 20
END;  -- Note: Not all databases support expressions in LIMIT

-- Alternative approach with variables
SET @row_limit = CASE WHEN @user_type = 'premium' THEN 100 ELSE 20 END;
SELECT product_name, price FROM products ORDER BY price DESC LIMIT @row_limit;
```

### Batch Processing

```sql
-- Process large table in batches
DECLARE @batch_size INT = 1000;
DECLARE @offset INT = 0;

WHILE EXISTS (
    SELECT 1 FROM large_table 
    WHERE processed = 0 
    ORDER BY id 
    LIMIT 1 OFFSET @offset
)
BEGIN
    -- Process batch
    UPDATE large_table 
    SET processed = 1
    WHERE id IN (
        SELECT id FROM large_table 
        WHERE processed = 0 
        ORDER BY id 
        LIMIT @batch_size OFFSET @offset
    );
    
    SET @offset = @offset + @batch_size;
END;
```

---

## Best Practices

### Always Use ORDER BY with LIMIT

```sql
-- BAD: Unpredictable results
SELECT * FROM products LIMIT 10;

-- GOOD: Predictable, deterministic results
SELECT * FROM products ORDER BY product_id LIMIT 10;

-- BETTER: Include unique column for true determinism
SELECT * FROM products ORDER BY price DESC, product_id ASC LIMIT 10;
```

### Handle Edge Cases

```sql
-- Check for existence before pagination
IF EXISTS (SELECT 1 FROM products WHERE category = @category)
BEGIN
    SELECT product_name, price
    FROM products
    WHERE category = @category
    ORDER BY product_name
    LIMIT @page_size OFFSET @offset;
END
ELSE
BEGIN
    SELECT 'No products found' AS message;
END;
```

### Validate Pagination Parameters

```sql
-- Ensure non-negative offset and reasonable page size
DECLARE @safe_offset INT = GREATEST(0, @user_offset);
DECLARE @safe_limit INT = LEAST(1000, GREATEST(1, @user_limit));

SELECT product_name, price
FROM products
ORDER BY product_name
LIMIT @safe_limit OFFSET @safe_offset;
```

---

## Quick Reference

### LIMIT Checklist
- Always use ORDER BY with LIMIT for deterministic results
- Include unique columns in ORDER BY for pagination
- Use keyset pagination for large offsets
- Index ORDER BY columns for performance
- Validate user input for pagination parameters
- Consider total count requirements for UI

### Pagination Formula
- **Page N with X items**: `LIMIT X OFFSET (N-1)*X`
- **Page 1**: `LIMIT 20 OFFSET 0`
- **Page 2**: `LIMIT 20 OFFSET 20`
- **Page 5**: `LIMIT 20 OFFSET 80`

### Performance Guidelines
- **Small offsets** (< 1000): OFFSET pagination OK
- **Large offsets** (> 10000): Use keyset pagination
- **Random access needed**: Consider search/filtering instead
- **Real-time data**: Keyset pagination with timestamps

### Common Use Cases
- **Top N lists**: `ORDER BY metric DESC LIMIT N`
- **Pagination**: `ORDER BY stable_column LIMIT page_size OFFSET offset`
- **Sampling**: `ORDER BY RANDOM() LIMIT sample_size`
- **Safety limits**: `LIMIT max_safe_rows` on potentially large queries 