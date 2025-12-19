# Directory Structure

This document describes the organization of the project directory.

## Root Directory

```
presentation/
├── agents/              # Research data engineer agent code
├── Europe/              # Country and operator data (markdown files)
├── Operators/           # Individual operator documentation
├── scripts/             # Utility scripts
├── img/                 # Images and logos
├── docs/                # Documentation files
├── data/                # Data files (JSON, DB, SQL, etc.)
├── visualizations/      # HTML visualization files
├── logs/                # Log files
└── research/            # Research workflow documentation
```

## Directory Details

### `/docs/`
All markdown documentation files:
- README files
- Data extraction reports
- Database summaries
- Analysis reports
- Guides and instructions

### `/data/`
All data files:
- JSON files (dashboard_data.json, master_data.json, etc.)
- Database files (.db)
- SQL files (.sql)
- CSV exports
- ZIP archives
- Text data files

### `/visualizations/`
HTML visualization files:
- Dashboard HTML files
- Visualization HTML files
- Interactive charts and graphs

### `/logs/`
Log files from workflows and scripts:
- operator_research_full.log
- Other execution logs

### `/research/`
Research workflow documentation:
- OpenAI workflow guides
- Operator research summaries
- Workflow execution guides
- Research completion reports

### `/agents/`
Research data engineer agent:
- Core agent code
- Database module
- Web researcher
- CLI interface
- Workflow scripts

### `/Europe/`
Country and operator data:
- Country demographics
- Operator specifications
- Strategy summaries
- Contact information

### `/Operators/`
Individual operator documentation:
- Operator-specific markdown files
- Operator details and specifications

### `/scripts/`
Utility scripts:
- Data extraction scripts
- Analysis scripts
- Export scripts
- Contact management scripts

### `/img/`
Images and logos:
- Operator logos
- Country maps
- Visual assets

## File Organization Rules

1. **Documentation** → `/docs/`
2. **Data Files** → `/data/`
3. **Visualizations** → `/visualizations/`
4. **Logs** → `/logs/`
5. **Research Docs** → `/research/`
6. **Code** → `/agents/` or `/scripts/`
7. **Content** → `/Europe/` or `/Operators/`
8. **Assets** → `/img/`

## Maintenance

- Keep root directory clean
- Move new files to appropriate subdirectories
- Update this document when structure changes
