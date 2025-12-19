#!/usr/bin/env python3
"""
Generate interactive visualization for subscription data.
Shows subscriptions over time, by operator, by country.
"""

import sqlite3
import json
from pathlib import Path
from collections import defaultdict

def connect_db():
    """Connect to the database"""
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(str(db_path))

def get_subscriptions_data(conn):
    """Get all subscription data"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.operator_name,
            s.country_name,
            s.subscription_value,
            s.year,
            s.source_text,
            s.metric_type,
            s.confidence,
            s.file_path
        FROM subscriptions s
        WHERE s.year IS NOT NULL
        ORDER BY s.year DESC, s.country_name, s.operator_name
    """)
    return cursor.fetchall()

def get_subscriptions_by_operator(conn):
    """Get subscriptions grouped by operator"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.operator_name,
            s.country_name,
            s.subscription_value,
            s.year,
            s.source_text
        FROM subscriptions s
        WHERE s.year IS NOT NULL
        ORDER BY s.operator_name, s.year DESC
    """)
    return cursor.fetchall()

def get_subscriptions_by_country(conn):
    """Get subscriptions grouped by country"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.country_name,
            s.operator_name,
            s.subscription_value,
            s.year,
            s.source_text
        FROM subscriptions s
        WHERE s.year IS NOT NULL
        ORDER BY s.country_name, s.year DESC
    """)
    return cursor.fetchall()

def generate_html_visualization(conn):
    """Generate interactive HTML visualization"""
    
    all_data = get_subscriptions_data(conn)
    by_operator = get_subscriptions_by_operator(conn)
    by_country = get_subscriptions_by_country(conn)
    
    # Prepare data for JavaScript
    subscriptions_json = json.dumps([
        {
            "operator": row[0],
            "country": row[1],
            "value": row[2],
            "year": row[3],
            "source": row[4],
            "metric_type": row[5] or "total",
            "confidence": row[6]
        }
        for row in all_data
    ])
    
    # Group by operator for time series
    operator_timeseries = defaultdict(list)
    for row in by_operator:
        operator_timeseries[row[0]].append({
            "year": row[3],
            "value": row[2],
            "country": row[1],
            "source": row[4]
        })
    
    # Group by country for time series
    country_timeseries = defaultdict(list)
    for row in by_country:
        country_timeseries[row[0]].append({
            "year": row[3],
            "value": row[2],
            "operator": row[1],
            "source": row[4]
        })
    
    # Get unique operators and countries
    operators = sorted(set(row[0] for row in all_data))
    countries = sorted(set(row[1] for row in all_data))
    years = sorted(set(row[3] for row in all_data if row[3]))
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subscription Data - Fact Checked</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 20px 0;
        }}
        
        .controls {{
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        select, input {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #f5f5f5;
            font-weight: 600;
            color: #667eea;
            position: sticky;
            top: 0;
        }}
        
        tr:hover {{
            background: #f9f9f9;
        }}
        
        .value {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .source {{
            font-size: 0.9em;
            color: #666;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .confidence-high {{
            color: #4caf50;
        }}
        
        .confidence-medium {{
            color: #ff9800;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: white;
            text-decoration: none;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
        }}
        
        .back-link:hover {{
            background: rgba(255,255,255,0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="database_visualization.html" class="back-link">← Back to Main Dashboard</a>
        
        <header>
            <h1>📊 Subscription Data</h1>
            <p class="subtitle">Fact-Checked Subscriber Numbers with Sources and Years</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="totalRecords">{len(all_data)}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(operators)}</div>
                <div class="stat-label">Operators</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(countries)}</div>
                <div class="stat-label">Countries</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{years[0] if years else 'N/A'} - {years[-1] if years else 'N/A'}</div>
                <div class="stat-label">Year Range</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Subscriptions Over Time</h2>
            <div class="controls">
                <select id="operatorFilter">
                    <option value="">All Operators</option>
                    {''.join(f'<option value="{op}">{op}</option>' for op in operators)}
                </select>
                <select id="countryFilter">
                    <option value="">All Countries</option>
                    {''.join(f'<option value="{country}">{country}</option>' for country in countries)}
                </select>
            </div>
            <div class="chart-container">
                <canvas id="timeSeriesChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 All Subscription Records</h2>
            <p>Only includes data with clear sources and years. Sorted by year (most recent first).</p>
            <div style="overflow-x: auto; max-height: 600px;">
                <table id="subscriptionsTable">
                    <thead>
                        <tr>
                            <th>Year</th>
                            <th>Operator</th>
                            <th>Country</th>
                            <th>Subscriptions</th>
                            <th>Metric Type</th>
                            <th>Source</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        const subscriptionsData = {subscriptions_json};
        const operatorTimeseries = {json.dumps(dict(operator_timeseries))};
        const countryTimeseries = {json.dumps(dict(country_timeseries))};
        
        // Format value
        function formatValue(value) {{
            if (value >= 1000000) {{
                return (value / 1000000).toFixed(2) + 'M';
            }} else if (value >= 1000) {{
                return (value / 1000).toFixed(1) + 'K';
            }}
            return value.toFixed(0);
        }}
        
        // Populate table
        const tableBody = document.getElementById('tableBody');
        subscriptionsData.forEach(sub => {{
            const row = tableBody.insertRow();
            row.insertCell(0).textContent = sub.year || 'N/A';
            row.insertCell(1).textContent = sub.operator;
            row.insertCell(2).textContent = sub.country;
            const valueCell = row.insertCell(3);
            valueCell.textContent = formatValue(sub.value);
            valueCell.className = 'value';
            row.insertCell(4).textContent = sub.metric_type;
            const sourceCell = row.insertCell(5);
            sourceCell.textContent = sub.source;
            sourceCell.className = 'source';
            const confCell = row.insertCell(6);
            confCell.textContent = sub.confidence;
            confCell.className = 'confidence-' + sub.confidence;
        }});
        
        // Time series chart
        const ctx = document.getElementById('timeSeriesChart').getContext('2d');
        let timeSeriesChart = null;
        
        function updateChart() {{
            const operatorFilter = document.getElementById('operatorFilter').value;
            const countryFilter = document.getElementById('countryFilter').value;
            
            const filtered = subscriptionsData.filter(sub => {{
                return (!operatorFilter || sub.operator === operatorFilter) &&
                       (!countryFilter || sub.country === countryFilter);
            }});
            
            // Group by year
            const byYear = {{}};
            filtered.forEach(sub => {{
                if (!byYear[sub.year]) {{
                    byYear[sub.year] = [];
                }}
                byYear[sub.year].push(sub.value);
            }});
            
            const years = Object.keys(byYear).sort();
            const datasets = [];
            
            if (operatorFilter) {{
                // Show single operator over time
                const operatorData = operatorTimeseries[operatorFilter] || [];
                const data = years.map(year => {{
                    const entry = operatorData.find(e => e.year == year);
                    return entry ? entry.value : null;
                }});
                
                datasets.push({{
                    label: operatorFilter,
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }});
            }} else {{
                // Show aggregated by year
                const data = years.map(year => {{
                    const values = byYear[year];
                    return values.reduce((a, b) => a + b, 0);
                }});
                
                datasets.push({{
                    label: 'Total Subscriptions',
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }});
            }}
            
            if (timeSeriesChart) {{
                timeSeriesChart.destroy();
            }}
            
            timeSeriesChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: years,
                    datasets: datasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: true }},
                        title: {{ display: true, text: 'Subscriptions Over Time' }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return formatValue(value);
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        document.getElementById('operatorFilter').addEventListener('change', updateChart);
        document.getElementById('countryFilter').addEventListener('change', updateChart);
        
        // Initial chart
        updateChart();
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    conn = connect_db()
    if not conn:
        return
    
    print("Generating subscription visualization...")
    html = generate_html_visualization(conn)
    
    output_path = Path(__file__).parent.parent / "subscriptions_visualization.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Visualization generated: {output_path}")
    print(f"Open in browser: http://localhost:8000/subscriptions_visualization.html")
    
    conn.close()

if __name__ == "__main__":
    main()
