#!/usr/bin/env python3
"""
Generate a focused visualization for Austria.
Shows operators, demographics, market data, and relationships.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def connect_db():
    """Connect to the database"""
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(str(db_path))

def get_austria_operators(conn):
    """Get all operators in Austria"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            o.aliases,
            oc.operator_name_in_country,
            o.operator_id
        FROM operators o
        JOIN operator_countries oc ON o.operator_id = oc.operator_id
        JOIN countries c ON oc.country_id = c.country_id
        WHERE c.country_name = 'Austria'
        ORDER BY o.canonical_name
    """)
    return cursor.fetchall()

def get_austria_facts(conn):
    """Get all facts about Austria"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            f.fact_type,
            f.value_json,
            f.unit,
            f.observed_at,
            f.confidence
        FROM facts f
        JOIN entities e ON f.entity_id = e.entity_id
        WHERE e.entity_type = 'country' AND e.canonical_name = 'Austria'
        ORDER BY f.fact_type
    """)
    return cursor.fetchall()

def get_austria_operator_relationships(conn):
    """Get operator relationships for Austria"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            COUNT(DISTINCT oc2.country_id) as other_countries
        FROM operators o
        JOIN operator_countries oc ON o.operator_id = oc.operator_id
        JOIN countries c ON oc.country_id = c.country_id
        LEFT JOIN operator_countries oc2 ON o.operator_id = oc2.operator_id
        WHERE c.country_name = 'Austria'
        GROUP BY o.operator_id, o.canonical_name
        ORDER BY other_countries DESC, o.canonical_name
    """)
    return cursor.fetchall()

def generate_austria_html(operators, facts, relationships):
    """Generate HTML visualization for Austria"""
    
    # Prepare data
    operators_json = json.dumps([
        {
            "name": op[0],
            "aliases": json.loads(op[1]) if op[1] else [],
            "name_in_austria": op[2] if op[2] else op[0]
        }
        for op in operators
    ])
    
    facts_json = json.dumps([
        {
            "type": f[0],
            "value": float(f[1]) if f[1] else None,
            "unit": f[2],
            "observed_at": f[3],
            "confidence": f[4]
        }
        for f in facts
    ])
    
    relationships_json = json.dumps([
        {
            "operator": rel[0],
            "other_countries": rel[1]
        }
        for rel in relationships
    ])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Austria - Broadcast Industry Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }}
        
        h1 {{
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .flag {{
            font-size: 4em;
            margin: 20px 0;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .stat-unit {{
            font-size: 0.8em;
            color: #999;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 2em;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 20px 0;
        }}
        
        .operators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .operator-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .operator-card h3 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .operator-card .alias {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }}
        
        .facts-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .facts-table th,
        .facts-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .facts-table th {{
            background: #f5f5f5;
            font-weight: 600;
            color: #667eea;
        }}
        
        .facts-table tr:hover {{
            background: #f9f9f9;
        }}
        
        .value-cell {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        
        .multi-country-badge {{
            display: inline-block;
            background: #4caf50;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: white;
            text-decoration: none;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            transition: background 0.3s;
        }}
        
        .back-link:hover {{
            background: rgba(255,255,255,0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="database_visualization.html" class="back-link">← Back to Full Dashboard</a>
        
        <header>
            <div class="flag">🇦🇹</div>
            <h1>Austria</h1>
            <p class="subtitle">Broadcast Industry Market Analysis</p>
        </header>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be populated by JavaScript -->
        </div>
        
        <div class="section">
            <h2>📊 Market Demographics</h2>
            <div class="chart-container">
                <canvas id="demographicsChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>📺 Operators in Austria</h2>
            <p>Austria has {len(operators)} broadcast operators serving the market.</p>
            <div class="operators-grid" id="operatorsGrid">
                <!-- Operators will be populated by JavaScript -->
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Market Facts & Data</h2>
            <table class="facts-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                        <th>Unit</th>
                        <th>Observed</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody id="factsTableBody">
                    <!-- Facts will be populated by JavaScript -->
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🌍 Operator Geographic Reach</h2>
            <p>Some operators in Austria also operate in other countries.</p>
            <div class="chart-container">
                <canvas id="reachChart"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        const operatorsData = {operators_json};
        const factsData = {facts_json};
        const relationshipsData = {relationships_json};
        
        // Populate stats
        const statsGrid = document.getElementById('statsGrid');
        const population = factsData.find(f => f.type === 'population');
        const tvHouseholds = factsData.find(f => f.type === 'tv_households');
        const broadband = factsData.find(f => f.type === 'broadband_penetration');
        const smartTV = factsData.find(f => f.type === 'smart_tv_penetration');
        
        if (population) {{
            statsGrid.innerHTML += `
                <div class="stat-card">
                    <div class="stat-value">${{population.value}}</div>
                    <div class="stat-label">Population</div>
                    <div class="stat-unit">million</div>
                </div>
            `;
        }}
        
        if (tvHouseholds) {{
            statsGrid.innerHTML += `
                <div class="stat-card">
                    <div class="stat-value">${{tvHouseholds.value}}</div>
                    <div class="stat-label">TV Households</div>
                    <div class="stat-unit">million</div>
                </div>
            `;
        }}
        
        if (broadband) {{
            statsGrid.innerHTML += `
                <div class="stat-card">
                    <div class="stat-value">${{broadband.value}}%</div>
                    <div class="stat-label">Broadband Penetration</div>
                </div>
            `;
        }}
        
        if (smartTV) {{
            statsGrid.innerHTML += `
                <div class="stat-card">
                    <div class="stat-value">${{smartTV.value}}%</div>
                    <div class="stat-label">Smart TV Penetration</div>
                </div>
            `;
        }}
        
        // Populate operators
        const operatorsGrid = document.getElementById('operatorsGrid');
        operatorsData.forEach(op => {{
            const isMultiCountry = relationshipsData.find(r => r.operator === op.name && r.other_countries > 0);
            operatorsGrid.innerHTML += `
                <div class="operator-card">
                    <h3>${{op.name_in_austria}}</h3>
                    ${{op.aliases.length > 0 ? `<div class="alias">Also known as: ${{op.aliases.join(', ')}}</div>` : ''}}
                    ${{isMultiCountry ? `<span class="multi-country-badge">Operates in ${{isMultiCountry.other_countries + 1}} countries</span>` : ''}}
                </div>
            `;
        }});
        
        // Populate facts table
        const factsTableBody = document.getElementById('factsTableBody');
        factsData.forEach(fact => {{
            const value = fact.value !== null ? fact.value.toLocaleString() : 'N/A';
            const unit = fact.unit || '';
            factsTableBody.innerHTML += `
                <tr>
                    <td><strong>${{fact.type.replace('_', ' ').replace(/\\b\\w/g, l => l.toUpperCase())}}</strong></td>
                    <td class="value-cell">${{value}} ${{unit}}</td>
                    <td>${{unit}}</td>
                    <td>${{fact.observed_at || 'N/A'}}</td>
                    <td>${{fact.confidence || 'N/A'}}</td>
                </tr>
            `;
        }});
        
        // Demographics Chart
        const demoCtx = document.getElementById('demographicsChart').getContext('2d');
        const demoData = {{
            labels: factsData.filter(f => ['population', 'tv_households', 'paytv_households'].includes(f.type)).map(f => 
                f.type.replace('_', ' ').replace(/\\b\\w/g, l => l.toUpperCase())
            ),
            datasets: [{{
                label: 'Value (millions)',
                data: factsData.filter(f => ['population', 'tv_households', 'paytv_households'].includes(f.type)).map(f => f.value),
                backgroundColor: [
                    'rgba(102, 126, 234, 0.6)',
                    'rgba(118, 75, 162, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 2
            }}]
        }};
        
        new Chart(demoCtx, {{
            type: 'bar',
            data: demoData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{ display: true, text: 'Key Market Metrics' }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Value (millions)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Operator Reach Chart
        const reachCtx = document.getElementById('reachChart').getContext('2d');
        const multiCountryOps = relationshipsData.filter(r => r.other_countries > 0);
        const singleCountryOps = relationshipsData.filter(r => r.other_countries === 0);
        
        new Chart(reachCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Multi-Country Operators', 'Austria-Only Operators'],
                datasets: [{{
                    data: [multiCountryOps.length, singleCountryOps.length],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.6)',
                        'rgba(200, 200, 200, 0.6)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(200, 200, 200, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'right' }},
                    title: {{ display: true, text: 'Operator Geographic Reach' }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    conn = connect_db()
    if not conn:
        return
    
    print("Generating Austria visualization...")
    
    operators = get_austria_operators(conn)
    facts = get_austria_facts(conn)
    relationships = get_austria_operator_relationships(conn)
    
    print(f"Found {len(operators)} operators, {len(facts)} facts")
    
    html = generate_austria_html(operators, facts, relationships)
    
    output_path = Path(__file__).parent.parent / "austria_visualization.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Austria visualization generated: {output_path}")
    print(f"Open in browser: http://localhost:8000/austria_visualization.html")
    
    conn.close()

if __name__ == "__main__":
    main()
