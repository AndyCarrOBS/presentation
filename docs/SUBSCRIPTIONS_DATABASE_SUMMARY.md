# Subscriptions Database - Summary Report

**Generated:** 2025-01-27  
**Database:** `broadcast_industry.db`  
**Table:** `subscriptions`

---

## Summary of Actions Taken

1. **Created subscriptions table** following data engineer rules:
   - Full provenance tracking (source_id, source_text, file_path)
   - Date semantics (year, observed_at)
   - Links to operators and countries tables
   - Confidence levels for data quality

2. **Extracted subscription data** from markdown files:
   - Scanned 222 markdown files
   - Found 686 potential subscription entries
   - Filtered to 417 valid records (with operator, country, and source/year)
   - 35 records have explicit years (2018, 2022, 2023, 2024, 2025)

3. **Data quality filtering**:
   - Only includes data with clear sources
   - Only includes data with years or explicit source citations
   - Excludes entries without operator or country identification

---

## Tables Affected

### subscriptions
- **Records:** 417 subscription records
- **Purpose:** Track subscriber/subscription numbers with full provenance
- **Key Fields:** 
  - operator_name, country_name
  - subscription_value, unit, metric_type
  - year, observed_at
  - source_id, source_text, file_path
  - confidence

---

## Records Inserted

### Subscription Records
- **417 total records** inserted
- **35 records with explicit years** (2018, 2022, 2023, 2024, 2025)
- **382 records with sources** but no explicit year
- **31 unique operators** represented
- **46 unique countries** represented

### Year Distribution
- **2025:** Most recent data (multiple operators)
- **2024:** Recent data (multiple operators)
- **2023:** Historical data
- **2022:** Historical data
- **2018:** Historical data

### Top Operators by Data Points
1. Deutsche Telekom Magenta TV (Germany) - Multiple years
2. Canal+ (Poland) - 2025 data
3. Sky Deutschland (Germany) - 2025 data
4. YouSee (Denmark) - 2025 data
5. Free France (France) - Multiple data points

---

## Sources with Published_at and Retrieved_at

### Source Types Identified
1. **Operator specification files** - From `specifications.md` files
2. **Operator markdown files** - From `Operators/` directory
3. **Demographics files** - From country demographics research
4. **Research summaries** - From aggregated research documents
5. **Industry reports** - Referenced in source text

### Source Provenance
- **Source ID tracking:** All records linked to sources table
- **Source text:** Extracted from file context or explicit citations
- **File paths:** Full paths to source files for verification
- **Retrieved dates:** 2025-01-27 (extraction date)

---

## Data Quality Checks Performed

### ✅ Completeness Checks
- All records have operator_name (417/417)
- All records have country_name (417/417)
- All records have subscription_value (417/417)
- All records have source_text or source_id (417/417)
- 35 records have explicit years (8.4%)

### ✅ Data Quality Metrics
- **Confidence Levels:**
  - High: Records with both year and source
  - Medium: Records with source but no explicit year
- **Metric Types Identified:**
  - total_households
  - paytv_households
  - broadband_households
  - ftth_households
  - video_customers
  - total (default)

### ⚠️ Areas for Improvement
1. **Year Extraction:** Only 8.4% of records have explicit years
   - Many sources mention years in text but not in structured format
   - Need better pattern matching for year extraction
2. **Operator Name Normalization:** Some entries may need canonical name mapping
3. **Value Validation:** Some values may need review (e.g., mobile customers vs TV subscribers)
4. **Source Verification:** Some sources are file names rather than authoritative citations

---

## Example Queries

### Subscriptions by Year
```sql
SELECT 
    year,
    COUNT(*) as record_count,
    COUNT(DISTINCT operator_name) as operators,
    COUNT(DISTINCT country_name) as countries
FROM subscriptions
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year DESC;
```

### Top Operators by Subscriptions (2025)
```sql
SELECT 
    operator_name,
    country_name,
    subscription_value,
    source_text
FROM subscriptions
WHERE year = 2025
ORDER BY subscription_value DESC
LIMIT 10;
```

### Subscriptions by Country
```sql
SELECT 
    country_name,
    COUNT(*) as records,
    COUNT(DISTINCT operator_name) as operators,
    MAX(subscription_value) as max_subscriptions
FROM subscriptions
WHERE year IS NOT NULL
GROUP BY country_name
ORDER BY records DESC;
```

### Time Series for Specific Operator
```sql
SELECT 
    year,
    subscription_value,
    source_text
FROM subscriptions
WHERE operator_name = 'Deutsche Telekom Magenta TV'
  AND country_name = 'Germany'
  AND year IS NOT NULL
ORDER BY year;
```

---

## Files Generated

1. **subscriptions_table.html** - Simple HTML table of all subscription data
2. **subscriptions_visualization.html** - Interactive visualization with charts
3. **Database table:** `subscriptions` in `broadcast_industry.db`

---

## Access the Data

### View HTML Table
```
http://localhost:8000/subscriptions_table.html
```

### View Interactive Visualization
```
http://localhost:8000/subscriptions_visualization.html
```

### Query Database
```python
import sqlite3
conn = sqlite3.connect('broadcast_industry.db')
cursor = conn.cursor()
cursor.execute("""
    SELECT operator_name, country_name, year, subscription_value, source_text
    FROM subscriptions
    WHERE year IS NOT NULL
    ORDER BY year DESC, subscription_value DESC
""")
```

---

## Next Steps

1. **Improve Year Extraction:** Better pattern matching for years in text
2. **Source Verification:** Cross-reference with authoritative sources
3. **Data Validation:** Review and validate subscription values
4. **Operator Normalization:** Map to canonical operator names
5. **Add More Data:** Continue extracting from additional sources
6. **Time Series Analysis:** Build trend analysis for operators with multiple years

---

**Data Engineer Compliance:**
- ✅ All facts have sources
- ✅ Full provenance tracking (source_id, source_text, file_path)
- ✅ Date semantics (year, observed_at)
- ✅ Confidence levels recorded
- ⚠️ Year extraction needs improvement (only 8.4% have explicit years)
- ⚠️ Some sources need verification (file names vs authoritative citations)
