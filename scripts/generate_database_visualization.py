#!/usr/bin/env python3
"""
Generate visualizations of the database contents.
Creates HTML dashboard with interactive charts and network graphs.
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

def get_countries_by_region(conn):
    """Get countries grouped by region"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region, COUNT(*) as total, SUM(has_data) as with_data
        FROM countries
        GROUP BY region
        ORDER BY region
    """)
    return cursor.fetchall()

def get_operators_by_country(conn):
    """Get operators with their countries"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            o.aliases,
            COUNT(oc.country_id) as country_count,
            GROUP_CONCAT(c.country_name, '|') as countries,
            GROUP_CONCAT(oc.operator_name_in_country, '|') as country_names
        FROM operators o
        LEFT JOIN operator_countries oc ON o.operator_id = oc.operator_id
        LEFT JOIN countries c ON oc.country_id = c.country_id
        GROUP BY o.operator_id, o.canonical_name, o.aliases
        ORDER BY country_count DESC, o.canonical_name
    """)
    return cursor.fetchall()

def get_countries_with_operators(conn):
    """Get countries with their operators"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.country_name,
            c.region,
            c.iso_code,
            COUNT(oc.operator_id) as operator_count,
            GROUP_CONCAT(o.canonical_name, '|') as operators,
            GROUP_CONCAT(oc.operator_name_in_country, '|') as operator_names
        FROM countries c
        LEFT JOIN operator_countries oc ON c.country_id = oc.country_id
        LEFT JOIN operators o ON oc.operator_id = o.operator_id
        WHERE c.region = 'Europe'
        GROUP BY c.country_id, c.country_name, c.region, c.iso_code
        ORDER BY operator_count DESC, c.country_name
    """)
    return cursor.fetchall()

def get_facts_summary(conn):
    """Get facts summary by type"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            fact_type,
            COUNT(*) as count,
            COUNT(DISTINCT entity_id) as entities
        FROM facts
        GROUP BY fact_type
        ORDER BY count DESC
    """)
    return cursor.fetchall()

def get_country_facts(conn, country_name):
    """Get facts for a specific country"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            f.fact_type,
            f.value_json,
            f.unit,
            f.observed_at
        FROM facts f
        JOIN entities e ON f.entity_id = e.entity_id
        WHERE e.entity_type = 'country' AND e.canonical_name = ?
        ORDER BY f.fact_type
    """, (country_name,))
    return cursor.fetchall()

def generate_network_data(conn):
    """Generate network graph data for operator-country relationships"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            c.country_name,
            c.region,
            oc.operator_name_in_country
        FROM operators o
        JOIN operator_countries oc ON o.operator_id = oc.operator_id
        JOIN countries c ON oc.country_id = c.country_id
        WHERE c.region = 'Europe'
        ORDER BY o.canonical_name, c.country_name
    """)
    
    nodes = []
    links = []
    node_set = set()
    
    # Add operator nodes
    operators = set()
    countries = set()
    
    for row in cursor.fetchall():
        operator, country, region, op_name_in_country = row
        operators.add(operator)
        countries.add(country)
        
        # Add operator node
        if operator not in node_set:
            nodes.append({
                "id": operator,
                "name": operator,
                "type": "operator",
                "group": "operator"
            })
            node_set.add(operator)
        
        # Add country node
        if country not in node_set:
            nodes.append({
                "id": country,
                "name": country,
                "type": "country",
                "group": region
            })
            node_set.add(country)
        
        # Add link
        links.append({
            "source": operator,
            "target": country,
            "value": 1,
            "label": op_name_in_country if op_name_in_country else operator
        })
    
    return {"nodes": nodes, "links": links}

def generate_html_dashboard(conn):
    """Generate interactive HTML dashboard"""
    
    # Get data
    regions_data = get_countries_by_region(conn)
    operators_data = get_operators_by_country(conn)
    countries_data = get_countries_with_operators(conn)
    facts_data = get_facts_summary(conn)
    network_data = generate_network_data(conn)
    
    # Prepare data for JavaScript
    regions_json = json.dumps([{"region": r[0], "total": r[1], "with_data": r[2] or 0} 
                               for r in regions_data])
    
    operators_json = json.dumps([
        {
            "name": op[0],
            "aliases": json.loads(op[1]) if op[1] else [],
            "country_count": op[2],
            "countries": op[3].split("|") if op[3] else [],
            "country_names": op[4].split("|") if op[4] else []
        }
        for op in operators_data
    ])
    
    countries_json = json.dumps([
        {
            "name": c[0],
            "region": c[1],
            "iso_code": c[2],
            "operator_count": c[3] or 0,
            "operators": c[4].split("|") if c[4] else [],
            "operator_names": c[5].split("|") if c[5] else []
        }
        for c in countries_data
    ])
    
    facts_json = json.dumps([{"type": f[0], "count": f[1], "entities": f[2]} 
                            for f in facts_data])
    
    network_json = json.dumps(network_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Broadcast Industry Database - Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
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
            max-width: 1400px;
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
        
        .stats-grid {{
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
        
        .network-container {{
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
            position: relative;
            overflow: hidden;
        }}
        
        .zoom-controls {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 100;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .zoom-btn {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .zoom-btn:hover {{
            background: #f5f5f5;
        }}
        
        .zoom-info {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(255,255,255,0.9);
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .controls {{
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        .btn:hover {{
            background: #5568d3;
        }}
        
        .table-container {{
            overflow-x: auto;
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
        }}
        
        tr:hover {{
            background: #f9f9f9;
        }}
        
        .operator-tag {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9em;
        }}
        
        .country-tag {{
            display: inline-block;
            background: #f3e5f5;
            color: #7b1fa2;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9em;
        }}
        
        .node {{
            cursor: pointer;
        }}
        
        .node circle {{
            stroke: #fff;
            stroke-width: 2px;
        }}
        
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
            stroke-width: 1.5px;
        }}
        
        .link:hover {{
            stroke-opacity: 1;
            stroke-width: 2px;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px;
            border-radius: 5px;
            pointer-events: none;
            font-size: 12px;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📺 Broadcast Industry Database</h1>
            <p class="subtitle">Visualization & Relationship Explorer</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="stat-countries">196</div>
                <div class="stat-label">Countries</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-operators">55</div>
                <div class="stat-label">Operators</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-relationships">70</div>
                <div class="stat-label">Relationships</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-facts">318</div>
                <div class="stat-label">Facts</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🌍 Countries by Region</h2>
            <div class="chart-container">
                <canvas id="regionsChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 Operator-Country Network</h2>
            <p>Interactive network graph showing relationships between operators and countries. 
            <strong>Zoom:</strong> Mouse wheel or pinch gesture. <strong>Pan:</strong> Click and drag background. <strong>Move nodes:</strong> Click and drag nodes.</p>
            <div class="network-container" id="network">
                <div class="zoom-controls">
                    <button class="zoom-btn" id="zoomIn">+</button>
                    <button class="zoom-btn" id="zoomOut">−</button>
                    <button class="zoom-btn" id="resetZoom">⌂</button>
                </div>
                <div class="zoom-info" id="zoomInfo">Zoom: 100%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Top Operators by Country Coverage</h2>
            <div class="chart-container">
                <canvas id="operatorsChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>🏢 Top Countries by Operator Count</h2>
            <div class="chart-container">
                <canvas id="countriesChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Facts Summary</h2>
            <div class="chart-container">
                <canvas id="factsChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Multi-Country Operators</h2>
            <div class="table-container">
                <table id="multiCountryTable">
                    <thead>
                        <tr>
                            <th>Operator</th>
                            <th>Countries</th>
                            <th>Country Names</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
        
        <div class="section">
            <h2>🗺️ Countries with Operators</h2>
            <div class="controls">
                <input type="text" id="countrySearch" placeholder="Search countries..." style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; flex: 1;">
            </div>
            <div class="table-container">
                <table id="countriesTable">
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Region</th>
                            <th>Operators</th>
                            <th>Operator Names</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        // Data from Python
        const regionsData = {regions_json};
        const operatorsData = {operators_json};
        const countriesData = {countries_json};
        const factsData = {facts_json};
        const networkData = {network_json};
        
        // Update stats
        document.getElementById('stat-countries').textContent = regionsData.reduce((sum, r) => sum + r.total, 0);
        document.getElementById('stat-operators').textContent = operatorsData.length;
        document.getElementById('stat-relationships').textContent = networkData.links.length;
        document.getElementById('stat-facts').textContent = factsData.reduce((sum, f) => sum + f.count, 0);
        
        // Regions Chart
        const regionsCtx = document.getElementById('regionsChart').getContext('2d');
        new Chart(regionsCtx, {{
            type: 'bar',
            data: {{
                labels: regionsData.map(r => r.region),
                datasets: [{{
                    label: 'Total Countries',
                    data: regionsData.map(r => r.total),
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}, {{
                    label: 'With Data',
                    data: regionsData.map(r => r.with_data),
                    backgroundColor: 'rgba(118, 75, 162, 0.6)',
                    borderColor: 'rgba(118, 75, 162, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top' }},
                    title: {{ display: true, text: 'Countries by Region' }}
                }}
            }}
        }});
        
        // Top Operators Chart
        const topOperators = operatorsData
            .filter(op => op.country_count > 0)
            .sort((a, b) => b.country_count - a.country_count)
            .slice(0, 10);
        
        const operatorsCtx = document.getElementById('operatorsChart').getContext('2d');
        new Chart(operatorsCtx, {{
            type: 'bar',
            indexAxis: 'y',
            data: {{
                labels: topOperators.map(op => op.name),
                datasets: [{{
                    label: 'Number of Countries',
                    data: topOperators.map(op => op.country_count),
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{ display: true, text: 'Top 10 Operators by Country Coverage' }}
                }}
            }}
        }});
        
        // Top Countries Chart
        const topCountries = countriesData
            .filter(c => c.operator_count > 0)
            .sort((a, b) => b.operator_count - a.operator_count)
            .slice(0, 10);
        
        const countriesCtx = document.getElementById('countriesChart').getContext('2d');
        new Chart(countriesCtx, {{
            type: 'bar',
            indexAxis: 'y',
            data: {{
                labels: topCountries.map(c => c.name),
                datasets: [{{
                    label: 'Number of Operators',
                    data: topCountries.map(c => c.operator_count),
                    backgroundColor: 'rgba(118, 75, 162, 0.6)',
                    borderColor: 'rgba(118, 75, 162, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{ display: true, text: 'Top 10 Countries by Operator Count' }}
                }}
            }}
        }});
        
        // Facts Chart
        const factsCtx = document.getElementById('factsChart').getContext('2d');
        new Chart(factsCtx, {{
            type: 'doughnut',
            data: {{
                labels: factsData.map(f => f.type),
                datasets: [{{
                    data: factsData.map(f => f.count),
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.6)',
                        'rgba(118, 75, 162, 0.6)',
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'right' }},
                    title: {{ display: true, text: 'Facts by Type' }}
                }}
            }}
        }});
        
        // Network Graph - wait for DOM and D3 to be ready
        function initNetworkGraph() {{
            console.log('Initializing network graph...');
            
            if (typeof d3 === 'undefined') {{
                console.error('D3.js not loaded!');
                const networkContainer = document.getElementById('network');
                if (networkContainer) {{
                    networkContainer.innerHTML = '<p style="padding: 20px; color: red;">Error: D3.js library failed to load. Please check your internet connection.</p>';
                }}
                return;
            }}
            
            const networkContainer = document.getElementById('network');
            if (!networkContainer) {{
                console.error('Network container not found!');
                return;
            }}
            
            const width = networkContainer.clientWidth || 1200;
            const height = 800;
            
            console.log('Network container size:', width, 'x', height);
            
            // Clear any existing content
            networkContainer.innerHTML = '';
            
            if (!networkData || !networkData.nodes || networkData.nodes.length === 0) {{
                console.error('No network data available!', networkData);
                networkContainer.innerHTML = '<p style="padding: 20px;">No network data to display.</p>';
                return;
            }}
            
            console.log('Network data:', networkData.nodes.length, 'nodes,', networkData.links.length, 'links');
            
            const svg = d3.select('#network')
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .style('background', '#fafafa');
            
            // Create a container group for zoom/pan
            const g = svg.append('g');
            
            // Set up zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.1, 4])
                .on('zoom', function(event) {{
                    g.attr('transform', event.transform);
                    updateZoomInfo(event.transform.k);
                }});
            
            svg.call(zoom);
            
            // Initial zoom to fit all nodes
            const bounds = g.node().getBBox();
            const fullWidth = bounds.width;
            const fullHeight = bounds.height;
            const midX = bounds.x + fullWidth / 2;
            const midY = bounds.y + fullHeight / 2;
            
            // Calculate initial scale to fit
            const scale = Math.min(width / fullWidth, height / fullHeight, 1) * 0.9;
            const translate = [width / 2 - scale * midX, height / 2 - scale * midY];
            
            // Apply initial transform
            const initialTransform = d3.zoomIdentity
                .translate(translate[0], translate[1])
                .scale(scale);
            
            svg.call(zoom.transform, initialTransform);
            
            // Zoom controls
            d3.select('#zoomIn').on('click', function() {{
                svg.transition().call(zoom.scaleBy, 1.5);
            }});
            
            d3.select('#zoomOut').on('click', function() {{
                svg.transition().call(zoom.scaleBy, 1 / 1.5);
            }});
            
            d3.select('#resetZoom').on('click', function() {{
                svg.transition().call(zoom.transform, initialTransform);
            }});
            
            function updateZoomInfo(scale) {{
                d3.select('#zoomInfo').text('Zoom: ' + Math.round(scale * 100) + '%');
            }}
            
            updateZoomInfo(scale);
            
            // Convert link source/target from strings to node objects
            const nodeMap = new Map();
            networkData.nodes.forEach(node => {{
                nodeMap.set(node.id, node);
            }});
            
            networkData.links.forEach(link => {{
                link.source = nodeMap.get(link.source);
                link.target = nodeMap.get(link.target);
            }});
            
            // Create the force simulation
            const simulation = d3.forceSimulation(networkData.nodes)
                .force('link', d3.forceLink(networkData.links).id(d => d.id).distance(100))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(0, 0))
                .force('collision', d3.forceCollide().radius(30))
                .on('end', function() {{
                    // After simulation ends, fit the view
                    const bounds = g.node().getBBox();
                    const fullWidth = bounds.width;
                    const fullHeight = bounds.height;
                    const midX = bounds.x + fullWidth / 2;
                    const midY = bounds.y + fullHeight / 2;
                    
                    const scale = Math.min(width / fullWidth, height / fullHeight, 1) * 0.9;
                    const translate = [width / 2 - scale * midX, height / 2 - scale * midY];
                    
                    const fitTransform = d3.zoomIdentity
                        .translate(translate[0], translate[1])
                        .scale(scale);
                    
                    svg.transition().duration(750).call(zoom.transform, fitTransform);
                }});
            
            // Create links
            const link = g.append('g')
                .attr('class', 'links')
                .selectAll('line')
                .data(networkData.links)
                .enter().append('line')
                .attr('class', 'link')
                .attr('stroke', '#999')
                .attr('stroke-opacity', 0.6)
                .attr('stroke-width', 2);
            
            // Create nodes
            const node = g.append('g')
                .attr('class', 'nodes')
                .selectAll('circle')
                .data(networkData.nodes)
                .enter().append('circle')
                .attr('class', 'node')
                .attr('r', d => d.type === 'operator' ? 12 : 8)
                .attr('fill', d => d.type === 'operator' ? '#667eea' : '#764ba2')
                .attr('stroke', '#fff')
                .attr('stroke-width', 2)
                .call(d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended));
            
            // Create labels
            const label = g.append('g')
                .attr('class', 'labels')
                .selectAll('text')
                .data(networkData.nodes)
                .enter().append('text')
                .text(d => d.name.length > 20 ? d.name.substring(0, 20) + '...' : d.name)
                .attr('font-size', '11px')
                .attr('dx', 15)
                .attr('dy', 4)
                .attr('fill', '#333')
                .attr('pointer-events', 'none');
            
            // Create tooltip
            const tooltip = d3.select('body').append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0)
                .style('position', 'absolute')
                .style('background', 'rgba(0,0,0,0.8)')
                .style('color', 'white')
                .style('padding', '10px')
                .style('border-radius', '5px')
                .style('pointer-events', 'none')
                .style('z-index', '1000');
            
            // Node interactions
            node.on('mouseover', function(event, d) {{
                tooltip.transition().duration(200).style('opacity', 0.9);
                tooltip.html(`<strong>${{d.name}}</strong><br/>Type: ${{d.type}}<br/>Group: ${{d.group}}`)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
                d3.select(this).attr('r', d => d.type === 'operator' ? 16 : 12);
            }})
            .on('mouseout', function(event, d) {{
                tooltip.transition().duration(500).style('opacity', 0);
                d3.select(this).attr('r', d => d.type === 'operator' ? 12 : 8);
            }});
            
            // Update positions on simulation tick
            simulation.on('tick', () => {{
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                
                label
                    .attr('x', d => d.x)
                    .attr('y', d => d.y);
            }});
            
            function dragstarted(event, d) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }}
            
            function dragged(event, d) {{
                d.fx = event.x;
                d.fy = event.y;
            }}
            
            function dragended(event, d) {{
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }}
            
            console.log('Network graph initialized successfully');
        }}
        
        // Initialize network graph when page is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', function() {{
                setTimeout(initNetworkGraph, 500); // Small delay to ensure D3 is loaded
            }});
        }} else {{
            setTimeout(initNetworkGraph, 500);
        }}
        
        // Multi-country operators table
        const multiCountryOps = operatorsData.filter(op => op.country_count > 1);
        const multiTableBody = document.querySelector('#multiCountryTable tbody');
        multiCountryOps.forEach(op => {{
            const row = multiTableBody.insertRow();
            row.insertCell(0).textContent = op.name;
            row.insertCell(1).textContent = op.country_count;
            const countriesCell = row.insertCell(2);
            op.countries.forEach((country, i) => {{
                const tag = document.createElement('span');
                tag.className = 'country-tag';
                tag.textContent = country + (op.country_names[i] && op.country_names[i] !== country ? ` (as ${{op.country_names[i]}})` : '');
                countriesCell.appendChild(tag);
            }});
        }});
        
        // Countries table
        const countriesTableBody = document.querySelector('#countriesTable tbody');
        countriesData.forEach(country => {{
            const row = countriesTableBody.insertRow();
            row.insertCell(0).textContent = country.name;
            row.insertCell(1).textContent = country.region;
            row.insertCell(2).textContent = country.operator_count;
            const operatorsCell = row.insertCell(3);
            if (country.operators.length > 0) {{
                country.operators.forEach((op, i) => {{
                    const tag = document.createElement('span');
                    tag.className = 'operator-tag';
                    tag.textContent = op + (country.operator_names[i] && country.operator_names[i] !== op ? ` (${{country.operator_names[i]}})` : '');
                    operatorsCell.appendChild(tag);
                }});
            }}
        }});
        
        // Search functionality
        document.getElementById('countrySearch').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const rows = countriesTableBody.querySelectorAll('tr');
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            }});
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
    
    print("Generating HTML dashboard...")
    html = generate_html_dashboard(conn)
    
    output_path = Path(__file__).parent.parent / "database_visualization.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Dashboard generated: {output_path}")
    print(f"Open in browser: file://{output_path.absolute()}")
    
    conn.close()

if __name__ == "__main__":
    main()
