# Research Data Engineer Agent

A senior research data engineer agent that extracts, cleans, validates, and stores facts with comprehensive source tracking, external data enrichment, and citation management.

## Features

- **Structured Database**: SQLite database with proper schema for facts, sources, references, and external data
- **Data Extraction**: Extract facts from Markdown and JSON files
- **Data Cleaning**: Automatic cleaning and normalization of data values
- **Source Tracking**: Every fact is linked to its source(s) with confidence scores
- **External Data Enrichment**: Fetch and link external data points from web research
- **Citation Management**: Track references and URLs for all facts
- **Trend Analysis**: Historical data tracking for trend analysis
- **Data Quality Metrics**: Completeness, accuracy, and freshness scores
- **Dashboard Generation**: Generate responsive dashboard data from the database

## Installation

```bash
# Install dependencies
pip install requests pyyaml
```

## Usage

### Command Line Interface

```bash
# Extract facts from files
python -m agents.research_data_engineer.cli extract Europe/Austria/demographics.md

# Extract from multiple files
python -m agents.research_data_engineer.cli extract \
  Europe/Austria/ORF/specifications.md \
  dashboard_data.json

# Query facts
python -m agents.research_data_engineer.cli query \
  --entity-type country \
  --entity-id Austria

# Enrich facts with external data
python -m agents.research_data_engineer.cli enrich \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million

# Validate facts
python -m agents.research_data_engineer.cli validate \
  --entity-type operator \
  --entity-id ORF

# Generate dashboard
python -m agents.research_data_engineer.cli dashboard \
  --output dashboard_data.json \
  --format json

# Analyze trends
python -m agents.research_data_engineer.cli trend \
  --entity-type country \
  --entity-id Austria \
  --attribute population_million

# Show statistics
python -m agents.research_data_engineer.cli stats
```

### Python API

```python
from agents.research_data_engineer import ResearchDataEngineer

# Initialize agent
agent = ResearchDataEngineer(db_path='research_data.db')

# Extract facts from a file
facts = agent.extract_facts_from_markdown('Europe/Austria/demographics.md')

# Extract from JSON
facts = agent.extract_facts_from_json('dashboard_data.json')

# Enrich with external data
agent.enrich_with_external_data(
    entity_type='country',
    entity_id='Austria',
    attribute='population_million',
    search_queries=['Austria population 2024']
)

# Query facts
facts = agent.db.get_facts(
    entity_type='country',
    entity_id='Austria'
)

# Generate dashboard
dashboard = agent.generate_dashboard_data()

# Analyze trends
trend = agent.get_trend_analysis(
    entity_type='country',
    entity_id='Austria',
    attribute='population_million'
)
```

## Database Schema

### Facts Table
Stores core data points with entity type, ID, attribute, and value.

### Sources Table
Tracks where data came from (files, URLs, APIs, etc.).

### Fact-Sources Table
Links facts to their sources with confidence scores.

### References Table
External citations and links for facts.

### External Data Table
Data points fetched from external sources (web searches, APIs, etc.).

### Data Quality Table
Quality metrics for facts (completeness, accuracy, freshness).

## Data Source Tracking

Every fact includes:
- **Source**: Where it came from (file path, URL, etc.)
- **Source Date**: When the source was accessed/created
- **Confidence Score**: 0.0 to 1.0 indicating data quality
- **Extraction Method**: How the fact was extracted
- **References**: External citations and links
- **External Data**: Related data from web research

## Trend Analysis

The agent tracks historical changes to data points, enabling:
- Trend direction (increasing, decreasing, stable)
- First and last recorded values
- Data point count over time
- Temporal analysis for decision-making

## Data Quality

Each fact is scored on:
- **Completeness**: How complete the data is (based on sources, references, external data)
- **Accuracy**: Confidence in the data accuracy (based on source quality)
- **Freshness**: How recent the data is (based on source dates)

## Web Research Integration

The agent can fetch external data from:
- Web searches (requires API integration)
- Wikipedia summaries
- URL validation and content fetching
- Data freshness checking

**Note**: Web search functionality requires API keys. See `web_researcher.py` for integration details.

## Dashboard Generation

Generate structured dashboard data that can be used with:
- The existing `dashboard.html` file
- Custom visualization tools
- API endpoints
- Reporting systems

## Architecture

```
agents/research_data_engineer/
├── __init__.py          # Package initialization
├── agent.py             # Main agent class
├── database.py          # Database schema and management
├── data_cleaner.py      # Data cleaning utilities
├── web_researcher.py    # Web research capabilities
├── cli.py               # Command-line interface
└── README.md            # This file
```

## Future Enhancements

- [ ] Integration with search APIs (Google, Bing, DuckDuckGo)
- [ ] Machine learning for data quality scoring
- [ ] Automated fact verification
- [ ] Real-time data updates
- [ ] Advanced trend analysis with forecasting
- [ ] Multi-language support
- [ ] Data export to various formats (CSV, Excel, etc.)
