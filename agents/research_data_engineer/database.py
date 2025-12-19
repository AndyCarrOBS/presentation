#!/usr/bin/env python3
"""
Database schema and management for the Research Data Engineer Agent
Stores facts with source tracking, references, and temporal data for trend analysis
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import contextmanager


class ResearchDatabase:
    """Manages the structured database for research facts and data points"""
    
    def __init__(self, db_path: str = "research_data.db"):
        """Initialize the database connection"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database schema if it doesn't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Facts table - core data points
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,  -- e.g., 'country', 'operator', 'specification'
                    entity_id TEXT NOT NULL,     -- e.g., 'Austria', 'ORF', 'hbbtv_version'
                    attribute TEXT NOT NULL,     -- e.g., 'population', 'hbbtv_version', 'has_specification'
                    value TEXT,                  -- The actual value (stored as text, can be JSON)
                    value_type TEXT,             -- 'string', 'number', 'boolean', 'json', 'date'
                    unit TEXT,                   -- e.g., 'million', 'percent', 'version'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_current BOOLEAN DEFAULT 1  -- For versioning/historical data
                )
            """)
            
            # Sources table - tracks where data came from
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_type TEXT NOT NULL,  -- 'file', 'url', 'api', 'manual', 'web_search'
                    source_path TEXT,            -- File path or URL
                    source_name TEXT,            -- Human-readable name
                    source_date DATE,            -- When the source was accessed/created
                    source_metadata TEXT,        -- JSON metadata about the source
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(source_type, source_path, source_date)
                )
            """)
            
            # Fact-Source relationships - links facts to their sources
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fact_sources (
                    fact_id INTEGER NOT NULL,
                    source_id INTEGER NOT NULL,
                    confidence_score REAL DEFAULT 1.0,  -- 0.0 to 1.0
                    extraction_method TEXT,             -- How the fact was extracted
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (fact_id, source_id),
                    FOREIGN KEY (fact_id) REFERENCES facts(id),
                    FOREIGN KEY (source_id) REFERENCES sources(id)
                )
            """)
            
            # References table - external citations and links
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fact_references (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact_id INTEGER NOT NULL,
                    reference_type TEXT NOT NULL,  -- 'url', 'document', 'publication', 'api'
                    reference_url TEXT,
                    reference_title TEXT,
                    reference_date DATE,
                    reference_metadata TEXT,  -- JSON
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (fact_id) REFERENCES facts(id)
                )
            """)
            
            # External data points - data fetched from external sources
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS external_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact_id INTEGER NOT NULL,
                    external_source TEXT NOT NULL,  -- e.g., 'worldbank', 'statista', 'wikipedia'
                    external_id TEXT,               -- ID in external system
                    external_url TEXT,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_snapshot TEXT,             -- JSON snapshot of external data
                    FOREIGN KEY (fact_id) REFERENCES facts(id)
                )
            """)
            
            # Data quality metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_quality (
                    fact_id INTEGER NOT NULL,
                    completeness_score REAL,        -- 0.0 to 1.0
                    accuracy_score REAL,            -- 0.0 to 1.0
                    freshness_score REAL,           -- 0.0 to 1.0
                    source_count INTEGER DEFAULT 0,
                    last_verified_at TIMESTAMP,
                    verification_status TEXT,       -- 'verified', 'unverified', 'disputed'
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (fact_id) REFERENCES facts(id)
                )
            """)
            
            # Indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_entity ON facts(entity_type, entity_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_attribute ON facts(attribute)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_created ON facts(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_sources_fact ON fact_sources(fact_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_sources_source ON fact_sources(source_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_references_fact ON fact_references(fact_id)")
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def add_source(self, source_type: str, source_path: str, 
                   source_name: str = None, source_date: str = None,
                   metadata: Dict = None) -> int:
        """Add a new source and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO sources 
                (source_type, source_path, source_name, source_date, source_metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (source_type, source_path, source_name or source_path, 
                  source_date or datetime.now().date().isoformat(),
                  json.dumps(metadata or {})))
            conn.commit()
            
            # Get the ID
            cursor.execute("""
                SELECT id FROM sources 
                WHERE source_type = ? AND source_path = ? AND source_date = ?
            """, (source_type, source_path, source_date or datetime.now().date().isoformat()))
            result = cursor.fetchone()
            return result['id'] if result else None
    
    def add_fact(self, entity_type: str, entity_id: str, attribute: str,
                 value: Any, value_type: str = None, unit: str = None,
                 source_id: int = None, confidence: float = 1.0,
                 extraction_method: str = None) -> int:
        """Add a fact and optionally link it to a source"""
        # Determine value type if not provided
        if value_type is None:
            if isinstance(value, bool):
                value_type = 'boolean'
            elif isinstance(value, (int, float)):
                value_type = 'number'
            elif isinstance(value, (dict, list)):
                value_type = 'json'
                value = json.dumps(value)
            else:
                value_type = 'string'
                value = str(value)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if fact already exists with same value (avoid duplicates)
            cursor.execute("""
                SELECT id FROM facts 
                WHERE entity_type = ? AND entity_id = ? AND attribute = ? 
                AND value = ? AND is_current = 1
            """, (entity_type, entity_id, attribute, str(value)))
            existing = cursor.fetchone()
            
            if existing:
                # Fact already exists, return existing ID
                return existing['id']
            
            # Mark old facts as not current
            cursor.execute("""
                UPDATE facts 
                SET is_current = 0, updated_at = CURRENT_TIMESTAMP
                WHERE entity_type = ? AND entity_id = ? AND attribute = ? AND is_current = 1
            """, (entity_type, entity_id, attribute))
            
            # Insert new fact (remove created_at from UNIQUE constraint by using a small delay)
            import time
            time.sleep(0.001)  # Small delay to ensure different timestamp
            
            cursor.execute("""
                INSERT INTO facts 
                (entity_type, entity_id, attribute, value, value_type, unit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (entity_type, entity_id, attribute, str(value), value_type, unit))
            
            fact_id = cursor.lastrowid
            
            # Link to source if provided
            if source_id:
                cursor.execute("""
                    INSERT INTO fact_sources (fact_id, source_id, confidence_score, extraction_method)
                    VALUES (?, ?, ?, ?)
                """, (fact_id, source_id, confidence, extraction_method))
            
            conn.commit()
            return fact_id
    
    def add_reference(self, fact_id: int, reference_type: str, 
                     reference_url: str = None, reference_title: str = None,
                     reference_date: str = None, metadata: Dict = None):
        """Add a reference/citation for a fact"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fact_references 
                (fact_id, reference_type, reference_url, reference_title, 
                 reference_date, reference_metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fact_id, reference_type, reference_url, reference_title,
                  reference_date, json.dumps(metadata or {})))
            conn.commit()
    
    def add_external_data(self, fact_id: int, external_source: str,
                         external_id: str = None, external_url: str = None,
                         data_snapshot: Dict = None):
        """Add external data point linked to a fact"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO external_data 
                (fact_id, external_source, external_id, external_url, data_snapshot)
                VALUES (?, ?, ?, ?, ?)
            """, (fact_id, external_source, external_id, external_url,
                  json.dumps(data_snapshot or {})))
            conn.commit()
    
    def get_facts(self, entity_type: str = None, entity_id: str = None,
                  attribute: str = None, current_only: bool = True) -> List[Dict]:
        """Query facts with optional filters"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM facts WHERE 1=1"
            params = []
            
            if entity_type:
                query += " AND entity_type = ?"
                params.append(entity_type)
            if entity_id:
                query += " AND entity_id = ?"
                params.append(entity_id)
            if attribute:
                query += " AND attribute = ?"
                params.append(attribute)
            if current_only:
                query += " AND is_current = 1"
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_fact_with_sources(self, fact_id: int) -> Dict:
        """Get a fact with all its sources and references"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Get fact
            cursor.execute("SELECT * FROM facts WHERE id = ?", (fact_id,))
            fact = dict(cursor.fetchone()) if cursor.rowcount > 0 else None
            
            if not fact:
                return None
            
            # Get sources
            cursor.execute("""
                SELECT s.*, fs.confidence_score, fs.extraction_method
                FROM sources s
                JOIN fact_sources fs ON s.id = fs.source_id
                WHERE fs.fact_id = ?
            """, (fact_id,))
            fact['sources'] = [dict(row) for row in cursor.fetchall()]
            
            # Get references
            cursor.execute("SELECT * FROM fact_references WHERE fact_id = ?", (fact_id,))
            fact['references'] = [dict(row) for row in cursor.fetchall()]
            
            # Get external data
            cursor.execute("SELECT * FROM external_data WHERE fact_id = ?", (fact_id,))
            fact['external_data'] = [dict(row) for row in cursor.fetchall()]
            
            return fact
    
    def get_trend_data(self, entity_type: str, entity_id: str, attribute: str) -> List[Dict]:
        """Get historical data for trend analysis"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.*, s.source_date, s.source_name
                FROM facts f
                LEFT JOIN fact_sources fs ON f.id = fs.fact_id
                LEFT JOIN sources s ON fs.source_id = s.id
                WHERE f.entity_type = ? AND f.entity_id = ? AND f.attribute = ?
                ORDER BY f.created_at ASC
            """, (entity_type, entity_id, attribute))
            return [dict(row) for row in cursor.fetchall()]
