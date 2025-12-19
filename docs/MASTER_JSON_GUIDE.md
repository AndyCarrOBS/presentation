# Master JSON File Guide

## Overview

The `master_data.json` file contains all data from the research database in a structured format optimized for visualization.

**File:** `master_data.json`  
**Size:** ~780KB  
**Last Updated:** 2024-12-15

## File Structure

```json
{
  "metadata": {
    "export_date": "2024-12-15T...",
    "total_facts": 490,
    "total_sources": 168,
    "total_references": 438,
    "total_external_data": 0
  },
  "countries": {
    "Austria": {
      "attributes": {
        "population_million": {
          "value": 8.97,
          "value_type": "number",
          "unit": "million",
          "created_at": "...",
          "sources": [...],
          "references": [...]
        },
        ...
      },
      "facts": [...]
    },
    ...
  },
  "operators": {
    "KPN": {
      "attributes": {
        "subscribers": {
          "value": 2170000,
          "value_type": "number",
          "unit": "subscribers",
          "sources": [...],
          "references": [...]
        },
        "hbbtv_version": {
          "value": "2.0.1",
          "value_type": "string",
          "sources": [...]
        },
        ...
      },
      "facts": [...]
    },
    ...
  },
  "broadcasters": {
    "NPO": {
      "attributes": {
        "type": {
          "value": "PSB",
          "value_type": "string",
          "sources": [...]
        }
      },
      "facts": [...]
    },
    ...
  },
  "sources": {
    "1": {
      "source_type": "file",
      "source_path": "Europe/Austria/demographics.md",
      "source_name": "Austria demographics",
      "source_date": "2024-12-15"
    },
    ...
  },
  "statistics": {
    "countries": {
      "total": 46,
      "with_population": 46,
      "with_tv_homes": 46,
      "with_gdp": 39
    },
    "operators": {
      "total": 79,
      "with_subscribers": 51,
      "with_hbbtv": 17,
      "with_ci": 29,
      "with_ca": 12,
      "with_market_share": 36
    },
    "broadcasters": {
      "total": 86,
      "psbs": 86
    }
  },
  "flattened": {
    "countries": [
      {
        "country": "Austria",
        "population_million": 8.97,
        "tv_homes_million": 4.2,
        "gdp_billion_eur": 450.0
      },
      ...
    ],
    "operators": [
      {
        "operator": "KPN",
        "subscribers": 2170000,
        "hbbtv_version": "2.0.1",
        "market_share_percent": 20.0
      },
      ...
    ],
    "broadcasters": [...]
  }
}
```

## Data Sections

### 1. Metadata
Export information including:
- Export date/time
- Total counts (facts, sources, references)

### 2. Countries
Complete country data with:
- **Attributes**: All country attributes (population, TV homes, GDP, etc.)
- **Sources**: Source tracking for each attribute
- **References**: External citations
- **Facts**: Full fact records

**Example:**
```json
"Austria": {
  "attributes": {
    "population_million": {
      "value": 8.97,
      "sources": [{"source_name": "Austria demographics", ...}]
    }
  }
}
```

### 3. Operators
Complete operator data with:
- **Attributes**: Subscribers, HbbTV version, CI+ version, CA systems, market share, etc.
- **Sources**: Source tracking
- **References**: Technical specification URLs
- **Facts**: Full fact records

**Example:**
```json
"KPN": {
  "attributes": {
    "subscribers": {"value": 2170000},
    "hbbtv_version": {"value": "2.0.1"},
    "market_share_percent": {"value": 20.0}
  }
}
```

### 4. Broadcasters
Public Service Broadcasters (PSBs) and commercial broadcasters:
- **Attributes**: Type (PSB), OTT apps, etc.
- **Sources**: Source tracking

### 5. Sources
All source information:
- Source type (file, URL, API, etc.)
- Source path/URL
- Source date
- Metadata

### 6. Statistics
Summary statistics for quick reference:
- Country statistics
- Operator statistics
- Broadcaster statistics
- Data quality metrics

### 7. Flattened View
Simplified structure for easy visualization:
- **Countries**: Array of country objects with direct attribute values
- **Operators**: Array of operator objects with direct attribute values
- **Broadcasters**: Array of broadcaster objects with direct attribute values

**Use this section for:**
- Charts and graphs
- Data tables
- Quick lookups
- Visualization libraries (D3.js, Chart.js, etc.)

## Usage Examples

### For Visualization Libraries

```javascript
// Load the master JSON
const data = await fetch('master_data.json').then(r => r.json());

// Use flattened view for charts
const countries = data.flattened.countries;
const operators = data.flattened.operators;

// Create a population chart
const populationData = countries.map(c => ({
  country: c.country,
  population: c.population_million
}));

// Create operator subscriber chart
const subscriberData = operators
  .filter(o => o.subscribers)
  .map(o => ({
    operator: o.operator,
    subscribers: o.subscribers
  }));
```

### For Data Analysis

```python
import json

with open('master_data.json') as f:
    data = json.load(f)

# Access country data
austria = data['countries']['Austria']
population = austria['attributes']['population_million']['value']

# Access operator data with sources
kpn = data['operators']['KPN']
subscribers = kpn['attributes']['subscribers']['value']
sources = kpn['attributes']['subscribers']['sources']

# Use flattened view for analysis
countries_df = pd.DataFrame(data['flattened']['countries'])
operators_df = pd.DataFrame(data['flattened']['operators'])
```

## Data Completeness

### Countries (46 total)
- ✅ Population: 46/46 (100%)
- ✅ TV homes: 46/46 (100%)
- ✅ GDP: 39/46 (85%)

### Operators (79 total)
- ✅ Subscribers: 51/79 (65%)
- ✅ HbbTV version: 17/79 (22%)
- ✅ CI+ version: 29/79 (37%)
- ✅ CA systems: 12/79 (15%)
- ✅ Market share: 36/79 (46%)

### Broadcasters (86 total)
- ✅ PSBs: 86/86 (100%)

## Source Tracking

Every fact includes:
- **Sources**: Where the data came from (file paths, URLs)
- **Source dates**: When data was collected
- **Confidence scores**: Data quality indicators
- **Extraction methods**: How data was extracted
- **References**: External citations and URLs

## Updating the Master JSON

To regenerate the master JSON file:

```bash
python3 agents/research_data_engineer/export_master_json.py master_data.json
```

Or use the CLI:

```bash
python3 -m agents.research_data_engineer.cli export --output master_data.json
```

## Visualization Recommendations

### Use Flattened View For:
- ✅ Bar charts (country populations, operator subscribers)
- ✅ Pie charts (market share distribution)
- ✅ Scatter plots (GDP vs TV homes)
- ✅ Tables and data grids
- ✅ Quick lookups

### Use Full Structure For:
- ✅ Source attribution displays
- ✅ Data quality indicators
- ✅ Historical tracking
- ✅ Detailed fact exploration
- ✅ Reference links

## File Size Optimization

The file is ~780KB. If you need a smaller version:

1. **Remove sources/references** for visualization-only use
2. **Use flattened view only** (much smaller)
3. **Filter by country/operator** subsets
4. **Compress** (gzip) for web delivery

---

**Created:** 2024-12-15  
**Database:** research_data.db  
**Total Facts:** 490
