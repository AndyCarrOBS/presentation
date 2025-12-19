# Operator Research Workflow Guide

## Overview

A systematic, methodical workflow to research all operator-specific information using:
1. **Existing data** as reference
2. **Web search** for validation and enrichment
3. **Precise source tracking** for every data point

## Workflow Architecture

```
┌─────────────────┐
│  Get Operators  │
│  from Database  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Assess Data    │
│  - Existing     │
│  - Gaps         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Search │
│ Queries         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Research   │
│  - Search APIs  │
│  - Extract Data │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validate Data  │
│  - Cross-ref     │
│  - Confidence   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Store Facts    │
│  - With Sources │
│  - References   │
└─────────────────┘
```

## Step-by-Step Process

### Step 1: Data Assessment

For each operator:
- ✅ Query database for existing facts
- ✅ Identify what data we have
- ✅ Identify what data is missing
- ✅ Prioritize gaps by importance

**Output:** List of operators with data gaps

### Step 2: Research Planning

For each operator and gap:
- ✅ Generate targeted search queries
- ✅ Use operator name + country context
- ✅ Include specific data point in query
- ✅ Add validation queries

**Example:**
```
Operator: KPN (Netherlands)
Gaps: subscribers, hbbtv_version

Queries:
1. "KPN subscribers 2024"
2. "KPN TV subscribers Netherlands"
3. "KPN HbbTV version specifications"
4. "KPN TV operator Netherlands" (validation)
```

### Step 3: Web Research Execution

For each query:
- ✅ Execute via search API (Google, Bing, SerpAPI)
- ✅ Parse search results
- ✅ Extract structured data
- ✅ Rate limit to avoid API limits

**Data Sources:**
- Official operator websites
- Industry reports
- Wikipedia
- News articles
- Technical documentation

### Step 4: Data Extraction

From each search result:
- ✅ Extract subscriber numbers (patterns, formats)
- ✅ Extract HbbTV/CI+ versions
- ✅ Extract CA systems
- ✅ Extract URLs (websites, developer portals)
- ✅ Extract business information (parent company, market share)

**Extraction Methods:**
- Regex patterns
- Structured data parsing
- HTML parsing
- JSON/API responses

### Step 5: Data Validation

- ✅ Cross-reference with existing data
- ✅ Flag discrepancies
- ✅ Calculate confidence scores
- ✅ Document validation status

**Confidence Scoring:**
- **0.9-1.0:** Official source, multiple confirmations
- **0.7-0.9:** Reliable source, single confirmation
- **0.5-0.7:** Unverified, needs review
- **0.0-0.5:** Low confidence

### Step 6: Data Storage

For each extracted fact:
- ✅ Store in database with entity_type='operator'
- ✅ Link to source (web_search type)
- ✅ Add reference URL
- ✅ Record extraction method
- ✅ Set confidence score
- ✅ Add source date

## Source Tracking

Every fact includes:

```json
{
  "fact": {
    "entity_type": "operator",
    "entity_id": "KPN",
    "attribute": "subscribers",
    "value": 2170000,
    "sources": [
      {
        "source_type": "web_search",
        "source_path": "operator_research_workflow",
        "source_name": "Operator research: KPN",
        "source_date": "2024-12-15",
        "confidence_score": 0.8,
        "extraction_method": "web_search"
      }
    ],
    "references": [
      {
        "reference_type": "url",
        "reference_url": "https://example.com/kpn-subscribers",
        "reference_title": "KPN Subscriber Report 2024"
      }
    ]
  }
}
```

## Search API Setup

### Option 1: Google Custom Search API

```bash
# Set environment variables
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CX="your-search-engine-id"

# Get API key: https://developers.google.com/custom-search/v1/overview
# Create search engine: https://programmablesearchengine.google.com/
```

### Option 2: Bing Search API

```bash
export BING_API_KEY="your-api-key"

# Get API key: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
```

### Option 3: SerpAPI

```bash
export SERPAPI_KEY="your-api-key"

# Get API key: https://serpapi.com/
```

### Option 4: DuckDuckGo (No API key needed)

- Free but limited
- HTML scraping required
- Rate limits apply

## Execution

### Run Full Workflow

```bash
# Research all operators
python3 agents/research_data_engineer/operator_research_workflow.py
```

### Run Limited Workflow (Testing)

```bash
# Research first 10 operators
python3 agents/research_data_engineer/operator_research_workflow.py 10
```

### Output Files

- **Database:** `research_data.db` (updated)
- **Results:** `operator_research_results.json`
- **Log:** Console output

## Data Points Researched

### High Priority
1. **Subscriber Numbers** - Current subscriber count
2. **HbbTV Version** - Technical specification
3. **CI+ Version** - Technical specification
4. **CA Systems** - Conditional Access systems

### Medium Priority
5. **Website URL** - Official website
6. **Developer Portal** - Developer resources
7. **Market Share** - Market position
8. **Parent Company** - Ownership information

### Low Priority
9. **Platform Type** - Delivery method
10. **Process Flags** - Test material, gated process, etc.

## Validation Process

### Cross-Reference Check

1. Compare web results with existing database data
2. Flag significant discrepancies (>20% difference)
3. Mark for manual review if confidence < 0.7
4. Update existing data if web source is more recent/authoritative

### Confidence Calculation

```python
confidence = base_confidence * source_quality * recency_factor

base_confidence = 0.7  # Default for web search
source_quality = {
    'official_website': 1.0,
    'industry_report': 0.9,
    'wikipedia': 0.7,
    'news_article': 0.6
}
recency_factor = 1.0 if date < 1 year else 0.8
```

## Workflow Benefits

1. **Systematic:** Covers all operators methodically
2. **Comprehensive:** Identifies and fills all data gaps
3. **Validated:** Cross-references with existing data
4. **Traceable:** Full source tracking for every fact
5. **Repeatable:** Can be run periodically for updates
6. **Scalable:** Handles large numbers of operators

## Best Practices

1. **Rate Limiting:** Add delays between API calls
2. **Error Handling:** Gracefully handle API failures
3. **Data Validation:** Always validate extracted data
4. **Source Quality:** Prefer official sources
5. **Confidence Scoring:** Be conservative with confidence
6. **Manual Review:** Flag low-confidence data for review

## Next Steps

1. ✅ **Workflow created** - Systematic research process
2. ⚠️ **API Integration** - Configure search API keys
3. ⚠️ **Enhance Extraction** - Improve data extraction patterns
4. ⚠️ **Add Validation** - Implement cross-reference validation
5. ⚠️ **Schedule Updates** - Set up periodic re-research

---

**Workflow Version:** 1.0
**Status:** Ready for execution (requires API keys for web search)
