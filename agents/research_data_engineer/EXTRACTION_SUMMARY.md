# Data Extraction, Storage & Presentation Summary

## How Data is Extracted

### From Your Existing Files

**1. Markdown Files (demographics.md, specifications.md)**
```
Input: Europe/Austria/demographics.md
  - **Total population**: ~8.97 million (2024)
  - **TV households**: ~4.2 million

Extracted Facts:
  ✅ country/Austria/population_million = 8.97
  ✅ country/Austria/tv_homes_million = 4.2
  📎 Source: Europe/Austria/demographics.md (2024-12-15)
```

**2. Specification Files**
```
Input: Europe/Austria/ORF/specifications.md
  - **Operator**: ORF
  - **Version**: HbbTV 2.0.4
  - **URL**: https://www.hbbtv.org/

Extracted Facts:
  ✅ operator/ORF/hbbtv_version = 2.0.4
  ✅ operator/ORF/has_specification = True
  📎 Source: Europe/Austria/ORF/specifications.md
  🔗 Reference: https://www.hbbtv.org/
```

**3. JSON Files (dashboard_data.json)**
```
Input: dashboard_data.json
  {
    "countries": {
      "Austria": {
        "population_million": "8.97"
      }
    }
  }

Extracted Facts:
  ✅ country/Austria/population_million = 8.97
  📎 Source: dashboard_data.json
```

## How Data is Stored

### Database Structure

**Facts Table** - Core data points
```
id | entity_type | entity_id | attribute        | value  | value_type | created_at
1  | country     | Austria   | population_million | 8.97  | number     | 2024-12-15
2  | operator    | ORF       | hbbtv_version     | 2.0.4  | string     | 2024-12-15
```

**Sources Table** - Where data came from
```
id | source_type | source_path                          | source_date
1  | file        | Europe/Austria/demographics.md      | 2024-12-15
2  | file        | Europe/Austria/ORF/specifications.md | 2024-12-15
```

**Fact-Sources Link** - Links facts to sources
```
fact_id | source_id | confidence_score | extraction_method
1       | 1         | 1.0              | regex_pattern
2       | 2         | 1.0              | regex_pattern
```

**References Table** - External citations
```
fact_id | reference_url              | reference_title
2       | https://www.hbbtv.org/     | HbbTV Consortium
```

### Key Features

✅ **Source Tracking**: Every fact knows its source file and date
✅ **Versioning**: Historical data for trend analysis
✅ **References**: URLs and citations automatically tracked
✅ **Quality Metrics**: Completeness, accuracy, freshness scores

## How Data is Presented

### 1. JSON Dashboard (for dashboard.html)

**Command:**
```bash
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json
```

**Output Format:**
```json
{
  "countries": {
    "Austria": {
      "population_million": "8.97",
      "tv_homes_million": "4.2"
    }
  },
  "operators": {
    "Austria": {
      "ORF": {
        "hbbtv_version": "2.0.4",
        "has_specification": true
      }
    }
  },
  "statistics": {
    "total_countries": 25,
    "total_operators": 50,
    "total_facts": 500
  }
}
```

**Usage:** Your existing `dashboard.html` loads this JSON automatically!

### 2. Database Queries (for custom analysis)

**Command:**
```bash
python -m agents.research_data_engineer.cli query \
  --entity-type country \
  --entity-id Austria
```

**Output:**
```
Found 2 facts:

  [country] Austria.population_million = 8.97 (number)
    Type: number, Created: 2024-12-15 10:30:00
    Source: Europe/Austria/demographics.md (2024-12-15)

  [country] Austria.tv_homes_million = 4.2 (number)
    Type: number, Created: 2024-12-15 10:30:00
    Source: Europe/Austria/demographics.md (2024-12-15)
```

### 3. Trend Analysis (for time-series)

**Command:**
```bash
python -m agents.research_data_engineer.cli trend \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million
```

**Output:**
```json
{
  "entity_type": "country",
  "entity_id": "Austria",
  "attribute": "population_million",
  "data_points": 5,
  "first_recorded": "2024-01-15",
  "last_recorded": "2024-12-15",
  "current_value": 8.97,
  "trend": "increasing"
}
```

## Complete Workflow

### Step 1: Extract from All Files
```bash
# Extract from all markdown files
find Europe -name "*.md" -type f | \
  xargs python -m agents.research_data_engineer.cli extract

# Extract from JSON
python -m agents.research_data_engineer.cli extract dashboard_data.json
```

### Step 2: Generate Dashboard
```bash
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json
```

### Step 3: View Dashboard
Open `dashboard.html` in browser - it automatically loads `dashboard_data.json`

## Data Flow Diagram

```
┌─────────────────┐
│  Source Files   │
│                 │
│ • demographics  │
│ • specifications│
│ • JSON files    │
└────────┬────────┘
         │
         │ extract_facts_from_*
         ▼
┌─────────────────┐
│  Research Agent  │
│                 │
│ • Parse files   │
│ • Extract facts │
│ • Clean data    │
└────────┬────────┘
         │
         │ add_fact()
         ▼
┌─────────────────┐
│  SQLite Database│
│                 │
│ • facts         │
│ • sources       │
│ • references    │
└────────┬────────┘
         │
         │ generate_dashboard_data()
         ▼
┌─────────────────┐
│  Dashboard JSON │
│                 │
│ • countries     │
│ • operators     │
│ • statistics    │
└────────┬────────┘
         │
         │ Load in browser
         ▼
┌─────────────────┐
│  dashboard.html  │
│                 │
│ • Visual display│
│ • Interactive    │
└─────────────────┘
```

## Key Advantages

1. **Source Provenance**: Every fact tracks where it came from
2. **Date Tracking**: Know when data was collected (critical for trends)
3. **Historical Data**: Track changes over time
4. **Quality Metrics**: Automatic scoring of data quality
5. **Citations**: Automatic reference management
6. **Structured Storage**: SQLite database for efficient querying

## Example: Complete Extraction Session

```bash
# 1. Extract from demographics
$ python -m agents.research_data_engineer.cli extract \
    Europe/Austria/demographics.md
✅ Extracted 2 facts from demographics.md

# 2. Extract from specifications
$ python -m agents.research_data_engineer.cli extract \
    Europe/Austria/ORF/specifications.md
✅ Extracted 7 facts from specifications.md

# 3. Query what we extracted
$ python -m agents.research_data_engineer.cli query \
    --entity-type country --entity-id Austria
Found 2 facts:
  [country] Austria.population_million = 8.97
  [country] Austria.tv_homes_million = 4.2

# 4. Generate dashboard
$ python -m agents.research_data_engineer.cli dashboard \
    --output dashboard_data.json
✅ Dashboard saved to dashboard_data.json

# 5. View statistics
$ python -m agents.research_data_engineer.cli stats
📊 Database Statistics
   Total facts: 9
   Countries: 1
   Operators: 1
```

## Integration with Existing System

The agent is designed as a **drop-in replacement** for your current extraction:

**Before:**
```bash
python scripts/extract_dashboard_data.py
# → dashboard_data.json
```

**After:**
```bash
python -m agents.research_data_engineer.cli extract Europe/**/*.md
python -m agents.research_data_engineer.cli dashboard --output dashboard_data.json
# → dashboard_data.json (with source tracking!)
```

Your `dashboard.html` works **without any changes**!
