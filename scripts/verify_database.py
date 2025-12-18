#!/usr/bin/env python3
"""Verify database quality and generate summary report"""

import sqlite3
from pathlib import Path

def verify_database(db_path: str):
    """Verify database quality and generate report"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE VERIFICATION REPORT")
    print("=" * 80)
    
    # 1. Countries by region
    print("\n1. COUNTRIES BY REGION:")
    print("-" * 80)
    cursor.execute("""
        SELECT region, COUNT(*) as total, SUM(has_data) as with_data
        FROM countries
        GROUP BY region
        ORDER BY region
    """)
    for row in cursor.fetchall():
        region, total, with_data = row
        print(f"  {region:20s}: {total:3d} countries ({with_data:2d} with data)")
    
    # 2. Data quality checks
    print("\n2. DATA QUALITY CHECKS:")
    print("-" * 80)
    
    # Check for facts without sources
    cursor.execute("SELECT COUNT(*) FROM facts WHERE source_id IS NULL")
    no_source = cursor.fetchone()[0]
    print(f"  Facts without sources: {no_source} (should be 0)")
    
    # Check for facts without retrieved_at
    cursor.execute("SELECT COUNT(*) FROM facts WHERE retrieved_at IS NULL")
    no_retrieved = cursor.fetchone()[0]
    print(f"  Facts without retrieved_at: {no_retrieved} (should be 0)")
    
    # Check for entities without facts
    cursor.execute("""
        SELECT COUNT(*) FROM entities e
        LEFT JOIN facts f ON e.entity_id = f.entity_id
        WHERE f.entity_id IS NULL
    """)
    entities_no_facts = cursor.fetchone()[0]
    print(f"  Entities without facts: {entities_no_facts}")
    
    # Check fact coverage by type
    print("\n3. FACT COVERAGE BY TYPE:")
    print("-" * 80)
    cursor.execute("""
        SELECT fact_type, COUNT(*) as count, COUNT(DISTINCT entity_id) as entities
        FROM facts
        GROUP BY fact_type
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        fact_type, count, entities = row
        print(f"  {fact_type:25s}: {count:3d} facts across {entities:2d} entities")
    
    # 4. Source provenance
    print("\n4. SOURCE PROVENANCE:")
    print("-" * 80)
    cursor.execute("""
        SELECT s.publisher, COUNT(*) as fact_count, 
               MIN(f.retrieved_at) as first_retrieved, 
               MAX(f.retrieved_at) as last_retrieved
        FROM sources s
        JOIN facts f ON s.source_id = f.source_id
        GROUP BY s.source_id, s.publisher
    """)
    for row in cursor.fetchall():
        publisher, fact_count, first, last = row
        print(f"  {publisher:30s}: {fact_count:3d} facts")
        print(f"    Retrieved: {first} to {last}")
    
    # 5. European countries with data
    print("\n5. EUROPEAN COUNTRIES WITH DATA:")
    print("-" * 80)
    cursor.execute("""
        SELECT c.country_name, COUNT(f.fact_id) as fact_count
        FROM countries c
        JOIN entities e ON e.entity_type = 'country' AND e.canonical_name = c.country_name
        JOIN facts f ON f.entity_id = e.entity_id
        WHERE c.region = 'Europe' AND c.has_data = 1
        GROUP BY c.country_name
        ORDER BY fact_count DESC, c.country_name
        LIMIT 10
    """)
    for row in cursor.fetchall():
        country, count = row
        print(f"  {country:30s}: {count:2d} facts")
    
    # 6. Date coverage
    print("\n6. DATE COVERAGE:")
    print("-" * 80)
    cursor.execute("""
        SELECT 
            MIN(observed_at) as earliest_observed,
            MAX(observed_at) as latest_observed,
            MIN(retrieved_at) as earliest_retrieved,
            MAX(retrieved_at) as latest_retrieved
        FROM facts
        WHERE observed_at IS NOT NULL
    """)
    row = cursor.fetchone()
    if row and row[0]:
        print(f"  Observed dates: {row[0]} to {row[1]}")
        print(f"  Retrieved dates: {row[2]} to {row[3]}")
    
    conn.close()
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    verify_database(str(db_path))
