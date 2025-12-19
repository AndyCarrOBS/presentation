# Data Extraction, Storage, and Presentation Flow

## Overview

This document explains how the Research Data Engineer Agent extracts data from your existing files, stores it in a structured database, and presents it for dashboards.

## 1. Data Extraction Process

### Input Sources

The agent can extract facts from:

1. **Markdown Files** (`*.md`):
   - `demographics.md` - Country demographic data
   - `specifications.md` - Operator technical specifications
   - `contacts.md` - Contact information
   - Any other structured markdown files

2. **JSON Files** (`*.json`):
   - `dashboard_data.json` - Existing dashboard data
   - Any structured JSON with country/operator data

### Extraction Methods

#### From Demographics Files

**Pattern Recognition:**
```markdown
- **Total population**: ~8.97 million (2024)
- **TV households**: ~4.2 million TV households
- **GDP (total)**: ~€450 billion (2024)
```

**Extracted Facts:**
- `entity_type`: `country`
- `entity_id`: `Austria`
- `attribute`: `population_million`
- `value`: `8.97`
- `value_type`: `number`
- `unit`: `million`
- `source`: File path + modification date

#### From Specification Files

**Pattern Recognition:**
```markdown
- **Country**: Austria
- **Operator**: ORF
- **Version**: HbbTV 2.0.4 (TS 102 796 v1.7.1)
- **URL**: https://www.hbbtv.org/
```

**Extracted Facts:**
- `entity_type`: `operator`
- `entity_id`: `ORF`
- `attribute`: `hbbtv_version`
- `value`: `2.0.4`
- `source`: File path + modification date
- `references`: URLs found in the file

### Example Extraction

```python
from agents.research_data_engineer import ResearchDataEngineer

agent = ResearchDataEngineer(db_path='research_data.db')

# Extract from markdown
facts = agent.extract_facts_from_markdown('Europe/Austria/demographics.md')
# Returns: [{'fact_id': 1, 'type': 'population'}, ...]

# Extract from JSON
facts = agent.extract_facts_from_json('dashboard_data.json')
```

## 2. Database Storage Structure

### Schema Overview

```
┌─────────────┐
│   facts     │  Core data points
│             │  - entity_type, entity_id, attribute, value
│             │  - value_type, unit, created_at, is_current
└──────┬──────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────┐  ┌────▼──────────┐
│   sources   │  │fact_sources   │  Links facts to sources
│             │  │               │  with confidence scores
│ - file/URL  │  │ - fact_id     │
│ - date      │  │ - source_id   │
│ - metadata  │  │ - confidence  │
└─────────────┘  └───────────────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────────┐  ┌──────▼──────────┐
│fact_references  │  │external_data    │
│                 │  │                 │
│ - URLs          │  │ - web search     │
│ - citations     │  │ - API data      │
│ - documents     │  │ - snapshots     │
└─────────────────┘  └─────────────────┘
```

### Facts Table

Stores the core data points:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `entity_type` | TEXT | `country`, `operator`, `specification` |
| `entity_id` | TEXT | `Austria`, `ORF`, etc. |
| `attribute` | TEXT | `population_million`, `hbbtv_version` |
| `value` | TEXT | The actual value (as string) |
| `value_type` | TEXT | `string`, `number`, `boolean`, `json` |
| `unit` | TEXT | `million`, `percent`, `version` |
| `created_at` | TIMESTAMP | When fact was recorded |
| `is_current` | BOOLEAN | Latest version flag |

### Source Tracking

Every fact is linked to its source:

```python
# Example fact with source
{
    'id': 1,
    'entity_type': 'country',
    'entity_id': 'Austria',
    'attribute': 'population_million',
    'value': '8.97',
    'sources': [
        {
            'source_type': 'file',
            'source_path': 'Europe/Austria/demographics.md',
            'source_date': '2024-12-15',
            'confidence_score': 1.0,
            'extraction_method': 'regex_pattern'
        }
    ],
    'references': [
        {
            'reference_url': 'https://example.com/data',
            'reference_title': 'Official Statistics'
        }
    ]
}
```

## 3. Data Presentation

### Dashboard Generation

The agent generates dashboard data compatible with your existing `dashboard.html`:

```python
dashboard = agent.generate_dashboard_data()

# Output structure:
{
    'countries': {
        'Austria': {
            'population_million': 8.97,
            'tv_homes_million': 4.2,
            ...
        }
    },
    'operators': {
        'Austria': {
            'ORF': {
                'hbbtv_version': '2.0.4',
                'has_specification': True,
                ...
            }
        }
    },
    'statistics': {
        'total_countries': 25,
        'total_operators': 50,
        'total_facts': 500
    }
}
```

### Presentation Formats

#### 1. JSON Dashboard (for existing dashboard.html)

```bash
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json
```

This generates a JSON file that your existing `dashboard.html` can consume directly.

#### 2. Database Queries (for custom visualizations)

```bash
# Query all country facts
python -m agents.research_data_engineer.cli query \
  --entity-type country \
  --format json

# Query specific operator
python -m agents.research_data_engineer.cli query \
  --entity-type operator \
  --entity-id ORF
```

#### 3. Trend Analysis (for time-series charts)

```bash
python -m agents.research_data_engineer.cli trend \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million
```

Output:
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

## 4. Complete Workflow Example

### Step 1: Extract All Data

```bash
# Extract from all markdown files
find Europe -name "*.md" -type f | \
  xargs python -m agents.research_data_engineer.cli extract

# Extract from JSON
python -m agents.research_data_engineer.cli extract dashboard_data.json
```

### Step 2: Enrich with External Data (optional)

```bash
# Enrich population data with web research
python -m agents.research_data_engineer.cli enrich \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million \
  --queries "Austria population 2024" "Austria demographics"
```

### Step 3: Validate Data Quality

```bash
# Validate all facts
python -m agents.research_data_engineer.cli validate
```

### Step 4: Generate Dashboard

```bash
# Generate dashboard JSON
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json
```

### Step 5: View in Dashboard

Open `dashboard.html` in a browser - it will automatically load `dashboard_data.json`.

## 5. Data Quality Tracking

Each fact has quality metrics:

- **Completeness**: Based on number of sources and references
- **Accuracy**: Based on source confidence scores
- **Freshness**: Based on source dates

```python
# Get quality metrics
fact = agent.db.get_fact_with_sources(fact_id)
quality = agent.validate_and_clean_fact(fact_id)

print(f"Completeness: {quality['completeness']:.2f}")
print(f"Accuracy: {quality['accuracy']:.2f}")
print(f"Freshness: {quality['freshness']:.2f}")
```

## 6. Integration with Existing Dashboard

The agent is designed to be a drop-in replacement for your existing data extraction:

**Before:**
```bash
python scripts/extract_dashboard_data.py
# Generates dashboard_data.json
```

**After:**
```bash
python -m agents.research_data_engineer.cli extract Europe/**/*.md
python -m agents.research_data_engineer.cli dashboard --output dashboard_data.json
# Generates dashboard_data.json with source tracking
```

Your existing `dashboard.html` works without changes!

## 7. Advantages Over Current System

1. **Source Tracking**: Every fact knows where it came from
2. **Date Tracking**: Track when data was collected (important for trends)
3. **Versioning**: Historical data for trend analysis
4. **Quality Metrics**: Automatic quality scoring
5. **External Enrichment**: Can fetch additional data from web
6. **Citations**: Automatic reference management
7. **Structured Storage**: SQLite database instead of just JSON

## 8. Next Steps

1. **Extract all existing data**:
   ```bash
   find Europe -name "*.md" | xargs python -m agents.research_data_engineer.cli extract
   ```

2. **Generate new dashboard**:
   ```bash
   python -m agents.research_data_engineer.cli dashboard --output dashboard_data.json
   ```

3. **View trends**:
   ```bash
   python -m agents.research_data_engineer.cli trend --entity-type country --entity-id Austria --attribute population_million
   ```

4. **Query specific data**:
   ```bash
   python -m agents.research_data_engineer.cli query --entity-type operator
   ```
