# SQL Cheat Sheet - Quick Reference Guide

## About This Cheat Sheet

This cheat sheet provides a quick reference for SQL fundamentals, organized by the logical execution order of SQL queries. Each module focuses on a specific SQL clause or concept, providing essential syntax, rules, and tips.

## SQL Query Execution Order

**The most important concept in SQL** - Understanding this order explains alias scope, WHERE vs. HAVING usage, and overall query behavior:

<div class="sql-cheat-flow">
  <div class="cheat-flow-header">
    <h4>🚀 SQL Execution Order</h4>
  </div>
  <div class="cheat-flow-container">
    <div class="cheat-flow-step">
      <span class="cheat-step-num">1</span>
      <code>FROM</code> & <code>JOIN</code>
      <span class="cheat-step-desc">Define sources</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">2</span>
      <code>WHERE</code>
      <span class="cheat-step-desc">Filter rows</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">3</span>
      <code>GROUP BY</code>
      <span class="cheat-step-desc">Group rows</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">4</span>
      <code>HAVING</code>
      <span class="cheat-step-desc">Filter groups</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">5</span>
      <code>SELECT</code>
      <span class="cheat-step-desc">Choose columns</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">6</span>
      <code>DISTINCT</code>
      <span class="cheat-step-desc">Remove dupes</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">7</span>
      <code>ORDER BY</code>
      <span class="cheat-step-desc">Sort results</span>
    </div>
    <span class="cheat-arrow">→</span>
    
    <div class="cheat-flow-step">
      <span class="cheat-step-num">8</span>
      <code>LIMIT</code>
      <span class="cheat-step-desc">Restrict rows</span>
    </div>
  </div>
</div>

<style>
.sql-cheat-flow {
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 12px;
  border: 2px solid #0ea5e9;
  box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.1);
}

.cheat-flow-header h4 {
  margin: 0 0 1rem 0;
  color: #0c4a6e;
  font-size: 1.1rem;
  text-align: center;
  font-weight: 600;
}

.cheat-flow-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
}

.cheat-flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  min-width: 80px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #bae6fd;
  transition: transform 0.2s ease;
}

.cheat-flow-step:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.cheat-step-num {
  display: inline-block;
  width: 20px;
  height: 20px;
  background: #0ea5e9;
  color: white;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: bold;
  line-height: 20px;
  text-align: center;
  margin-bottom: 0.25rem;
}

.cheat-flow-step code {
  font-size: 0.8rem;
  font-weight: 600;
  color: #0c4a6e;
  background: none;
  padding: 0;
  margin-bottom: 0.25rem;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.cheat-step-desc {
  font-size: 0.7rem;
  color: #475569;
  line-height: 1.2;
}

.cheat-arrow {
  color: #0ea5e9;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 0.25rem;
}

/* Responsive - stack vertically on small screens */
@media (max-width: 768px) {
  .cheat-flow-container {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .cheat-arrow {
    transform: rotate(90deg);
    margin: 0;
  }
  
  .cheat-flow-step {
    min-width: 120px;
    padding: 1rem 0.75rem;
  }
  
  .cheat-flow-step code {
    font-size: 0.9rem;
  }
  
  .cheat-step-desc {
    font-size: 0.8rem;
  }
}
</style>

> **💡 Key Point**: This execution order is logical, not necessarily the physical order. Understanding it helps you write correct, efficient SQL.

## How to Use This Cheat Sheet

Each module covers one major SQL component:

- **Module 1**: FROM Clause and JOINs
- **Module 2**: WHERE Clause and Filtering  
- **Module 3**: GROUP BY and Aggregate Functions
- **Module 4**: HAVING Clause
- **Module 5**: SELECT Clause and Expressions
- **Module 6**: ORDER BY Clause
- **Module 7**: LIMIT and Result Set Control

## Quick Syntax Reference

```sql
-- Complete query structure
SELECT [DISTINCT] column_list
FROM table_name [alias]
[JOIN other_table ON condition]
[WHERE condition]
[GROUP BY column_list]
[HAVING condition]
[ORDER BY column_list [ASC|DESC]]
[LIMIT number [OFFSET number]]
```

## Key SQL Principles

1. **No guaranteed order without ORDER BY** - Results are arbitrary without explicit sorting
2. **NULL requires special handling** - Use `IS NULL`/`IS NOT NULL`, not `= NULL`
3. **Performance matters** - Write sargable conditions, index join columns
4. **DBMS variations exist** - Test syntax on your target database system
5. **Aliases have scope** - Can't use SELECT aliases in WHERE/GROUP BY/HAVING

Let's dive into each module for detailed syntax and best practices! 