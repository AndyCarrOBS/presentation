# Database Visualization Guide

## Interactive HTML Dashboard

The main visualization is an interactive HTML dashboard that provides comprehensive views of the database relationships.

### Generate the Dashboard

```bash
python3 scripts/generate_database_visualization.py
```

This creates `database_visualization.html` in the project root.

### Open the Dashboard

Open the HTML file in your web browser:
```bash
# On Linux/Mac
xdg-open database_visualization.html
# or
open database_visualization.html  # Mac
# or just double-click the file
```

Or navigate to: `file:///path/to/database_visualization.html`

## Dashboard Features

### 1. **Statistics Overview**
- Total countries (196)
- Total operators (55)
- Total relationships (70)
- Total facts (318)

### 2. **Countries by Region Chart**
- Bar chart showing total countries vs countries with data
- Grouped by region (Europe, Asia, Africa, etc.)

### 3. **Interactive Network Graph**
- **Visual representation** of operator-country relationships
- **Nodes**: Operators (blue) and Countries (purple)
- **Links**: Relationships between operators and countries
- **Interactive**: Click and drag nodes to explore
- **Hover**: See details about each node

### 4. **Top Operators Chart**
- Horizontal bar chart showing operators by country coverage
- Shows which operators operate in the most countries

### 5. **Top Countries Chart**
- Horizontal bar chart showing countries by operator count
- Identifies markets with the most operator presence

### 6. **Facts Summary**
- Doughnut chart showing distribution of fact types
- Population, GDP, broadband penetration, etc.

### 7. **Multi-Country Operators Table**
- Lists all operators that operate in multiple countries
- Shows country names and local operator names

### 8. **Countries with Operators Table**
- Searchable table of all European countries
- Shows operator count and operator names
- Includes local operator names where they differ

## Understanding the Network Graph

### Node Types
- **Blue circles (larger)**: Operators
- **Purple circles (smaller)**: Countries

### Relationships
- **Lines**: Connect operators to countries where they operate
- **Thickness**: All relationships are equal weight
- **Layout**: Force-directed layout - related nodes cluster together

### Key Insights from the Graph
1. **M7 Group** appears as a central hub (operates in 6 countries)
2. **Allente** connects multiple Nordic countries
3. **Sky** spans Germany, Ireland, and Italy
4. **UPC** appears in multiple Central/Eastern European countries

## Using the Visualizations

### To Analyze Relationships:
1. **Start with the network graph** - see overall structure
2. **Check multi-country operators** - identify regional players
3. **Review country operator counts** - find competitive markets
4. **Examine facts** - understand market characteristics

### To Find Specific Information:
1. **Search countries** - use the search box in the countries table
2. **Hover over network nodes** - see operator/country details
3. **Click and drag nodes** - reorganize the network view
4. **Review charts** - see trends and patterns

## Alternative: Command-Line Exploration

If you prefer command-line tools:

```bash
# Show all database contents
python3 scripts/explore_database.py --all

# Interactive menu
python3 scripts/explore_database.py
```

## Data Relationships Visualized

### Operator → Country (Many-to-Many)
- One operator can operate in multiple countries
- One country can have multiple operators
- Junction table: `operator_countries`

### Country → Facts (One-to-Many)
- Each country can have multiple facts
- Facts include: population, GDP, broadband penetration, etc.
- Table: `facts` linked via `entities`

### Entity Hierarchy
- **Countries**: Geographic entities
- **Operators**: Business entities
- Both stored in `entities` table with type differentiation

## Tips for Analysis

1. **Multi-country operators** indicate regional strategies
2. **High operator count countries** are competitive markets
3. **Network clusters** show regional groupings
4. **Missing relationships** indicate research opportunities

## Updating Visualizations

After updating the database, regenerate the dashboard:
```bash
python3 scripts/generate_database_visualization.py
```

The dashboard automatically pulls the latest data from `broadcast_industry.db`.
