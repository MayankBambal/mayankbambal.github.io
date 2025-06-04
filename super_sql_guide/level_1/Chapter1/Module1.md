# Chapter 1: Getting Your Data - FROM Clause and JOINs

When you want to get information from a database, you need to tell it where to look. That's what the FROM clause does - it's like telling someone which file cabinet to open before looking for documents.

## 1.1. The FROM Clause: Where Your Data Lives

### What it does

The FROM clause tells the database which table (or tables) contains the data you want. Think of a table like a spreadsheet with rows and columns. Every time you want to get data, you need to specify which table to look in.

Here's a simple example:
```sql
SELECT name 
FROM employees
```

This says "I want to see names, and you can find them in the employees table."

### When it happens

Remember the processing order we talked about in the introduction? The FROM clause is processed FIRST. The database needs to know where to look before it can do anything else.

### Making Table Names Shorter with Aliases

Sometimes table names are long and hard to type. You can give them shorter "nicknames" called aliases:

```sql
SELECT e.name 
FROM employees AS e
```

The `AS e` part gives the employees table a short nickname "e". Now instead of typing "employees" every time, you can just type "e". This becomes very helpful when working with multiple tables.

**Important rule**: Once you give a table an alias, you MUST use that alias for the rest of the query. You can't switch back to the original name.

### Getting Data from Query Results (Subqueries)

Sometimes the data you need doesn't exist in a single table - you need to create it first. You can do this with a subquery in the FROM clause:

```sql
SELECT dept_name, avg_salary
FROM (
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
) AS dept_averages
```

This might look complex, but let's break it down:
1. The inner query calculates average salary by department
2. The outer query treats those results like a temporary table
3. We give this temporary table the alias "dept_averages"

Think of it like making a summary report first, then using that summary for further analysis.

## 1.2. JOINs: Connecting Related Information

In real databases, information is often split across multiple tables. For example, you might have:
- An `employees` table with names and department IDs  
- A `departments` table with department IDs and department names

To see employee names with their actual department names (not just IDs), you need to JOIN these tables together.

### What JOINs do

JOINs connect rows from different tables based on related information. It's like matching puzzle pieces - you find rows that "belong together" based on some common value.

### Types of JOINs (The Main Ones You'll Use)

#### INNER JOIN - Only Show Matches

An INNER JOIN only shows rows where there's a match in BOTH tables.

```sql
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
```

This means:
- Only employees who have a valid department will be shown
- Only departments that have employees will be shown
- If an employee has no department, they won't appear
- If a department has no employees, it won't appear

**Real-world example**: Like a list of "students AND their assigned teachers" - only students who have teachers assigned will appear.

#### LEFT JOIN - Show All from the First Table

A LEFT JOIN shows ALL rows from the first (left) table, plus any matches from the second table.

```sql
SELECT e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id
```

This means:
- ALL employees will be shown
- If an employee has a department, show the department name
- If an employee has no department, still show the employee but department_name will be blank (NULL)

**Real-world example**: Like a list of "all students, and their teachers if they have one" - every student appears, but some might not have a teacher assigned.

#### RIGHT JOIN - Show All from the Second Table

A RIGHT JOIN is the opposite of LEFT JOIN - it shows ALL rows from the second (right) table.

```sql
SELECT e.name, d.department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.department_id
```

This means:
- ALL departments will be shown
- If a department has employees, show them
- If a department has no employees, still show the department but employee name will be blank (NULL)

**Real-world example**: Like a list of "all teachers, and their students if they have any."

### How to Join Tables

To join tables, you need to specify:
1. **Which tables** to join (in the FROM and JOIN clauses)
2. **How they connect** (in the ON clause)

The ON clause tells the database how the tables are related:
```sql
ON employees.department_id = departments.department_id
```

This says "match rows where the department_id is the same in both tables."

### Common JOIN Example

Let's say you have these tables:

**employees table:**
| employee_id | name  | department_id |
|-------------|-------|---------------|
| 1           | Alice | 1             |
| 2           | Bob   | 2             |
| 3           | Carol | NULL          |

**departments table:**
| department_id | department_name |
|---------------|-----------------|
| 1             | Sales           |
| 2             | Marketing       |
| 3             | HR              |

Different JOINs would give different results:

**INNER JOIN** (only matches):
| name  | department_name |
|-------|-----------------|
| Alice | Sales           |
| Bob   | Marketing       |

**LEFT JOIN** (all employees):
| name  | department_name |
|-------|-----------------|
| Alice | Sales           |
| Bob   | Marketing       |
| Carol | NULL            |

**RIGHT JOIN** (all departments):
| name  | department_name |
|-------|-----------------|
| Alice | Sales           |
| Bob   | Marketing       |
| NULL  | HR              |

## 1.3. Common JOIN Mistakes to Avoid

### 1. Forgetting the ON Clause
```sql
-- WRONG - This will create way too many rows!
SELECT e.name, d.department_name
FROM employees e
JOIN departments d

-- RIGHT - Always specify how tables connect
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
```

### 2. Using the Wrong JOIN Type
- Use INNER JOIN when you only want rows that have matches in both tables
- Use LEFT JOIN when you want all rows from the first table, regardless of matches
- Use RIGHT JOIN when you want all rows from the second table, regardless of matches

### 3. Not Using Table Aliases with Multiple Tables
```sql
-- CONFUSING - Which table does name come from?
SELECT name, department_name
FROM employees
JOIN departments ON employees.department_id = departments.department_id

-- CLEAR - Use aliases to make it obvious
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
```

## 1.4. Practice Questions

### Basic Questions:

**"What does the FROM clause do?"**

The FROM clause tells the database which table(s) to get data from. It's processed first, before any filtering or column selection happens.

**"What's the difference between INNER JOIN and LEFT JOIN?"**

- INNER JOIN only shows rows where there's a match in both tables
- LEFT JOIN shows all rows from the first table, plus any matches from the second table (filling in blanks with NULL where there's no match)

**"When would you use a LEFT JOIN?"**

Use LEFT JOIN when you want to see all records from your main table, even if some don't have corresponding records in the other table. For example, "show all customers and their orders" - you'd want to see customers even if they haven't placed any orders yet.

### Practice Scenarios:

**"You have a customers table and an orders table. How would you list all customers and their order information?"**

```sql
SELECT c.customer_name, o.order_date, o.order_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
```

We use LEFT JOIN because we want to see ALL customers, even those who haven't placed orders yet.

**"How would you find only customers who have placed orders?"**

```sql
SELECT c.customer_name, o.order_date, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
```

We use INNER JOIN because we only want customers who appear in both tables (customers who have orders).

**"You have employees and departments tables. How would you see employee names with their department names?"**

```sql
SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
```

This assumes we only want to see employees who are assigned to a department.

## Summary

- **FROM clause**: Tells the database which table(s) to use
- **Table aliases**: Short nicknames for tables (employees AS e)
- **INNER JOIN**: Only shows matches from both tables
- **LEFT JOIN**: Shows all from first table, matches from second table
- **RIGHT JOIN**: Shows all from second table, matches from first table
- **ON clause**: Specifies how tables are connected

Remember: JOINs are like connecting puzzle pieces - you match rows based on common information between tables! 