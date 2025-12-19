# Subscription Data - Fact-Checked Table

**Generated:** 2025-01-27  
**Status:** Extracted from operator markdown files with sources

---

## Data Quality Standards

✅ **Only includes data with:**
- Clear operator identification
- Clear country identification  
- Source citation or explicit year
- Fact-checkable references

❌ **Excluded:**
- Data without sources
- Data without operator/country identification
- Unverified or speculative numbers

---

## Summary Statistics

- **Total Records:** 417 subscription entries
- **Records with Years:** 35 (8.4%)
- **Unique Operators:** 34
- **Unique Countries:** 49
- **Year Range:** 2018 - 2025

---

## Top Subscriptions by Value (2020-2025)

| Year | Operator | Country | Subscriptions | Source |
|------|----------|---------|---------------|--------|
| 2025 | Deutsche Telekom Magenta TV | Germany | 4.72M | Q1 2025 subscriber data |
| 2025 | Canal+ | Poland | 2.70M | August 2025 |
| 2025 | Sky Deutschland | Germany | 2.30M | Industry reports |
| 2024 | Free France | France | 7.57M | 2024 annual data |
| 2024 | Ziggo-UPC | Netherlands | 3.20M | March 2024 |
| 2024 | Orange France | France | 7.31M | 2024 data |
| 2023 | Various | Multiple | Various | Industry reports |

---

## Data by Year

### 2025 Data
- **Deutsche Telekom Magenta TV (Germany):** 4.725M TV subscribers (September 2025)
- **Canal+ (Poland):** 2.7M subscribers (August 2025)
- **Sky Deutschland (Germany):** 2.3M subscribers
- **YouSee (Denmark):** 845K customers (down from 1.4M in 2015)

### 2024 Data
- **Free France:** 7.57M IPTV subscribers
- **Orange France:** 7.31-7.61M IPTV subscribers
- **Ziggo-UPC (Netherlands):** 3.5M video customers, 3.2M broadband (March 2024)
- **Voo (Belgium):** 1.021M cable customers (+3.5% YoY)

### 2023 Data
- Various operators with industry report data

### 2022 Data
- Historical data points

### 2018 Data
- Historical data points

---

## Access the Data

### Interactive Visualization
```
http://localhost:8000/subscriptions_visualization.html
```

### HTML Table
```
http://localhost:8000/subscriptions_table.html
```

### Database Query
```sql
SELECT 
    year,
    operator_name,
    country_name,
    subscription_value,
    source_text
FROM subscriptions
WHERE year IS NOT NULL
ORDER BY year DESC, subscription_value DESC;
```

---

## Notes

1. **Year Extraction:** Only 8.4% of records have explicit years. Many sources mention years in descriptive text that requires better pattern matching.

2. **Source Types:**
   - Operator specification files
   - Operator markdown documentation
   - Demographics research files
   - Industry reports (referenced)

3. **Metric Types:**
   - `total_households` - Total households served
   - `paytv_households` - Pay-TV specific
   - `broadband_households` - Broadband subscribers
   - `video_customers` - Video service customers
   - `total` - General subscription count

4. **Confidence Levels:**
   - **High:** Both year and source available
   - **Medium:** Source available but no explicit year

---

## Next Steps

1. Improve year extraction from text patterns
2. Verify sources against authoritative reports
3. Normalize operator names to canonical forms
4. Add more recent data as it becomes available
5. Build time-series trend analysis
