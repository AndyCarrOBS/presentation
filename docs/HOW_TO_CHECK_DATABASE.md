# How to Check Database Contents

## Quick Overview

The database `broadcast_industry.db` contains:
- **196 countries** across 6 regions
- **55 operators** with country relationships
- **318 facts** about countries (demographics, market data)
- **70 operator-country relationships**

## Method 1: Using the Explore Script (Recommended)

### Show Everything
```bash
python3 scripts/explore_database.py --all
```

### Interactive Menu
```bash
python3 scripts/explore_database.py
```

Then choose from the menu:
1. Database Statistics
2. Countries by Region
3. Top Operators by Country Coverage
4. Top Countries by Operator Count
5. Multi-Country Operators
6. Operator Details (all)
7. Facts Summary
8. Search Operator
9. Show All

## Method 2: Direct SQL Queries

### Using Python
```python
import sqlite3

conn = sqlite3.connect('broadcast_industry.db')
cursor = conn.cursor()

# Example: List all operators
cursor.execute("SELECT canonical_name FROM operators ORDER BY canonical_name")
for row in cursor.fetchall():
    print(row[0])

conn.close()
```

### Using SQLite CLI (if installed)
```bash
sqlite3 broadcast_industry.db
```

Then run SQL queries:
```sql
-- List all operators
SELECT canonical_name, COUNT(country_id) as countries
FROM operators o
LEFT JOIN operator_countries oc ON o.operator_id = oc.operator_id
GROUP BY o.operator_id
ORDER BY countries DESC;

-- Show operators in a specific country
SELECT o.canonical_name, oc.operator_name_in_country
FROM operators o
JOIN operator_countries oc ON o.operator_id = oc.operator_id
JOIN countries c ON oc.country_id = c.country_id
WHERE c.country_name = 'Austria';

-- Show countries for a specific operator
SELECT c.country_name, oc.operator_name_in_country
FROM countries c
JOIN operator_countries oc ON c.country_id = oc.country_id
JOIN operators o ON oc.operator_id = o.operator_id
WHERE o.canonical_name = 'M7 Group';
```

## Method 3: Using Database Views

The database includes pre-built views for common queries:

```sql
-- Operators summary with country counts
SELECT * FROM v_operators_summary LIMIT 10;

-- Countries with operator counts
SELECT * FROM v_countries_operators 
WHERE region = 'Europe' 
ORDER BY operator_count DESC 
LIMIT 10;

-- Latest facts for countries
SELECT * FROM v_facts_latest 
WHERE entity_type = 'country' 
AND entity_name = 'Austria';
```

## Common Queries

### Find all operators in a country
```sql
SELECT o.canonical_name, oc.operator_name_in_country
FROM operators o
JOIN operator_countries oc ON o.operator_id = oc.operator_id
JOIN countries c ON oc.country_id = c.country_id
WHERE c.country_name = 'Germany'
ORDER BY o.canonical_name;
```

### Find all countries for an operator
```sql
SELECT c.country_name, c.region, oc.operator_name_in_country
FROM countries c
JOIN operator_countries oc ON c.country_id = oc.country_id
JOIN operators o ON oc.operator_id = o.operator_id
WHERE o.canonical_name = 'Allente'
ORDER BY c.country_name;
```

### Get country demographics
```sql
SELECT 
    e.canonical_name as country,
    f.fact_type,
    f.value_json as value,
    f.unit,
    f.observed_at
FROM facts f
JOIN entities e ON f.entity_id = e.entity_id
WHERE e.entity_type = 'country' 
AND e.canonical_name = 'France'
ORDER BY f.fact_type;
```

### Multi-country operators
```sql
SELECT 
    o.canonical_name,
    COUNT(oc.country_id) as country_count,
    GROUP_CONCAT(c.country_name, ', ') as countries
FROM operators o
JOIN operator_countries oc ON o.operator_id = oc.operator_id
JOIN countries c ON oc.country_id = c.country_id
GROUP BY o.operator_id
HAVING country_count > 1
ORDER BY country_count DESC;
```

## Database Schema

### Main Tables
- `countries` - All countries with regions
- `operators` - Canonical operator names with aliases
- `operator_countries` - Many-to-many relationship
- `entities` - Unified entity tracking
- `facts` - All facts with full provenance
- `sources` - Data source tracking

### Views
- `v_operators_summary` - Operators with country counts
- `v_countries_operators` - Countries with operator lists
- `v_facts_latest` - Most recent facts per entity
- `v_facts_timeseries` - Time-series data
- `v_countries_with_facts` - Countries with data coverage

## Quick Stats

Run this to see current database statistics:
```bash
python3 scripts/explore_database.py --all | head -30
```

Or in Python:
```python
import sqlite3
conn = sqlite3.connect('broadcast_industry.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM countries")
print(f"Countries: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM operators")
print(f"Operators: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM operator_countries")
print(f"Relationships: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM facts")
print(f"Facts: {cursor.fetchone()[0]}")

conn.close()
```

## Troubleshooting

### Database not found
Make sure you're in the project root directory:
```bash
cd /home/andycarr/code/business-dev/presentation
```

### Check if database exists
```bash
ls -lh broadcast_industry.db
```

### Verify database integrity
```bash
python3 scripts/verify_database.py
```
