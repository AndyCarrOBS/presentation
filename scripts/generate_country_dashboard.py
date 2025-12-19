#!/usr/bin/env python3
"""
Generate country dashboard prototype.
Shows: country info, top operators with subscriber data, PSBs.
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

def connect_db():
    """Connect to the database"""
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(str(db_path))

# Country flag emojis
COUNTRY_FLAGS = {
    "Austria": "🇦🇹",
    "Germany": "🇩🇪",
    "France": "🇫🇷",
    "Italy": "🇮🇹",
    "Spain": "🇪🇸",
    "United Kingdom": "🇬🇧",
    "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪",
    "Switzerland": "🇨🇭",
    "Poland": "🇵🇱",
    "Denmark": "🇩🇰",
    "Sweden": "🇸🇪",
    "Norway": "🇳🇴",
    "Finland": "🇫🇮",
    "Ireland": "🇮🇪",
    "Portugal": "🇵🇹",
    "Czech Republic": "🇨🇿",
    "Romania": "🇷🇴",
    "Hungary": "🇭🇺",
    "Greece": "🇬🇷",
}

# Operator logo mapping
OPERATOR_LOGOS = {
    "ORF": "orf-logo.svg",
    "ORF (SAT+Terrestrial)": "orf-logo.svg",
    "Magenta TV": "vodafone-logo.png",  # Placeholder
    "Deutsche Telekom Magenta TV": "vodafone-logo.png",
    "M7 Group": "canal-digital.png",
    "M7 HD Austria": "canal-digital.png",
    "HD+": "hdplus-logo.png",
    "Ziggo": "ziggo-logo.svg",
    "Vodafone": "vodafone-logo.png",
    "Vodafone Germany": "vodafone-logo.png",
    "PYUR": "pyur-logo.png",
    "Fransat": "fransat-logo.png",
    "YouSee": "yousee-logo.png",
    "Voo": "voo-logo.png",
    "Tivusat": "TivuSat-UHD.jpg",
}

def get_country_data(conn, country_name: str) -> Dict:
    """Get country demographics and facts"""
    cursor = conn.cursor()
    
    # Get country info
    cursor.execute("""
        SELECT country_id, country_name, iso_code, region
        FROM countries
        WHERE country_name = ?
    """, (country_name,))
    country_row = cursor.fetchone()
    
    if not country_row:
        return None
    
    country_id, name, iso_code, region = country_row
    
    # Get facts
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
    
    facts = {}
    for row in cursor.fetchall():
        fact_type, value, unit, observed_at = row
        facts[fact_type] = {
            'value': float(value) if value else None,
            'unit': unit,
            'observed_at': observed_at
        }
    
    return {
        'country_id': country_id,
        'country_name': name,
        'iso_code': iso_code,
        'region': region,
        'facts': facts,
        'flag': COUNTRY_FLAGS.get(name, '🏳️')
    }

def get_country_operators(conn, country_name: str) -> List[Dict]:
    """Get operators for a country with subscription data"""
    cursor = conn.cursor()
    
    # Get operators
    cursor.execute("""
        SELECT 
            o.operator_id,
            o.canonical_name,
            o.aliases,
            oc.operator_name_in_country
        FROM operators o
        JOIN operator_countries oc ON o.operator_id = oc.operator_id
        JOIN countries c ON oc.country_id = c.country_id
        WHERE c.country_name = ?
        ORDER BY o.canonical_name
    """, (country_name,))
    
    operators = []
    for row in cursor.fetchall():
        op_id, canonical_name, aliases, name_in_country = row
        
        # Get subscription data for last 3 years
        # Try multiple name variations
        name_variations = [canonical_name, name_in_country]
        if aliases:
            name_variations.extend(json.loads(aliases))
        
        subscriptions = []
        for name_var in name_variations:
            cursor.execute("""
                SELECT 
                    year,
                    subscription_value,
                    metric_type,
                    source_text
                FROM subscriptions
                WHERE (operator_name = ? OR operator_name LIKE ?) 
                  AND country_name = ? 
                  AND year IS NOT NULL
                ORDER BY year DESC
                LIMIT 3
            """, (name_var, f"%{name_var}%", country_name))
            
            for sub_row in cursor.fetchall():
                subscriptions.append({
                    'year': sub_row[0],
                    'value': sub_row[1],
                    'metric_type': sub_row[2] or 'total',
                    'source': sub_row[3]
                })
        
        # Remove duplicates and sort
        seen = set()
        unique_subs = []
        for sub in sorted(subscriptions, key=lambda x: x['year'], reverse=True):
            key = (sub['year'], sub['value'])
            if key not in seen:
                seen.add(key)
                unique_subs.append(sub)
        
        subscriptions = unique_subs[:3]
        
        subscriptions = []
        for sub_row in cursor.fetchall():
            subscriptions.append({
                'year': sub_row[0],
                'value': sub_row[1],
                'metric_type': sub_row[2] or 'total',
                'source': sub_row[3]
            })
        
        # Get revenue data if available (from operator files)
        revenue_data = get_operator_revenue(canonical_name, country_name)
        
        operators.append({
            'operator_id': op_id,
            'canonical_name': canonical_name,
            'name_in_country': name_in_country or canonical_name,
            'aliases': json.loads(aliases) if aliases else [],
            'subscriptions': subscriptions,
            'revenue': revenue_data,
            'logo': OPERATOR_LOGOS.get(canonical_name) or find_logo(canonical_name)
        })
    
    # Sort by subscription value (most recent year) or name
    operators.sort(key=lambda x: (
        -x['subscriptions'][0]['value'] if x['subscriptions'] and len(x['subscriptions']) > 0 else 0,
        x['canonical_name']
    ))
    
    return operators[:10]  # Top 10

def get_operator_revenue(operator_name: str, country_name: str) -> List[Dict]:
    """Extract revenue data from operator markdown files"""
    base_path = Path(__file__).parent.parent
    
    revenue_data = []
    
    # Search for operator files
    search_paths = [
        base_path / "Operators" / operator_name,
        base_path / "Europe" / country_name / operator_name,
        base_path / "Europe" / country_name,
    ]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        # Look for .md files
        for md_file in search_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Look for revenue patterns
                revenue_patterns = [
                    r'Latest annual revenue[:\s]+([€$]?[\d.,\s]+(?:\s*(?:billion|million|B|M))?)',
                    r'Revenue[:\s]+([€$]?[\d.,\s]+(?:\s*(?:billion|million|B|M))?)\s*(?:\(([^)]+)\))?',
                    r'€([\d.,\s]+(?:\s*(?:billion|million))?)\s*(?:\(([^)]+)\))?',
                ]
                
                for pattern in revenue_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        value_text = match.group(1)
                        year_text = match.group(2) if len(match.groups()) > 1 else None
                        
                        # Extract number
                        number = extract_revenue_number(value_text)
                        if number:
                            year = extract_year_from_text(year_text or match.group(0))
                            
                            revenue_data.append({
                                'year': year,
                                'value': number,
                                'unit': 'EUR',
                                'source': f"From {md_file.name}"
                            })
            except:
                pass
    
    # Sort by year (treat None as 0), then take most recent 3
    return sorted(revenue_data, key=lambda x: x.get('year') or 0, reverse=True)[:3]

def extract_revenue_number(text: str) -> Optional[float]:
    """Extract revenue number from text"""
    text = text.replace(',', '').replace(' ', '').replace('€', '').replace('$', '')
    
    patterns = [
        (r'([\d.]+)\s*billion', 1_000_000_000),
        (r'([\d.]+)\s*B\b', 1_000_000_000),
        (r'([\d.]+)\s*million', 1_000_000),
        (r'([\d.]+)\s*M\b', 1_000_000),
        (r'([\d.]+)', 1),
    ]
    
    for pattern, multiplier in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1)) * multiplier
            except:
                pass
    
    return None

def extract_year_from_text(text: str) -> Optional[int]:
    """Extract year from text"""
    if not text:
        return None
    years = re.findall(r'\b(20\d{2}|19\d{2})\b', text)
    if years:
        return int(years[-1])
    return None

def find_logo(operator_name: str) -> Optional[str]:
    """Find logo file for operator"""
    base_path = Path(__file__).parent.parent / "img"
    
    # Try different variations
    name_variations = [
        operator_name.lower().replace(' ', '-'),
        operator_name.lower().replace(' ', '_'),
        operator_name.lower(),
    ]
    
    for variation in name_variations:
        for ext in ['svg', 'png', 'jpg', 'jpeg']:
            logo_path = base_path / f"{variation}-logo.{ext}"
            if logo_path.exists():
                return f"img/{variation}-logo.{ext}"
            logo_path = base_path / f"{variation}.{ext}"
            if logo_path.exists():
                return f"img/{variation}.{ext}"
    
    return None

def get_psb_data(conn, country_name: str, base_path: Path) -> List[Dict]:
    """Get Public Service Broadcasters for country"""
    psbs = []
    
    # Check dashboard_data.json
    dashboard_data_file = base_path / "dashboard_data.json"
    if dashboard_data_file.exists():
        try:
            with open(dashboard_data_file, 'r') as f:
                data = json.load(f)
                country_data = data.get('countries', {}).get(country_name, {})
                psb_list = country_data.get('psb', [])
                
                for psb in psb_list:
                    psb_name = psb.get('name', '')
                    psbs.append({
                        'name': psb_name,
                        'logo': find_logo(psb_name) or f"img/{psb_name.lower().replace(' ', '-')}-logo.png"
                    })
        except:
            pass
    
    # Also check free-to-air-market.md
    fta_file = base_path / "Europe" / country_name / "free-to-air-market.md"
    if fta_file.exists():
        try:
            content = fta_file.read_text(encoding='utf-8')
            # Look for PSB mentions
            psb_pattern = r'(?:PSB|Public Service|Public broadcaster)[:\s]+([A-Z][^\n]+)'
            matches = re.findall(psb_pattern, content, re.IGNORECASE)
            for match in matches:
                psb_name = match.strip().split(',')[0].split('(')[0].strip()
                if psb_name and psb_name not in [p['name'] for p in psbs]:
                    psbs.append({
                        'name': psb_name,
                        'logo': find_logo(psb_name)
                    })
        except:
            pass
    
    return psbs

def generate_country_dashboard(country_name: str, conn, base_path: Path) -> str:
    """Generate HTML dashboard for a country"""
    
    # Get country data
    country_data = get_country_data(conn, country_name)
    if not country_data:
        return f"<html><body>Country '{country_name}' not found</body></html>"
    
    # Get operators
    operators = get_country_operators(conn, country_name)
    
    # Get PSBs
    psbs = get_psb_data(conn, country_name, base_path)
    
    # Prepare data
    population = country_data['facts'].get('population', {}).get('value')
    tv_households = country_data['facts'].get('tv_households', {}).get('value')
    
    operators_json = json.dumps(operators)
    psbs_json = json.dumps(psbs)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{country_name} - Broadcast Industry Dashboard</title>
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
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header-section {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 30px;
            align-items: center;
        }}
        
        .country-flag {{
            font-size: 8em;
            text-align: center;
        }}
        
        .country-info {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .country-name {{
            font-size: 3.5em;
            color: #667eea;
            font-weight: bold;
        }}
        
        .country-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .section-title {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .operators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        
        .operator-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .operator-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .operator-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .operator-logo {{
            width: 60px;
            height: 60px;
            object-fit: contain;
            background: white;
            padding: 8px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .operator-name {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        
        .subscriptions-chart {{
            height: 150px;
            margin: 15px 0;
        }}
        
        .revenue-data {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }}
        
        .revenue-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 0.9em;
        }}
        
        .revenue-year {{
            color: #666;
        }}
        
        .revenue-value {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .psb-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .psb-card {{
            background: white;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .psb-card:hover {{
            transform: scale(1.05);
        }}
        
        .psb-logo {{
            width: 120px;
            height: 120px;
            object-fit: contain;
            margin: 0 auto 15px;
        }}
        
        .psb-name {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
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
        
        .no-data {{
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="database_visualization.html" class="back-link">← Back to Main Dashboard</a>
        
        <div class="header-section">
            <div class="country-flag">{country_data['flag']}</div>
            <div class="country-info">
                <h1 class="country-name">{country_name}</h1>
                <div class="country-stats">
                    <div class="stat-box">
                        <div class="stat-value">{population:.2f}M</div>
                        <div class="stat-label">Population</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{tv_households:.2f}M</div>
                        <div class="stat-label">TV Households</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📺 Top Operators</h2>
            <div class="operators-grid" id="operatorsGrid">
                <!-- Operators will be populated by JavaScript -->
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📻 Public Service Broadcasters</h2>
            <div class="psb-grid" id="psbGrid">
                <!-- PSBs will be populated by JavaScript -->
            </div>
        </div>
    </div>
    
    <script>
        const operatorsData = {operators_json};
        const psbsData = {psbs_json};
        
        // Format value
        function formatValue(value) {{
            if (value >= 1000000) {{
                return (value / 1000000).toFixed(2) + 'M';
            }} else if (value >= 1000) {{
                return (value / 1000).toFixed(1) + 'K';
            }}
            return value.toFixed(0);
        }}
        
        // Format revenue
        function formatRevenue(value) {{
            if (value >= 1000000000) {{
                return '€' + (value / 1000000000).toFixed(2) + 'B';
            }} else if (value >= 1000000) {{
                return '€' + (value / 1000000).toFixed(2) + 'M';
            }}
            return '€' + value.toFixed(0);
        }}
        
        // Populate operators
        const operatorsGrid = document.getElementById('operatorsGrid');
        
        operatorsData.forEach((op, index) => {{
            const card = document.createElement('div');
            card.className = 'operator-card';
            
            // Operator header
            const header = document.createElement('div');
            header.className = 'operator-header';
            
            const logoImg = document.createElement('img');
            logoImg.className = 'operator-logo';
            logoImg.src = op.logo || 'img/OBS-Logo.png';
            logoImg.alt = op.canonical_name;
            logoImg.onerror = function() {{ this.style.display = 'none'; }};
            
            const nameDiv = document.createElement('div');
            nameDiv.className = 'operator-name';
            nameDiv.textContent = op.name_in_country;
            
            header.appendChild(logoImg);
            header.appendChild(nameDiv);
            
            // Subscriptions chart
            let chartHtml = '';
            if (op.subscriptions && op.subscriptions.length > 0) {{
                const years = op.subscriptions.map(s => s.year).reverse();
                const values = op.subscriptions.map(s => s.value).reverse();
                
                chartHtml = `
                    <div class="subscriptions-chart">
                        <canvas id="chart${{index}}"></canvas>
                    </div>
                `;
                
                card.innerHTML = header.outerHTML + chartHtml;
                
                // Create chart after DOM is ready
                setTimeout(() => {{
                    const canvas = document.getElementById(`chart${{index}}`);
                    if (!canvas) return;
                    
                    const ctx = canvas.getContext('2d');
                    new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: years,
                            datasets: [{{
                                label: 'Subscribers',
                                data: values,
                                borderColor: '#667eea',
                                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                tension: 0.4,
                                fill: true
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{ display: false }},
                                tooltip: {{
                                    callbacks: {{
                                        label: function(context) {{
                                            return formatValue(context.parsed.y);
                                        }}
                                    }}
                                }}
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
                }}, 200);
            }} else {{
                card.innerHTML = header.outerHTML + '<div class="no-data">No subscription data available</div>';
            }}
            
            // Revenue data
            if (op.revenue && op.revenue.length > 0) {{
                const revenueDiv = document.createElement('div');
                revenueDiv.className = 'revenue-data';
                revenueDiv.innerHTML = '<strong>Revenue:</strong>';
                
                op.revenue.forEach(rev => {{
                    const item = document.createElement('div');
                    item.className = 'revenue-item';
                    item.innerHTML = `
                        <span class="revenue-year">${{rev.year || 'N/A'}}</span>
                        <span class="revenue-value">${{formatRevenue(rev.value)}}</span>
                    `;
                    revenueDiv.appendChild(item);
                }});
                
                card.appendChild(revenueDiv);
            }}
            
            operatorsGrid.appendChild(card);
        }});
        
        // Populate PSBs
        const psbGrid = document.getElementById('psbGrid');
        
        if (psbsData.length > 0) {{
            psbsData.forEach(psb => {{
                const card = document.createElement('div');
                card.className = 'psb-card';
                
                const logoImg = document.createElement('img');
                logoImg.className = 'psb-logo';
                logoImg.src = psb.logo || 'img/OBS-Logo.png';
                logoImg.alt = psb.name;
                logoImg.onerror = function() {{ this.style.display = 'none'; }};
                
                const nameDiv = document.createElement('div');
                nameDiv.className = 'psb-name';
                nameDiv.textContent = psb.name;
                
                card.appendChild(logoImg);
                card.appendChild(nameDiv);
                psbGrid.appendChild(card);
            }});
        }} else {{
            psbGrid.innerHTML = '<div class="no-data">No Public Service Broadcasters data available</div>';
        }}
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    import sys
    
    country_name = sys.argv[1] if len(sys.argv) > 1 else "Austria"
    
    base_path = Path(__file__).parent.parent
    conn = connect_db()
    
    if not conn:
        return
    
    print(f"Generating dashboard for {country_name}...")
    html = generate_country_dashboard(country_name, conn, base_path)
    
    filename = f"{country_name.lower().replace(' ', '_')}_dashboard.html"
    output_path = base_path / filename
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Dashboard generated: {output_path}")
    print(f"Open in browser: http://localhost:8000/{filename}")
    
    conn.close()

if __name__ == "__main__":
    main()
