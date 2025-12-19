#!/usr/bin/env python3
"""
Explore and display database contents.
Provides various views of countries, operators, facts, and relationships.
"""

import sqlite3
from pathlib import Path

def connect_db():
    """Connect to the database"""
    db_path = Path(__file__).parent.parent / "broadcast_industry.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(str(db_path))

def format_table(rows, headers, max_width=80):
    """Simple table formatter"""
    if not rows:
        return "No data found"
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            if val:
                col_widths[i] = max(col_widths[i], len(str(val)))
    
    # Limit column widths
    total_width = sum(col_widths) + len(headers) * 3 + 1
    if total_width > max_width:
        scale = max_width / total_width
        col_widths = [int(w * scale) for w in col_widths]
    
    # Build table
    lines = []
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Header
    lines.append(separator)
    header_row = "| " + " | ".join(h[:col_widths[i]].ljust(col_widths[i]) 
                                    for i, h in enumerate(headers)) + " |"
    lines.append(header_row)
    lines.append(separator)
    
    # Data rows
    for row in rows:
        data_row = "| " + " | ".join(str(val)[:col_widths[i]].ljust(col_widths[i]) 
                                      if val else "".ljust(col_widths[i])
                                      for i, val in enumerate(row)) + " |"
        lines.append(data_row)
    
    lines.append(separator)
    return "\n".join(lines)

def show_countries_by_region(conn):
    """Show countries grouped by region"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region, COUNT(*) as total, SUM(has_data) as with_data
        FROM countries
        GROUP BY region
        ORDER BY region
    """)
    
    print("\n" + "=" * 80)
    print("COUNTRIES BY REGION")
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Region", "Total Countries", "With Data"]
    print(format_table(rows, headers))
    
    # Show sample countries from Europe
    print("\n" + "-" * 80)
    print("Sample European Countries (with data):")
    print("-" * 80)
    cursor.execute("""
        SELECT country_name, iso_code, 
               CASE WHEN has_data THEN 'Yes' ELSE 'No' END as has_data
        FROM countries
        WHERE region = 'Europe' AND has_data = 1
        ORDER BY country_name
        LIMIT 10
    """)
    rows = cursor.fetchall()
    headers = ["Country", "ISO Code", "Has Data"]
    print(format_table(rows, headers))

def show_operators_summary(conn):
    """Show operators summary"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            COUNT(oc.country_id) as country_count,
            GROUP_CONCAT(c.country_name, ', ') as countries
        FROM operators o
        LEFT JOIN operator_countries oc ON o.operator_id = oc.operator_id
        LEFT JOIN countries c ON oc.country_id = c.country_id
        GROUP BY o.operator_id, o.canonical_name
        ORDER BY country_count DESC, o.canonical_name
        LIMIT 15
    """)
    
    print("\n" + "=" * 80)
    print("TOP OPERATORS BY COUNTRY COVERAGE")
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Operator", "Countries", "Country List"]
    print(format_table(rows, headers))

def show_countries_with_operators(conn):
    """Show countries with their operators"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.country_name,
            c.region,
            COUNT(oc.operator_id) as operator_count,
            GROUP_CONCAT(o.canonical_name, ', ') as operators
        FROM countries c
        JOIN operator_countries oc ON c.country_id = oc.country_id
        JOIN operators o ON oc.operator_id = o.operator_id
        WHERE c.region = 'Europe'
        GROUP BY c.country_id, c.country_name, c.region
        ORDER BY operator_count DESC, c.country_name
        LIMIT 15
    """)
    
    print("\n" + "=" * 80)
    print("TOP COUNTRIES BY OPERATOR COUNT")
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Country", "Region", "Operator Count", "Operators"]
    print(format_table(rows, headers))

def show_operator_details(conn, operator_name=None):
    """Show detailed information about a specific operator or all operators"""
    cursor = conn.cursor()
    
    if operator_name:
        cursor.execute("""
            SELECT 
                o.canonical_name,
                COALESCE(o.aliases, '') as aliases,
                oc.operator_name_in_country,
                c.country_name,
                c.region
            FROM operators o
            JOIN operator_countries oc ON o.operator_id = oc.operator_id
            JOIN countries c ON oc.country_id = c.country_id
            WHERE o.canonical_name LIKE ?
            ORDER BY c.country_name
        """, (f"%{operator_name}%",))
    else:
        cursor.execute("""
            SELECT 
                o.canonical_name,
                COALESCE(o.aliases, '') as aliases,
                oc.operator_name_in_country,
                c.country_name,
                c.region
            FROM operators o
            JOIN operator_countries oc ON o.operator_id = oc.operator_id
            JOIN countries c ON oc.country_id = c.country_id
            ORDER BY o.canonical_name, c.country_name
            LIMIT 20
        """)
    
    print("\n" + "=" * 80)
    print("OPERATOR DETAILS" + (f" - {operator_name}" if operator_name else ""))
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Canonical Name", "Aliases", "Name in Country", "Country", "Region"]
    print(format_table(rows, headers))

def show_facts_summary(conn):
    """Show facts summary"""
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
    
    print("\n" + "=" * 80)
    print("FACTS SUMMARY")
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Fact Type", "Total Facts", "Entities"]
    print(format_table(rows, headers))
    
    # Show sample facts for a country
    print("\n" + "-" * 80)
    print("Sample Facts for Austria:")
    print("-" * 80)
    cursor.execute("""
        SELECT 
            e.canonical_name,
            f.fact_type,
            f.value_json,
            f.unit,
            f.observed_at
        FROM facts f
        JOIN entities e ON f.entity_id = e.entity_id
        WHERE e.entity_type = 'country' AND e.canonical_name = 'Austria'
        ORDER BY f.fact_type
    """)
    rows = cursor.fetchall()
    headers = ["Entity", "Fact Type", "Value", "Unit", "Observed At"]
    print(format_table(rows, headers))

def show_database_stats(conn):
    """Show overall database statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    # Count countries
    cursor.execute("SELECT COUNT(*) FROM countries")
    stats['countries'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM countries WHERE has_data = 1")
    stats['countries_with_data'] = cursor.fetchone()[0]
    
    # Count operators
    cursor.execute("SELECT COUNT(*) FROM operators")
    stats['operators'] = cursor.fetchone()[0]
    
    # Count relationships
    cursor.execute("SELECT COUNT(*) FROM operator_countries")
    stats['operator_countries'] = cursor.fetchone()[0]
    
    # Count entities
    cursor.execute("SELECT COUNT(*) FROM entities")
    stats['entities'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM entities WHERE entity_type = 'country'")
    stats['country_entities'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM entities WHERE entity_type = 'operator'")
    stats['operator_entities'] = cursor.fetchone()[0]
    
    # Count facts
    cursor.execute("SELECT COUNT(*) FROM facts")
    stats['facts'] = cursor.fetchone()[0]
    
    # Count sources
    cursor.execute("SELECT COUNT(*) FROM sources")
    stats['sources'] = cursor.fetchone()[0]
    
    print("\n" + "=" * 80)
    print("DATABASE STATISTICS")
    print("=" * 80)
    
    rows = [
        ["Countries (total)", stats['countries']],
        ["Countries (with data)", stats['countries_with_data']],
        ["Operators", stats['operators']],
        ["Operator-Country Relationships", stats['operator_countries']],
        ["Entities (total)", stats['entities']],
        ["Entities (countries)", stats['country_entities']],
        ["Entities (operators)", stats['operator_entities']],
        ["Facts", stats['facts']],
        ["Sources", stats['sources']],
    ]
    
    headers = ["Metric", "Count"]
    print(format_table(rows, headers))

def show_multi_country_operators(conn):
    """Show operators that operate in multiple countries"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.canonical_name,
            COALESCE(o.aliases, '') as aliases,
            COUNT(oc.country_id) as country_count,
            GROUP_CONCAT(c.country_name || ' (' || COALESCE(oc.operator_name_in_country, '') || ')', ', ') as countries_with_names
        FROM operators o
        JOIN operator_countries oc ON o.operator_id = oc.operator_id
        JOIN countries c ON oc.country_id = c.country_id
        GROUP BY o.operator_id, o.canonical_name, o.aliases
        HAVING country_count > 1
        ORDER BY country_count DESC, o.canonical_name
    """)
    
    print("\n" + "=" * 80)
    print("MULTI-COUNTRY OPERATORS")
    print("=" * 80)
    
    rows = cursor.fetchall()
    headers = ["Operator", "Aliases", "Countries", "Countries (with local names)"]
    print(format_table(rows, headers))

def interactive_menu():
    """Interactive menu for exploring database"""
    conn = connect_db()
    if not conn:
        return
    
    while True:
        print("\n" + "=" * 80)
        print("DATABASE EXPLORER")
        print("=" * 80)
        print("1. Database Statistics")
        print("2. Countries by Region")
        print("3. Top Operators by Country Coverage")
        print("4. Top Countries by Operator Count")
        print("5. Multi-Country Operators")
        print("6. Operator Details (all)")
        print("7. Facts Summary")
        print("8. Search Operator")
        print("9. Show All")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            show_database_stats(conn)
        elif choice == "2":
            show_countries_by_region(conn)
        elif choice == "3":
            show_operators_summary(conn)
        elif choice == "4":
            show_countries_with_operators(conn)
        elif choice == "5":
            show_multi_country_operators(conn)
        elif choice == "6":
            show_operator_details(conn)
        elif choice == "7":
            show_facts_summary(conn)
        elif choice == "8":
            operator_name = input("Enter operator name to search: ").strip()
            show_operator_details(conn, operator_name)
        elif choice == "9":
            show_database_stats(conn)
            show_countries_by_region(conn)
            show_operators_summary(conn)
            show_countries_with_operators(conn)
            show_multi_country_operators(conn)
            show_facts_summary(conn)
        else:
            print("Invalid choice")
    
    conn.close()

def main():
    """Main function - show all or interactive menu"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Show everything
        conn = connect_db()
        if conn:
            show_database_stats(conn)
            show_countries_by_region(conn)
            show_operators_summary(conn)
            show_countries_with_operators(conn)
            show_multi_country_operators(conn)
            show_facts_summary(conn)
            conn.close()
    else:
        # Interactive menu
        interactive_menu()

if __name__ == "__main__":
    main()
