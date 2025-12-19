#!/usr/bin/env python3
"""
Extract subscription/subscriber data from operator markdown files.
Only includes data with clear sources and years.
Following data engineer rules: full provenance, date semantics, structured facts.
"""

import sqlite3
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import unicodedata

def connect_db():
    """Connect to the database"""
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(str(db_path))

def normalize_text(text):
    """Normalize text for matching"""
    if not text:
        return ""
    # Remove accents and normalize
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text.lower().strip()

def extract_year(text: str) -> Optional[int]:
    """Extract year from text"""
    # Look for 4-digit years (1900-2100) - be more specific
    # Prefer years in parentheses or after "as of", "in", etc.
    patterns = [
        r'\b(20\d{2}|19\d{2})\b',  # Full 4-digit years
        r'\((\d{4})\)',  # Years in parentheses
        r'(?:as of|in|since|from)\s+(\d{4})',  # Years after common phrases
        r'(\d{4})\s+(?:subscribers|customers|households)',  # Years before metrics
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Get the last match (most recent)
            year_str = matches[-1] if isinstance(matches[-1], str) else str(matches[-1])
            try:
                year = int(year_str)
                if 1900 <= year <= 2100:
                    return year
            except:
                pass
    
    return None

def extract_number(text: str) -> Optional[float]:
    """Extract number from text, handling millions, thousands, etc."""
    # Remove common formatting
    text = text.replace(',', '').replace(' ', '')
    
    # Pattern for numbers with units
    patterns = [
        (r'~?([\d.]+)\s*million', 1_000_000),
        (r'~?([\d.]+)\s*M\b', 1_000_000),
        (r'~?([\d.]+)\s*thousand', 1_000),
        (r'~?([\d.]+)\s*K\b', 1_000),
        (r'~?([\d.]+)\s*billion', 1_000_000_000),
        (r'~?([\d.]+)\s*B\b', 1_000_000_000),
        (r'~?([\d.]+)', 1),  # Plain number
    ]
    
    for pattern, multiplier in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1)) * multiplier
            except:
                pass
    
    return None

def find_source_in_text(text: str, context: str = "") -> Optional[str]:
    """Try to identify source from text"""
    # Look for common source indicators
    source_patterns = [
        r'Source[:\s]+([^\n]+)',
        r'from ([^\n]+)',
        r'according to ([^\n]+)',
        r'\(([^)]+)\)',  # Parenthetical citations
        r'\[([^\]]+)\]',  # Bracketed citations
    ]
    
    for pattern in source_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return the most specific/longest match
            return max(matches, key=len).strip()
    
    # If no explicit source, check if it's from a specific file
    if context:
        if 'demographics.md' in context:
            return "Internal demographics research"
        if 'specifications.md' in context:
            return "Operator specifications file"
        if '.md' in context:
            return f"From {Path(context).name}"
    
    return None

def extract_subscription_data_from_file(file_path: Path) -> List[Dict]:
    """Extract subscription data from a markdown file"""
    subscriptions = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Get operator and country from file path or content
        country = None
        operator = None
        
        # Try to extract from file path
        parts = file_path.parts
        if 'Europe' in parts:
            idx = parts.index('Europe')
            if len(parts) > idx + 1:
                country = parts[idx + 1]
            if len(parts) > idx + 2:
                operator = parts[idx + 2]
        
        # Try to extract from content
        country_match = re.search(r'\*\*Country\*\*:\s*(.+)', content)
        if country_match:
            country = country_match.group(1).strip()
        
        operator_match = re.search(r'\*\*Operator\*\*:\s*(.+)', content)
        if operator_match:
            operator = operator_match.group(1).strip()
        
        # Also try to get operator from title
        if not operator:
            title_match = re.search(r'^#\s+(.+?)(?:\s+[-–]|$)', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                # Skip if it's clearly not an operator name
                if 'demographics' not in title.lower() and 'specification' not in title.lower():
                    operator = title
        
        # Look for subscriber/subscription patterns
        # Pattern 1: "Subscribers: ~X million (YEAR)"
        pattern1 = re.compile(
            r'(?:Subscribers?|subscriptions?|customers?|households?)[:\s]+'
            r'~?([\d.,\s]+(?:\s*(?:million|thousand|M|K|billion|B))?)\s*'
            r'(?:\(([^)]+)\))?',
            re.IGNORECASE
        )
        
        # Pattern 2: "~X million subscribers (YEAR)"
        pattern2 = re.compile(
            r'~?([\d.,\s]+(?:\s*(?:million|thousand|M|K|billion|B))?)\s+'
            r'(?:subscribers?|subscriptions?|customers?|households?)'
            r'(?:\s+\(([^)]+)\))?',
            re.IGNORECASE
        )
        
        # Pattern 3: "Total Pay-TV households: ~X million"
        pattern3 = re.compile(
            r'(?:Total|Total\s+(?:Pay-TV|TV|broadband|FTTH|mobile))\s+'
            r'(?:households?|subscribers?|customers?)[:\s]+'
            r'~?([\d.,\s]+(?:\s*(?:million|thousand|M|K|billion|B))?)\s*'
            r'(?:\(([^)]+)\))?',
            re.IGNORECASE
        )
        
        patterns = [pattern1, pattern2, pattern3]
        
        for pattern in patterns:
            for match in pattern.finditer(content):
                value_text = match.group(1) if match.group(1) else ""
                context_text = match.group(2) if len(match.groups()) > 1 and match.group(2) else ""
                
                # Extract number
                number = extract_number(value_text)
                if not number:
                    continue
                
                # Extract year
                full_match_text = match.group(0) + " " + context_text
                year = extract_year(full_match_text)
                
                # Get context around the match
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 200)
                context = content[start:end]
                
                # Find source
                source = find_source_in_text(context, str(file_path))
                
                # Only include if we have a year or clear source
                if year or source:
                    subscriptions.append({
                        'operator': operator,
                        'country': country,
                        'value': number,
                        'year': year,
                        'source': source or "From operator file",
                        'file_path': str(file_path),
                        'context': context[:100]  # First 100 chars for reference
                    })
        
        # Also look for specific structured data sections
        # Look for "Subscriber Overview" sections
        subscriber_section = re.search(
            r'##\s*3\.\s*Subscriber\s+Overview.*?##\s*4\.',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if subscriber_section:
            section_content = subscriber_section.group(0)
            # Extract structured data from this section
            structured_patterns = [
                (r'Total\s+households?\s+served[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)\s*(?:\(([^)]+)\))?', 'total_households'),
                (r'Total\s+Pay-TV\s+households?[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)\s*(?:\(([^)]+)\))?', 'paytv_households'),
                (r'Total\s+broadband\s+households?[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)\s*(?:\(([^)]+)\))?', 'broadband_households'),
                (r'Total\s+FTTH\s+households?[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)\s*(?:\(([^)]+)\))?', 'ftth_households'),
                (r'Total\s+video\s+customers?[:\s]+~?([\d.,\s]+(?:\s*(?:million|thousand|M|K))?)\s*(?:\(([^)]+)\))?', 'video_customers'),
            ]
            
            for pattern, metric_type in structured_patterns:
                for match in re.finditer(pattern, section_content, re.IGNORECASE):
                    value_text = match.group(1)
                    context_text = match.group(2) if len(match.groups()) > 1 and match.group(2) else ""
                    
                    number = extract_number(value_text)
                    if not number:
                        continue
                    
                    full_text = match.group(0) + " " + context_text
                    year = extract_year(full_text)
                    
                    source = find_source_in_text(section_content, str(file_path))
                    
                    if year or source:
                        subscriptions.append({
                            'operator': operator,
                            'country': country,
                            'value': number,
                            'year': year,
                            'source': source or "From Subscriber Overview section",
                            'file_path': str(file_path),
                            'metric_type': metric_type,
                            'context': match.group(0)[:100]
                        })
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return subscriptions

def create_subscriptions_table(conn):
    """Create subscriptions table in database"""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER,
            country_id INTEGER,
            operator_name TEXT NOT NULL,
            country_name TEXT NOT NULL,
            subscription_value REAL NOT NULL,
            unit TEXT DEFAULT 'subscribers',
            metric_type TEXT,
            year INTEGER,
            observed_at DATE,
            source_id INTEGER,
            source_text TEXT,
            file_path TEXT,
            context TEXT,
            confidence TEXT DEFAULT 'medium',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (operator_id) REFERENCES operators(operator_id),
            FOREIGN KEY (country_id) REFERENCES countries(country_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_operator ON subscriptions(operator_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_country ON subscriptions(country_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_year ON subscriptions(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_operator_country ON subscriptions(operator_name, country_name)")
    
    conn.commit()

def get_operator_id(conn, operator_name: str) -> Optional[int]:
    """Get operator_id from canonical name"""
    cursor = conn.cursor()
    cursor.execute("SELECT operator_id FROM operators WHERE canonical_name = ?", (operator_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_country_id(conn, country_name: str) -> Optional[int]:
    """Get country_id from country name"""
    cursor = conn.cursor()
    cursor.execute("SELECT country_id FROM countries WHERE country_name = ?", (country_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_source(conn, source_text: str, file_path: str = None) -> int:
    """Create or get source record"""
    cursor = conn.cursor()
    retrieved_at = datetime.now().date().isoformat()
    
    # Check if source exists
    cursor.execute("""
        SELECT source_id FROM sources 
        WHERE publisher = ? AND url LIKE ?
    """, (source_text, f"%{file_path}%"))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Create new source
    cursor.execute("""
        INSERT INTO sources (publisher, url, retrieved_at)
        VALUES (?, ?, ?)
    """, (source_text, file_path or "", retrieved_at))
    
    conn.commit()
    return cursor.lastrowid

def load_subscriptions(conn, base_path: Path):
    """Load subscription data from all operator files"""
    print("Scanning for subscription data...")
    
    # Find all operator markdown files
    operator_files = []
    
    # Check Operators directory
    operators_dir = base_path / "Operators"
    if operators_dir.exists():
        operator_files.extend(operators_dir.rglob("*.md"))
    
    # Check Europe directory
    europe_dir = base_path / "Europe"
    if europe_dir.exists():
        operator_files.extend(europe_dir.rglob("*.md"))
    
    # Also check root level
    root_files = list(base_path.glob("*.md"))
    operator_files.extend(root_files)
    
    print(f"Found {len(operator_files)} markdown files to scan")
    
    all_subscriptions = []
    
    for file_path in operator_files:
        # Skip certain files
        if any(skip in str(file_path) for skip in ['README', 'SUMMARY', 'strategy', 'contacts']):
            continue
        
        subscriptions = extract_subscription_data_from_file(file_path)
        all_subscriptions.extend(subscriptions)
        if subscriptions:
            print(f"  Found {len(subscriptions)} subscription entries in {file_path.name}")
    
    print(f"\nTotal subscription entries found: {len(all_subscriptions)}")
    
    # Filter to only include entries with sources or years
    valid_subscriptions = [
        s for s in all_subscriptions
        if s.get('year') or s.get('source')
    ]
    
    print(f"Valid subscriptions (with year or source): {len(valid_subscriptions)}")
    
    # Load into database
    subscriptions_loaded = 0
    
    for sub in valid_subscriptions:
        operator_name = (sub.get('operator') or '').strip()
        country_name = (sub.get('country') or '').strip()
        
        # Skip if no operator or country
        if not operator_name or not country_name:
            continue
        
        # Get IDs
        operator_id = get_operator_id(conn, operator_name)
        country_id = get_country_id(conn, country_name)
        
        # Create source
        source_text = sub.get('source', 'Unknown source')
        source_id = create_source(conn, source_text, sub.get('file_path'))
        
        # Insert subscription
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscriptions (
                operator_id, country_id, operator_name, country_name,
                subscription_value, unit, metric_type, year,
                source_id, source_text, file_path, context, confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            operator_id,
            country_id,
            operator_name,
            country_name,
            sub['value'],
            'subscribers',
            sub.get('metric_type'),
            sub.get('year'),
            source_id,
            source_text,
            sub.get('file_path'),
            sub.get('context'),
            'high' if sub.get('year') and sub.get('source') else 'medium'
        ))
        
        subscriptions_loaded += 1
    
    conn.commit()
    print(f"\nLoaded {subscriptions_loaded} subscription records into database")
    
    return subscriptions_loaded

def generate_subscriptions_table(conn) -> str:
    """Generate HTML table of subscriptions"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            s.operator_name,
            s.country_name,
            s.subscription_value,
            s.year,
            s.source_text,
            s.file_path,
            s.metric_type,
            s.confidence
        FROM subscriptions s
        ORDER BY s.year DESC, s.country_name, s.operator_name
    """)
    
    rows = cursor.fetchall()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Subscription Data - Fact Checked</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #667eea; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .value { font-weight: bold; color: #667eea; }
            .year { color: #666; }
            .source { font-size: 0.9em; color: #555; }
        </style>
    </head>
    <body>
        <h1>Subscription Data - Fact Checked</h1>
        <p>Only includes data with clear sources and years.</p>
        <table>
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
            <tbody>
    """
    
    for row in rows:
        operator, country, value, year, source, file_path, metric_type, confidence = row
        
        # Format value
        if value >= 1_000_000:
            value_str = f"{value/1_000_000:.2f}M"
        elif value >= 1_000:
            value_str = f"{value/1_000:.1f}K"
        else:
            value_str = f"{value:.0f}"
        
        html += f"""
                <tr>
                    <td class="year">{year or 'N/A'}</td>
                    <td>{operator}</td>
                    <td>{country}</td>
                    <td class="value">{value_str}</td>
                    <td>{metric_type or 'total'}</td>
                    <td class="source">{source}</td>
                    <td>{confidence}</td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    return html

def main():
    base_path = Path(__file__).parent.parent
    conn = connect_db()
    
    if not conn:
        return
    
    print("Creating subscriptions table...")
    create_subscriptions_table(conn)
    
    print("Loading subscription data...")
    count = load_subscriptions(conn, base_path)
    
    print("\nGenerating HTML table...")
    html = generate_subscriptions_table(conn)
    
    output_path = base_path / "subscriptions_table.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"\nSubscription table generated: {output_path}")
    print(f"Open in browser: http://localhost:8000/subscriptions_table.html")
    
    conn.close()

if __name__ == "__main__":
    main()
