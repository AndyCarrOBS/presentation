# Research Data Engineer Agent - Quick Start

## What Was Built

A complete **Senior Research Data Engineer Agent** that:

1. ✅ **Extracts facts** from Markdown and JSON files
2. ✅ **Stores facts** in a structured SQLite database with full source tracking
3. ✅ **Cleans and validates** data automatically
4. ✅ **Tracks sources** with dates, confidence scores, and extraction methods
5. ✅ **Enriches data** with external web research (ready for API integration)
6. ✅ **Manages citations** and references for all facts
7. ✅ **Analyzes trends** using historical data points
8. ✅ **Generates dashboards** from the database
9. ✅ **Provides CLI** for easy interaction

## Quick Start

### 1. Install Dependencies

```bash
cd /home/andycarr/code/business-dev/presentation
pip install -r agents/research_data_engineer/requirements.txt
```

### 2. Extract Facts from Your Existing Data

```bash
# Extract from markdown files
python -m agents.research_data_engineer.cli extract \
  Europe/Austria/demographics.md \
  Europe/Austria/ORF/specifications.md

# Extract from JSON
python -m agents.research_data_engineer.cli extract dashboard_data.json
```

### 3. Query the Database

```bash
# See all facts about Austria
python -m agents.research_data_engineer.cli query \
  --entity-type country \
  --entity-id Austria

# See all operators
python -m agents.research_data_engineer.cli query \
  --entity-type operator
```

### 4. Generate Dashboard

```bash
# Generate dashboard data
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data_from_db.json \
  --format json
```

### 5. View Statistics

```bash
python -m agents.research_data_engineer.cli stats
```

## Database Structure

The agent creates a SQLite database (`research_data.db` by default) with:

- **facts**: Core data points (entity_type, entity_id, attribute, value)
- **sources**: Where data came from (files, URLs, etc.)
- **fact_sources**: Links facts to sources with confidence scores
- **references**: External citations and URLs
- **external_data**: Data from web research
- **data_quality**: Quality metrics for each fact

## Key Features

### Source Tracking
Every fact includes:
- Source file/URL
- Source date
- Confidence score (0.0-1.0)
- Extraction method

### Trend Analysis
Track changes over time:
```bash
python -m agents.research_data_engineer.cli trend \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million
```

### Data Quality
Each fact is scored on:
- **Completeness**: Based on number of sources and references
- **Accuracy**: Based on source confidence scores
- **Freshness**: Based on source dates

## Python API Example

```python
from agents.research_data_engineer import ResearchDataEngineer

# Initialize
agent = ResearchDataEngineer(db_path='research_data.db')

# Extract facts
facts = agent.extract_facts_from_markdown('Europe/Austria/demographics.md')

# Query
facts = agent.db.get_facts(entity_type='country', entity_id='Austria')

# Generate dashboard
dashboard = agent.generate_dashboard_data()

# Analyze trends
trend = agent.get_trend_analysis(
    entity_type='country',
    entity_id='Austria',
    attribute='population_million'
)
```

## Next Steps

1. **Extract all your existing data**:
   ```bash
   # Find all markdown files and extract
   find Europe -name "*.md" -type f | xargs python -m agents.research_data_engineer.cli extract
   ```

2. **Enrich with external data** (requires web search API setup):
   ```bash
   python -m agents.research_data_engineer.cli enrich \
     --entity-type country \
     --entity-id Austria \
     --attribute population_million
   ```

3. **Validate all facts**:
   ```bash
   python -m agents.research_data_engineer.cli validate
   ```

4. **Generate updated dashboard**:
   ```bash
   python -m agents.research_data_engineer.cli dashboard \
     --output dashboard_data.json \
     --format json
   ```

## Architecture

```
agents/research_data_engineer/
├── agent.py          # Main agent class
├── database.py       # Database schema & operations
├── data_cleaner.py   # Data cleaning utilities
├── web_researcher.py # Web research (ready for API integration)
├── cli.py            # Command-line interface
└── README.md         # Full documentation
```

## Integration with Existing Dashboard

The agent can generate data in the same format as your existing `dashboard_data.json`, making it a drop-in replacement:

```bash
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json
```

Then your existing `dashboard.html` will work with the new data source!
