#!/usr/bin/env python3
"""
Create operators database table and operator-country relationships.
Handles operator name variations across countries.
Following data engineer rules: full provenance, date semantics, structured entities/facts.
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

# Operator name normalization - maps variations to canonical names
OPERATOR_ALIASES = {
    # M7 Group variations
    "M7 HD Austria": "M7 Group",
    "M7 Telesat": "M7 Group",
    "M7 Skylink CZ": "M7 Group",
    "M7 Skylink SK": "M7 Group",
    "M7 Canal Digitaal": "M7 Group",
    "M7 (HD Austria)": "M7 Group",
    "M7 (Telesat, TV Vlanderen)": "M7 Group",
    "M7 (Skylink CZ)": "M7 Group",
    "M7 (Skylink SK)": "M7 Group",
    "M7 (Canal Digitaal)": "M7 Group",
    "M7 (UPC Direct)": "M7 Group",
    "M7 Deutschland": "M7 Group",
    
    # UPC variations
    "UPC": "UPC",
    "UPC (Vodafone)": "UPC",
    "Ziggo/UPC": "UPC",
    "Ziggo-UPC": "UPC",
    
    # Magenta TV / Deutsche Telekom variations
    "Magenta TV": "Deutsche Telekom Magenta TV",
    "Magenta TV (UPC)": "Deutsche Telekom Magenta TV",
    "Deutsche Telekom Magenta TV": "Deutsche Telekom Magenta TV",
    
    # Vodafone variations
    "Vodafone Germany": "Vodafone",
    "Vodafone (Unity Media)": "Vodafone",
    "KDG/Vodafone": "Vodafone",
    "Vodafone-Czech-Republic": "Vodafone",
    
    # Allente variations
    "Allente": "Allente",
    
    # SimpliTV variations
    "SimpliTV SAT": "SimpliTV",
    "SimpliTV Terrestrial": "SimpliTV",
    "SimpliTV": "SimpliTV",
    
    # Canal+ variations
    "Canal+": "Canal+",
    "Canal+ France": "Canal+",
    "nc+/Canal+": "Canal+",
    "CANAL+-Polska": "Canal+",
    
    # Sky variations
    "SKY": "Sky",
    "Sky Deutschland": "Sky",
    "Sky Ireland": "Sky",
    "Sky-Italia": "Sky",
    
    # Boxer HD variations
    "Boxer HD": "Boxer HD",
    "Boxer-HD": "Boxer HD",
    
    # DigiTV variations
    "DigiTV (Cable)": "DigiTV",
    "DigiTV (Satellite)": "DigiTV",
    "DigiTV": "DigiTV",
    
    # Telenor variations
    "Telenor": "Telenor",
    "Telenor Norway": "Telenor",
    "Telenor (CanalDigital)": "Telenor",
    
    # Orange variations
    "Orange France": "Orange",
    "Orange-Polska": "Orange",
    "Orange": "Orange",
    
    # O2 variations
    "O2 Germany": "O2",
    "O2-Czech-Republic": "O2",
    
    # T-Mobile variations
    "T-Mobile-Czech-Republic": "T-Mobile",
    
    # Tele2 variations
    "Tele2": "Tele2",
    
    # Telia variations
    "Telia-Finland": "Telia",
    "Telia Norway": "Telia",
    
    # HD+ variations
    "HD+": "HD+",
    "HD+ (non-OpApp)": "HD+",
    
    # Fransat variations
    "Fransat": "Fransat",
    "Fransat Connect": "Fransat",
    
    # Tivusat variations
    "Tivusat - LaTivu": "Tivusat",
    "Tivusat---LaTivu": "Tivusat",
    
    # Other operators
    "Telenet": "Telenet",
    "Voo": "Voo",
    "YouSee": "YouSee",
    "Norlys": "Norlys",
    "Ziggo": "Ziggo",
    "Kabelio": "Kabelio",
    "PYUR": "PYUR",
    "PYÜR": "PYUR",
    "Telecolumbus(PÜYR)": "PYUR",
    "Freely": "Freely",
    "EE": "EE",
    "Talk Talk": "Talk Talk",
    "VirginMedia": "Virgin Media",
    "Virgin Media Ireland": "Virgin Media",
    "Saorview": "Saorview",
    "RiksTV": "RiksTV",
    "Riks TV": "RiksTV",
    "ORF": "ORF",
    "ORF (SAT+Terrestrial)": "ORF",
    "ORS Austria": "ORS Austria",
    "T2 CZ": "T2 CZ",
    "T2-CZ": "T2 CZ",
    "Proximus-Pickx": "Proximus Pickx",
    "Proximus Pickx": "Proximus Pickx",
    "Elisa": "Elisa",
    "Stofa": "Stofa",
    "Levira": "Levira",
    "evoTV (merged with Telekom)": "evoTV",
    "Hakom": "Hakom",
    "Digital TV": "Digital TV",
    "DVB-T/T2 Spec": "DVB-T/T2",
    "DVB-T2 HD": "DVB-T2",
    "TDT Hibrida (LovesTV)": "LovesTV",
    "MinDigTV": "MinDigTV",
    "CableHDReady": "CableHDReady",
    "AntennaHDReady": "AntennaHDReady",
    "A1 Telekom Austria": "A1 Telekom Austria",
    "Drei Austria": "Drei Austria",
    "ServusTV": "ServusTV",
    "France-24": "France 24",
    "Bouygues Telecom": "Bouygues Telecom",
    "Free France": "Free France",
    "SFR": "SFR",
    "Swisscom-TV": "Swisscom TV",
    "Swisscom TV": "Swisscom TV",
    "Sunrise": "Sunrise",
    "Zattoo": "Zattoo",
    "RAI": "RAI",
    "Mediaset": "Mediaset",
    "TIM": "TIM",
    "Cyfrowy-Polsat": "Cyfrowy Polsat",
    "Vectra": "Vectra",
    "KPN": "KPN",
    "Eir": "Eir",
    "Altibox": "Altibox",
}

def normalize_operator_name(name: str) -> str:
    """Normalize operator name to canonical form"""
    # Clean up the name
    name = name.strip()
    
    # Check if we have a direct alias mapping
    if name in OPERATOR_ALIASES:
        return OPERATOR_ALIASES[name]
    
    # Try to find partial matches
    for alias, canonical in OPERATOR_ALIASES.items():
        if alias.lower() in name.lower() or name.lower() in alias.lower():
            return canonical
    
    # If no match, return cleaned name
    return name


def extract_operator_from_spec_file(spec_file: Path) -> Optional[Dict]:
    """Extract operator information from specifications.md file"""
    if not spec_file.exists():
        return None
    
    try:
        content = spec_file.read_text(encoding='utf-8')
        
        # Extract country and operator from file
        country_match = re.search(r'\*\*Country\*\*:\s*(.+)', content)
        operator_match = re.search(r'\*\*Operator\*\*:\s*(.+)', content)
        
        country = country_match.group(1).strip() if country_match else None
        operator = operator_match.group(1).strip() if operator_match else None
        
        # If not found in content, try to infer from directory structure
        if not country or not operator:
            parts = spec_file.parts
            if 'Europe' in parts:
                europe_idx = parts.index('Europe')
                if len(parts) > europe_idx + 1:
                    country = parts[europe_idx + 1]
                if len(parts) > europe_idx + 2:
                    operator = parts[europe_idx + 2]
        
        if country and operator:
            return {
                'country': country,
                'operator': operator,
                'file_path': str(spec_file),
                'canonical_operator': normalize_operator_name(operator)
            }
    except Exception as e:
        print(f"Error reading {spec_file}: {e}")
    
    return None


def scan_operators(base_path: Path) -> Tuple[Dict[str, Set[str]], Dict[str, Dict]]:
    """
    Scan directory structure for operators.
    Returns:
        - operator_countries: dict mapping canonical operator name to set of countries
        - operator_details: dict with operator metadata
    """
    europe_dir = base_path / "Europe"
    operator_countries = defaultdict(set)
    operator_details = {}
    
    if not europe_dir.exists():
        print("Europe directory not found")
        return operator_countries, operator_details
    
    # Scan all specifications.md files
    for spec_file in europe_dir.rglob("specifications.md"):
        op_info = extract_operator_from_spec_file(spec_file)
        
        if op_info:
            country = op_info['country']
            canonical_op = op_info['canonical_operator']
            original_op = op_info['operator']
            
            operator_countries[canonical_op].add(country)
            
            # Store details (keep first occurrence or merge)
            if canonical_op not in operator_details:
                operator_details[canonical_op] = {
                    'canonical_name': canonical_op,
                    'aliases': [original_op] if original_op != canonical_op else [],
                    'countries': [country],
                    'file_paths': [op_info['file_path']]
                }
            else:
                # Add alias if different
                if original_op != canonical_op and original_op not in operator_details[canonical_op]['aliases']:
                    operator_details[canonical_op]['aliases'].append(original_op)
                # Add country if new
                if country not in operator_details[canonical_op]['countries']:
                    operator_details[canonical_op]['countries'].append(country)
                # Add file path
                if op_info['file_path'] not in operator_details[canonical_op]['file_paths']:
                    operator_details[canonical_op]['file_paths'].append(op_info['file_path'])
    
    return operator_countries, operator_details


def create_operators_schema(conn):
    """Create operators and operator_countries tables"""
    cursor = conn.cursor()
    
    # Operators table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operators (
            operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_name TEXT NOT NULL UNIQUE,
            aliases TEXT,
            parent_company TEXT,
            website TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Operator-Country junction table (many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operator_countries (
            operator_country_id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER NOT NULL,
            country_id INTEGER NOT NULL,
            operator_name_in_country TEXT,
            source_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (operator_id) REFERENCES operators(operator_id),
            FOREIGN KEY (country_id) REFERENCES countries(country_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id),
            UNIQUE(operator_id, country_id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operators_name ON operators(canonical_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operator_countries_op ON operator_countries(operator_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operator_countries_country ON operator_countries(country_id)")
    
    conn.commit()


def create_operator_entity(conn, canonical_name: str, aliases: Optional[List[str]] = None,
                           parent_company: Optional[str] = None, website: Optional[str] = None) -> int:
    """Create or get operator entity and return operator_id"""
    cursor = conn.cursor()
    
    aliases_json = json.dumps(aliases) if aliases else None
    
    cursor.execute("""
        INSERT OR IGNORE INTO operators (canonical_name, aliases, parent_company, website)
        VALUES (?, ?, ?, ?)
    """, (canonical_name, aliases_json, parent_company, website))
    
    # Get the operator_id
    cursor.execute("""
        SELECT operator_id FROM operators WHERE canonical_name = ?
    """, (canonical_name,))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    conn.commit()
    return cursor.lastrowid


def get_country_id(conn, country_name: str) -> Optional[int]:
    """Get country_id from country name"""
    cursor = conn.cursor()
    cursor.execute("SELECT country_id FROM countries WHERE country_name = ?", (country_name,))
    result = cursor.fetchone()
    return result[0] if result else None


def link_operator_to_country(conn, operator_id: int, country_id: int, 
                             operator_name_in_country: Optional[str] = None,
                             source_id: Optional[int] = None, notes: Optional[str] = None):
    """Link operator to country"""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR IGNORE INTO operator_countries 
        (operator_id, country_id, operator_name_in_country, source_id, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (operator_id, country_id, operator_name_in_country, source_id, notes))
    
    conn.commit()


def load_operators(conn, base_path: Path):
    """Load operators and country relationships"""
    print("Scanning directory structure for operators...")
    operator_countries, operator_details = scan_operators(base_path)
    
    print(f"Found {len(operator_countries)} unique operators")
    
    # Create source for operator data
    source_id = create_source(
        conn,
        url="file://" + str(base_path / "Europe"),
        publisher="Internal Research",
        published_at="2024-01-01"
    )
    
    operators_loaded = 0
    relationships_created = 0
    
    for canonical_name, countries in sorted(operator_countries.items()):
        details = operator_details.get(canonical_name, {})
        aliases = details.get('aliases', [])
        
        print(f"Loading {canonical_name} ({len(countries)} countries)...")
        
        # Create operator entity
        operator_id = create_operator_entity(
            conn,
            canonical_name=canonical_name,
            aliases=aliases if aliases else None
        )
        
        # Also create entity in entities table for consistency
        entity_id = create_entity(
            conn,
            entity_type="operator",
            canonical_name=canonical_name,
            aliases=aliases if aliases else None
        )
        
        # Link to countries
        for country_name in sorted(countries):
            country_id = get_country_id(conn, country_name)
            
            if country_id:
                # Find the operator name used in this country
                country_operator_name = None
                for file_path in details.get('file_paths', []):
                    if country_name in file_path:
                        # Extract operator name from path
                        parts = Path(file_path).parts
                        if 'Europe' in parts:
                            idx = parts.index('Europe')
                            if len(parts) > idx + 2:
                                country_operator_name = parts[idx + 2]
                                break
                
                link_operator_to_country(
                    conn,
                    operator_id=operator_id,
                    country_id=country_id,
                    operator_name_in_country=country_operator_name,
                    source_id=source_id,
                    notes=f"Extracted from {base_path / 'Europe'} directory structure"
                )
                relationships_created += 1
            else:
                print(f"  Warning: Country '{country_name}' not found in countries table")
        
        operators_loaded += 1
    
    print(f"\nLoaded {operators_loaded} operators")
    print(f"Created {relationships_created} operator-country relationships")
    
    return operators_loaded, relationships_created


def create_source(conn, url: str, publisher: str, published_at: Optional[str] = None) -> int:
    """Create a source record and return source_id"""
    cursor = conn.cursor()
    retrieved_at = datetime.now().date().isoformat()
    
    cursor.execute("""
        INSERT INTO sources (url, publisher, published_at, retrieved_at)
        VALUES (?, ?, ?, ?)
    """, (url, publisher, published_at, retrieved_at))
    
    conn.commit()
    return cursor.lastrowid


def create_entity(conn, entity_type: str, canonical_name: str, aliases: Optional[List[str]] = None,
                  external_ids: Optional[Dict] = None) -> int:
    """Create or get entity and return entity_id"""
    cursor = conn.cursor()
    
    aliases_json = json.dumps(aliases) if aliases else None
    external_ids_json = json.dumps(external_ids) if external_ids else None
    
    cursor.execute("""
        INSERT OR IGNORE INTO entities (entity_type, canonical_name, aliases, external_ids)
        VALUES (?, ?, ?, ?)
    """, (entity_type, canonical_name, aliases_json, external_ids_json))
    
    # Get the entity_id
    cursor.execute("""
        SELECT entity_id FROM entities 
        WHERE entity_type = ? AND canonical_name = ?
    """, (entity_type, canonical_name))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    conn.commit()
    return cursor.lastrowid


def generate_operators_summary(conn):
    """Generate summary report of operators"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("OPERATORS DATABASE SUMMARY")
    print("=" * 80)
    
    # Total operators
    cursor.execute("SELECT COUNT(*) FROM operators")
    total_ops = cursor.fetchone()[0]
    print(f"\nTotal operators: {total_ops}")
    
    # Operators by country count
    cursor.execute("""
        SELECT o.canonical_name, COUNT(oc.country_id) as country_count
        FROM operators o
        LEFT JOIN operator_countries oc ON o.operator_id = oc.operator_id
        GROUP BY o.operator_id, o.canonical_name
        ORDER BY country_count DESC, o.canonical_name
        LIMIT 15
    """)
    
    print("\nTop operators by country coverage:")
    for row in cursor.fetchall():
        name, count = row
        print(f"  {name:40s}: {count:2d} countries")
    
    # Total relationships
    cursor.execute("SELECT COUNT(*) FROM operator_countries")
    total_rel = cursor.fetchone()[0]
    print(f"\nTotal operator-country relationships: {total_rel}")
    
    # Countries with most operators
    cursor.execute("""
        SELECT c.country_name, COUNT(oc.operator_id) as operator_count
        FROM countries c
        JOIN operator_countries oc ON c.country_id = oc.country_id
        WHERE c.region = 'Europe'
        GROUP BY c.country_id, c.country_name
        ORDER BY operator_count DESC, c.country_name
        LIMIT 10
    """)
    
    print("\nTop countries by operator count:")
    for row in cursor.fetchall():
        country, count = row
        print(f"  {country:30s}: {count:2d} operators")


def main():
    base_path = Path(__file__).parent.parent
    db_path = base_path / "broadcast_industry.db"
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Please run create_countries_database.py first")
        return
    
    conn = sqlite3.connect(str(db_path))
    
    print("Creating operators schema...")
    create_operators_schema(conn)
    
    print("Loading operators...")
    load_operators(conn, base_path)
    
    generate_operators_summary(conn)
    
    conn.close()
    print(f"\nOperators database updated at: {db_path}")


if __name__ == "__main__":
    main()
