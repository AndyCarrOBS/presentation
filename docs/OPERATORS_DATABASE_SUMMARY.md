# Operators Database - Summary Report

**Generated:** 2025-01-27  
**Database:** `broadcast_industry.db`  
**Schema Version:** 1.1

---

## Summary of Actions Taken

1. **Created operators database schema**:
   - `operators` table for canonical operator entities with aliases
   - `operator_countries` junction table for many-to-many relationships
   - Indexes for performance optimization
   - Dashboard-ready views for operators and countries

2. **Scanned directory structure**:
   - Processed 78 operator directories in Europe/
   - Extracted operators from specifications.md files
   - Identified operator-country relationships

3. **Normalized operator names**:
   - Created canonical names for operators with variations
   - Handled aliases (e.g., "M7 HD Austria" → "M7 Group")
   - Mapped 55 unique operators from various name variations

4. **Loaded operator data**:
   - Created 55 operator entities
   - Created 70 operator-country relationships
   - Linked operators to countries with full provenance

---

## Tables Affected

### 1. operators
- **Records:** 55 operators
- **Purpose:** Canonical operator entities with aliases
- **Key Fields:** canonical_name, aliases, parent_company, website

### 2. operator_countries
- **Records:** 70 relationships
- **Purpose:** Many-to-many relationship between operators and countries
- **Key Fields:** operator_id, country_id, operator_name_in_country, source_id, notes

### 3. entities (updated)
- **Records:** 46 countries + 55 operators = 101 entities
- **Purpose:** Unified entity tracking
- **Key Fields:** entity_type, canonical_name, aliases

---

## Records Inserted/Updated

### Operators Table
- **55 operators** inserted with canonical names
- **Aliases tracked** for name variations across countries
- Examples:
  - M7 Group (aliases: M7 HD Austria, M7 Telesat, M7 Skylink CZ, etc.)
  - Deutsche Telekom Magenta TV (aliases: Magenta TV)
  - UPC (aliases: Ziggo/UPC, UPC (Vodafone))

### Operator-Country Relationships
- **70 relationships** created linking operators to countries
- Each relationship includes:
  - Operator name as used in that country
  - Source provenance
  - Notes about the relationship

### Top Operators by Country Coverage
1. **M7 Group**: 6 countries (Austria, Belgium, Czech Republic, Netherlands, Luxembourg, Slovakia)
2. **Allente**: 4 countries (Denmark, Finland, Norway, Sweden)
3. **Sky**: 3 countries (Germany, Ireland, Italy)
4. **UPC**: 3 countries (Czech Republic, Poland, Switzerland)
5. **Boxer HD**: 2 countries (Denmark, Sweden)
6. **Canal+**: 2 countries (France, Poland)
7. **Orange**: 2 countries (France, Poland)
8. **Telenor**: 2 countries (Norway, Sweden)

### Top Countries by Operator Count
1. **Austria**: 7 operators
2. **France**: 7 operators
3. **Czech Republic**: 5 operators
4. **Denmark**: 5 operators
5. **Germany**: 5 operators
6. **Italy**: 5 operators
7. **Switzerland**: 5 operators
8. **Belgium**: 4 operators
9. **Ireland**: 4 operators
10. **Norway**: 4 operators

---

## Sources with Published_at and Retrieved_at

### Source: Internal Research (Operator Directory Structure)
- **Source ID:** 2
- **Publisher:** Internal Research
- **URL:** file://Europe/
- **Published At:** 2024-01-01 (approximate)
- **Retrieved At:** 2025-01-27
- **Relationships Count:** 70
- **License Notes:** None specified

---

## Data Quality Checks Performed

### ✅ Completeness Checks
- All operator-country relationships have source_id (0 missing)
- All relationships linked to valid operators (0 orphaned)
- All relationships linked to valid countries (1 warning for "Multi-Country" - expected)

### ✅ Name Normalization
- **55 unique operators** identified from various name forms
- **Aliases tracked** for name variations (e.g., "M7 HD Austria" → "M7 Group")
- **Canonical names** established for consistent reference

### ✅ Relationship Integrity
- All relationships have both operator_id and country_id
- No duplicate relationships (UNIQUE constraint enforced)
- Operator names in country context preserved

### ⚠️ Areas for Improvement
1. **Parent Company Data:** Not yet extracted from source files
2. **Website URLs:** Not yet extracted from source files
3. **Additional Metadata:** Operator specifications, CAS systems, etc. not yet loaded
4. **Multi-Country Operators:** "Multi-Country / Service Provider" not in countries table (expected)

---

## Example Queries for Dashboards

### Operators by Country
```sql
SELECT 
    c.country_name,
    c.region,
    o.canonical_name as operator,
    oc.operator_name_in_country
FROM countries c
JOIN operator_countries oc ON c.country_id = oc.country_id
JOIN operators o ON oc.operator_id = o.operator_id
WHERE c.region = 'Europe'
ORDER BY c.country_name, o.canonical_name;
```

### Multi-Country Operators
```sql
SELECT 
    o.canonical_name,
    o.aliases,
    COUNT(oc.country_id) as country_count,
    GROUP_CONCAT(c.country_name, ', ') as countries
FROM operators o
JOIN operator_countries oc ON o.operator_id = oc.operator_id
JOIN countries c ON oc.country_id = c.country_id
GROUP BY o.operator_id, o.canonical_name
HAVING country_count > 1
ORDER BY country_count DESC, o.canonical_name;
```

### Countries with Most Operators
```sql
SELECT 
    c.country_name,
    c.region,
    COUNT(oc.operator_id) as operator_count
FROM countries c
JOIN operator_countries oc ON c.country_id = oc.country_id
WHERE c.region = 'Europe'
GROUP BY c.country_id, c.country_name, c.region
ORDER BY operator_count DESC, c.country_name;
```

### Operator Name Variations
```sql
SELECT 
    o.canonical_name,
    o.aliases,
    oc.operator_name_in_country,
    c.country_name
FROM operators o
JOIN operator_countries oc ON o.operator_id = oc.operator_id
JOIN countries c ON oc.country_id = c.country_id
WHERE o.aliases IS NOT NULL
ORDER BY o.canonical_name, c.country_name;
```

---

## Operator Name Normalization Examples

The following operators have been normalized to canonical names:

| Canonical Name | Aliases/Variations |
|----------------|-------------------|
| M7 Group | M7 HD Austria, M7 Telesat, M7 Skylink CZ, M7 Skylink SK, M7 Canal Digitaal, M7 (UPC Direct) |
| Deutsche Telekom Magenta TV | Magenta TV, Magenta TV (UPC) |
| UPC | UPC (Vodafone), Ziggo/UPC, Ziggo-UPC |
| Allente | Allente (appears in multiple Nordic countries) |
| SimpliTV | SimpliTV SAT, SimpliTV Terrestrial |
| Sky | Sky Deutschland, Sky Ireland, Sky-Italia, SKY |
| Canal+ | Canal+ France, nc+/Canal+, CANAL+-Polska |
| Vodafone | Vodafone Germany, Vodafone (Unity Media), KDG/Vodafone, Vodafone-Czech-Republic |
| Orange | Orange France, Orange-Polska |
| O2 | O2 Germany, O2-Czech-Republic |

---

## Next Steps

1. **Extract Operator Metadata**: Parse specifications.md files for:
   - Parent company information
   - Website URLs
   - Technical specifications
   - CAS systems used

2. **Add Operator Facts**: Create facts table entries for:
   - Subscriber counts
   - Market share
   - Platform types (Satellite, Cable, IPTV, OTT)
   - Technology stack

3. **Enrich with External Sources**: Add:
   - Company registration numbers
   - Industry classifications
   - Financial data

4. **Expand to Other Regions**: Apply same process for:
   - Asia
   - Americas
   - Africa
   - Oceania

---

## Database Files

- **Database:** `broadcast_industry.db` (SQLite)
- **Schema:** `database_schema.sql` (updated)
- **Creation Script:** `scripts/create_operators_database.py`
- **Verification:** Run `scripts/verify_database.py` for full verification

---

**Data Engineer Compliance:**
- ✅ All relationships have sources
- ✅ Full provenance tracking (source_id, notes)
- ✅ Canonical entities with aliases
- ✅ Many-to-many relationships properly modeled
- ✅ Unique constraints prevent duplicates
- ⚠️ Additional metadata (parent_company, website) to be extracted
