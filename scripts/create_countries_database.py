#!/usr/bin/env python3
"""
Create a comprehensive countries database with regions for the global broadcast industry.
Following data engineer rules: full provenance, date semantics, and structured entities/facts.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

# ISO 3166-1 alpha-2 country codes and comprehensive country list
# Grouped by regions: Europe, Asia, South America, North America, Oceania, Africa

WORLD_COUNTRIES = {
    # EUROPE (46 countries from directory + standard list)
    "Europe": [
        "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", 
        "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
        "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia",
        "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia",
        "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco",
        "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
        "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
        "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine",
        "United Kingdom", "Vatican City"
    ],
    # ASIA
    "Asia": [
        "Afghanistan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia",
        "China", "East Timor", "India", "Indonesia", "Iran", "Iraq", "Israel",
        "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos",
        "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal",
        "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar",
        "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria",
        "Taiwan", "Tajikistan", "Thailand", "Turkmenistan", "United Arab Emirates",
        "Uzbekistan", "Vietnam", "Yemen"
    ],
    # SOUTH AMERICA
    "South America": [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
        "French Guiana", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay",
        "Venezuela"
    ],
    # NORTH AMERICA (including Central America and Caribbean)
    "North America": [
        "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada",
        "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador",
        "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico",
        "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia",
        "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"
    ],
    # OCEANIA
    "Oceania": [
        "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia",
        "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa",
        "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
    ],
    # AFRICA
    "Africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
        "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
        "Congo", "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea",
        "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
        "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar",
        "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique",
        "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe",
        "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
        "Zambia", "Zimbabwe"
    ]
}

# ISO 3166-1 alpha-2 country codes mapping
ISO_CODES = {
    "Albania": "AL", "Andorra": "AD", "Armenia": "AM", "Austria": "AT",
    "Azerbaijan": "AZ", "Belarus": "BY", "Belgium": "BE", "Bosnia and Herzegovina": "BA",
    "Bulgaria": "BG", "Croatia": "HR", "Cyprus": "CY", "Czech Republic": "CZ",
    "Denmark": "DK", "Estonia": "EE", "Finland": "FI", "France": "FR",
    "Georgia": "GE", "Germany": "DE", "Greece": "GR", "Hungary": "HU",
    "Iceland": "IS", "Ireland": "IE", "Italy": "IT", "Latvia": "LV",
    "Liechtenstein": "LI", "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT",
    "Moldova": "MD", "Monaco": "MC", "Montenegro": "ME", "Netherlands": "NL",
    "North Macedonia": "MK", "Norway": "NO", "Poland": "PL", "Portugal": "PT",
    "Romania": "RO", "Russia": "RU", "San Marino": "SM", "Serbia": "RS",
    "Slovakia": "SK", "Slovenia": "SI", "Spain": "ES", "Sweden": "SE",
    "Switzerland": "CH", "Turkey": "TR", "Ukraine": "UA", "United Kingdom": "GB",
    "Vatican City": "VA"
}

def create_database_schema(db_path: str):
    """Create database schema following data engineer rules"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Sources table - tracks all data sources
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            publisher TEXT,
            published_at DATE,
            retrieved_at DATE NOT NULL,
            license_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Entities table - countries, operators, broadcasters, etc.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL,
            canonical_name TEXT NOT NULL,
            aliases TEXT,
            external_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type, canonical_name)
        )
    """)
    
    # Facts table - all facts about entities with full provenance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id INTEGER NOT NULL,
            fact_type TEXT NOT NULL,
            value_json TEXT NOT NULL,
            unit TEXT,
            observed_at DATE,
            published_at DATE,
            retrieved_at DATE NOT NULL,
            source_id INTEGER NOT NULL,
            confidence TEXT,
            notes TEXT,
            valid_from DATE,
            valid_to DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (entity_id) REFERENCES entities(entity_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        )
    """)
    
    # Countries table - comprehensive list with regions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            country_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT NOT NULL UNIQUE,
            iso_code TEXT,
            region TEXT NOT NULL,
            subregion TEXT,
            has_data BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_type_name ON entities(entity_type, canonical_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_entity ON facts(entity_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_type ON facts(fact_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_observed ON facts(observed_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_countries_region ON countries(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_countries_iso ON countries(iso_code)")
    
    conn.commit()
    return conn


def load_countries(conn):
    """Load all countries into the countries table"""
    cursor = conn.cursor()
    
    # Get existing European countries from directory
    europe_dir = Path(__file__).parent.parent / "Europe"
    european_countries_with_data = set()
    
    if europe_dir.exists():
        for country_dir in europe_dir.iterdir():
            if country_dir.is_dir() and country_dir.name not in ["Multi-Country"]:
                country_name = country_dir.name
                # Check if demographics file exists
                if (country_dir / "demographics.md").exists():
                    european_countries_with_data.add(country_name)
    
    # Insert all countries
    for region, countries_list in WORLD_COUNTRIES.items():
        for country in countries_list:
            iso_code = ISO_CODES.get(country)
            has_data = country in european_countries_with_data
            
            cursor.execute("""
                INSERT OR IGNORE INTO countries (country_name, iso_code, region, has_data)
                VALUES (?, ?, ?, ?)
            """, (country, iso_code, region, has_data))
    
    conn.commit()
    print(f"Loaded {len([c for countries in WORLD_COUNTRIES.values() for c in countries])} countries into database")


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


def insert_fact(conn, entity_id: int, fact_type: str, value: any, unit: Optional[str] = None,
                observed_at: Optional[str] = None, published_at: Optional[str] = None,
                source_id: int = None, confidence: str = "medium", notes: Optional[str] = None):
    """Insert a fact with full provenance"""
    cursor = conn.cursor()
    retrieved_at = datetime.now().date().isoformat()
    value_json = json.dumps(value)
    
    cursor.execute("""
        INSERT INTO facts (entity_id, fact_type, value_json, unit, observed_at, 
                          published_at, retrieved_at, source_id, confidence, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (entity_id, fact_type, value_json, unit, observed_at, published_at, 
          retrieved_at, source_id, confidence, notes))
    
    conn.commit()


def parse_demographics_file(file_path: Path) -> Dict:
    """Parse a demographics.md file and extract structured data"""
    data = {}
    
    if not file_path.exists():
        return data
    
    content = file_path.read_text(encoding='utf-8')
    
    # Extract population
    pop_match = re.search(r'\*\*Total population\*\*:\s*~?([\d.]+)\s*million', content)
    if pop_match:
        data['population_million'] = float(pop_match.group(1))
    
    # Extract TV households
    tv_match = re.search(r'\*\*Total TV households\*\*:\s*~?([\d.]+)\s*million', content)
    if tv_match:
        data['tv_households_million'] = float(tv_match.group(1))
    
    # Extract GDP
    gdp_match = re.search(r'\*\*GDP \(total\)\*\*:\s*~?([€$]?[\d.]+)\s*(trillion|billion)', content)
    if gdp_match:
        value = float(gdp_match.group(1).replace('€', '').replace('$', ''))
        unit = gdp_match.group(2)
        data['gdp_total'] = value
        data['gdp_unit'] = unit
    
    # Extract GDP per capita
    gdp_capita_match = re.search(r'\*\*GDP per capita\*\*:\s*~?([€$]?[\d,]+)', content)
    if gdp_capita_match:
        value = float(gdp_capita_match.group(1).replace('€', '').replace('$', '').replace(',', ''))
        data['gdp_per_capita'] = value
    
    # Extract broadband penetration
    bb_match = re.search(r'\*\*Broadband penetration\*\*:\s*~?([\d.]+)%', content)
    if bb_match:
        data['broadband_penetration_pct'] = float(bb_match.group(1))
    
    # Extract Smart TV penetration
    stv_match = re.search(r'\*\*Smart TV penetration\*\*:\s*~?([\d.]+)%', content)
    if stv_match:
        data['smart_tv_penetration_pct'] = float(stv_match.group(1))
    
    # Extract Pay-TV households
    paytv_match = re.search(r'\*\*Pay-TV households\*\*:\s*~?([\d.]+)\s*million', content)
    if paytv_match:
        data['paytv_households_million'] = float(paytv_match.group(1))
    
    # Extract SVOD penetration
    svod_match = re.search(r'\*\*SVOD penetration\*\*:\s*~?([\d.]+)%', content)
    if svod_match:
        data['svod_penetration_pct'] = float(svod_match.group(1))
    
    return data


def load_european_data(conn, base_path: Path):
    """Load European country data from demographics files"""
    europe_dir = base_path / "Europe"
    
    if not europe_dir.exists():
        print("Europe directory not found")
        return
    
    # Create source for demographics files
    source_id = create_source(
        conn,
        url="file://" + str(europe_dir),
        publisher="Internal Research",
        published_at="2024-01-01"  # Approximate, should be updated with actual dates
    )
    
    countries_loaded = 0
    facts_inserted = 0
    
    for country_dir in sorted(europe_dir.iterdir()):
        if not country_dir.is_dir() or country_dir.name == "Multi-Country":
            continue
        
        country_name = country_dir.name
        demographics_file = country_dir / "demographics.md"
        
        if not demographics_file.exists():
            continue
        
        print(f"Processing {country_name}...")
        
        # Create country entity
        country_entity_id = create_entity(
            conn,
            entity_type="country",
            canonical_name=country_name,
            external_ids={"iso_code": ISO_CODES.get(country_name)}
        )
        
        # Parse demographics
        demo_data = parse_demographics_file(demographics_file)
        
        # Insert facts
        observed_at = "2024-01-01"  # Should be extracted from file if available
        
        if 'population_million' in demo_data:
            insert_fact(
                conn, country_entity_id, "population", demo_data['population_million'],
                unit="million", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'tv_households_million' in demo_data:
            insert_fact(
                conn, country_entity_id, "tv_households", demo_data['tv_households_million'],
                unit="million", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'gdp_total' in demo_data:
            insert_fact(
                conn, country_entity_id, "gdp_total", demo_data['gdp_total'],
                unit=demo_data.get('gdp_unit', 'billion'), observed_at=observed_at,
                source_id=source_id, confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'gdp_per_capita' in demo_data:
            insert_fact(
                conn, country_entity_id, "gdp_per_capita", demo_data['gdp_per_capita'],
                unit="currency", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'broadband_penetration_pct' in demo_data:
            insert_fact(
                conn, country_entity_id, "broadband_penetration", demo_data['broadband_penetration_pct'],
                unit="percent", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'smart_tv_penetration_pct' in demo_data:
            insert_fact(
                conn, country_entity_id, "smart_tv_penetration", demo_data['smart_tv_penetration_pct'],
                unit="percent", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'paytv_households_million' in demo_data:
            insert_fact(
                conn, country_entity_id, "paytv_households", demo_data['paytv_households_million'],
                unit="million", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        if 'svod_penetration_pct' in demo_data:
            insert_fact(
                conn, country_entity_id, "svod_penetration", demo_data['svod_penetration_pct'],
                unit="percent", observed_at=observed_at, source_id=source_id,
                confidence="high", notes=f"From {demographics_file.name}"
            )
            facts_inserted += 1
        
        countries_loaded += 1
    
    print(f"\nLoaded data for {countries_loaded} European countries")
    print(f"Inserted {facts_inserted} facts")


def generate_summary_report(conn):
    """Generate a summary report of the database"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    # Countries by region
    cursor.execute("""
        SELECT region, COUNT(*) as count, SUM(has_data) as with_data
        FROM countries
        GROUP BY region
        ORDER BY region
    """)
    
    print("\nCountries by Region:")
    for row in cursor.fetchall():
        region, total, with_data = row
        print(f"  {region}: {total} countries ({with_data} with data)")
    
    # Total entities
    cursor.execute("SELECT COUNT(*) FROM entities")
    entity_count = cursor.fetchone()[0]
    print(f"\nTotal entities: {entity_count}")
    
    # Total facts
    cursor.execute("SELECT COUNT(*) FROM facts")
    fact_count = cursor.fetchone()[0]
    print(f"Total facts: {fact_count}")
    
    # Total sources
    cursor.execute("SELECT COUNT(*) FROM sources")
    source_count = cursor.fetchone()[0]
    print(f"Total sources: {source_count}")
    
    # Facts by type
    cursor.execute("""
        SELECT fact_type, COUNT(*) as count
        FROM facts
        GROUP BY fact_type
        ORDER BY count DESC
    """)
    
    print("\nFacts by Type:")
    for row in cursor.fetchall():
        fact_type, count = row
        print(f"  {fact_type}: {count}")


def main():
    base_path = Path(__file__).parent.parent
    db_path = base_path / "broadcast_industry.db"
    
    print("Creating database schema...")
    conn = create_database_schema(str(db_path))
    
    print("Loading countries...")
    load_countries(conn)
    
    print("Loading European data...")
    load_european_data(conn, base_path)
    
    generate_summary_report(conn)
    
    conn.close()
    print(f"\nDatabase created at: {db_path}")


if __name__ == "__main__":
    main()
