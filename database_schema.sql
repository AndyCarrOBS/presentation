-- Broadcast Industry Database Schema
-- Following data engineer rules: full provenance, date semantics, structured entities/facts
-- Created: 2025-01-27

-- Sources table - tracks all data sources with full provenance
CREATE TABLE IF NOT EXISTS sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    publisher TEXT,
    published_at DATE,
    retrieved_at DATE NOT NULL,
    license_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entities table - countries, operators, broadcasters, etc.
-- Entities must have canonical names and aliases
CREATE TABLE IF NOT EXISTS entities (
    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    canonical_name TEXT NOT NULL,
    aliases TEXT,
    external_ids TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_type, canonical_name)
);

-- Facts table - all facts about entities with full provenance
-- Every fact includes: observed_at, published_at, retrieved_at
-- Never overwrites facts silently - uses versioning with valid_from/valid_to
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
);

-- Countries table - comprehensive list with regions
CREATE TABLE IF NOT EXISTS countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE,
    iso_code TEXT,
    region TEXT NOT NULL,
    subregion TEXT,
    has_data BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_entities_type_name ON entities(entity_type, canonical_name);
CREATE INDEX IF NOT EXISTS idx_facts_entity ON facts(entity_id);
CREATE INDEX IF NOT EXISTS idx_facts_type ON facts(fact_type);
CREATE INDEX IF NOT EXISTS idx_facts_observed ON facts(observed_at);
CREATE INDEX IF NOT EXISTS idx_countries_region ON countries(region);
CREATE INDEX IF NOT EXISTS idx_countries_iso ON countries(iso_code);

-- Dashboard-friendly views

-- Latest snapshot view for countries
CREATE VIEW IF NOT EXISTS v_countries_latest AS
SELECT 
    c.country_id,
    c.country_name,
    c.iso_code,
    c.region,
    c.has_data,
    e.entity_id
FROM countries c
LEFT JOIN entities e ON e.entity_type = 'country' AND e.canonical_name = c.country_name;

-- Latest facts view (most recent observed_at for each fact type per entity)
CREATE VIEW IF NOT EXISTS v_facts_latest AS
SELECT 
    f.fact_id,
    f.entity_id,
    e.canonical_name as entity_name,
    e.entity_type,
    f.fact_type,
    f.value_json,
    f.unit,
    f.observed_at,
    f.published_at,
    f.retrieved_at,
    s.publisher as source_publisher,
    s.url as source_url,
    f.confidence,
    f.notes
FROM facts f
JOIN entities e ON f.entity_id = e.entity_id
JOIN sources s ON f.source_id = s.source_id
WHERE f.fact_id IN (
    SELECT MAX(f2.fact_id)
    FROM facts f2
    WHERE f2.entity_id = f.entity_id 
    AND f2.fact_type = f.fact_type
    GROUP BY f2.entity_id, f2.fact_type
);

-- Time-series trend view for facts
CREATE VIEW IF NOT EXISTS v_facts_timeseries AS
SELECT 
    f.fact_id,
    f.entity_id,
    e.canonical_name as entity_name,
    e.entity_type,
    f.fact_type,
    f.value_json,
    f.unit,
    f.observed_at,
    f.published_at,
    f.retrieved_at,
    s.publisher as source_publisher,
    f.confidence
FROM facts f
JOIN entities e ON f.entity_id = e.entity_id
JOIN sources s ON f.source_id = s.source_id
ORDER BY f.entity_id, f.fact_type, f.observed_at DESC;

-- Countries with facts summary
CREATE VIEW IF NOT EXISTS v_countries_with_facts AS
SELECT 
    c.country_id,
    c.country_name,
    c.iso_code,
    c.region,
    COUNT(DISTINCT f.fact_type) as fact_types_count,
    COUNT(f.fact_id) as total_facts,
    MAX(f.retrieved_at) as last_updated
FROM countries c
LEFT JOIN entities e ON e.entity_type = 'country' AND e.canonical_name = c.country_name
LEFT JOIN facts f ON f.entity_id = e.entity_id
GROUP BY c.country_id, c.country_name, c.iso_code, c.region;

-- Operators table - canonical operator entities
CREATE TABLE IF NOT EXISTS operators (
    operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_name TEXT NOT NULL UNIQUE,
    aliases TEXT,
    parent_company TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operator-Country junction table (many-to-many relationship)
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
);

-- Indexes for operators
CREATE INDEX IF NOT EXISTS idx_operators_name ON operators(canonical_name);
CREATE INDEX IF NOT EXISTS idx_operator_countries_op ON operator_countries(operator_id);
CREATE INDEX IF NOT EXISTS idx_operator_countries_country ON operator_countries(country_id);

-- Dashboard views for operators

-- Operators with country count
CREATE VIEW IF NOT EXISTS v_operators_summary AS
SELECT 
    o.operator_id,
    o.canonical_name,
    o.aliases,
    o.parent_company,
    COUNT(oc.country_id) as country_count,
    GROUP_CONCAT(c.country_name, ', ') as countries
FROM operators o
LEFT JOIN operator_countries oc ON o.operator_id = oc.operator_id
LEFT JOIN countries c ON oc.country_id = c.country_id
GROUP BY o.operator_id, o.canonical_name, o.aliases, o.parent_company
ORDER BY country_count DESC, o.canonical_name;

-- Countries with operator count
CREATE VIEW IF NOT EXISTS v_countries_operators AS
SELECT 
    c.country_id,
    c.country_name,
    c.region,
    COUNT(oc.operator_id) as operator_count,
    GROUP_CONCAT(o.canonical_name, ', ') as operators
FROM countries c
LEFT JOIN operator_countries oc ON c.country_id = oc.country_id
LEFT JOIN operators o ON oc.operator_id = o.operator_id
GROUP BY c.country_id, c.country_name, c.region
ORDER BY c.region, operator_count DESC, c.country_name;
