# Operator Research Workflow

## Overview

A systematic workflow to research all operator-specific information using existing data as reference, web search for validation/enrichment, and precise source tracking.

## Workflow Steps

### 1. Data Assessment
- ✅ Get all operators from database
- ✅ Identify existing data for each operator
- ✅ Identify data gaps

### 2. Research Planning
- ✅ Generate targeted search queries for missing data
- ✅ Prioritize high-value data points
- ✅ Use existing data as context

### 3. Web Research
- ✅ Execute search queries
- ✅ Extract structured data from results
- ✅ Validate against existing data

### 4. Data Storage
- ✅ Store new facts with source tracking
- ✅ Add references (URLs, documents)
- ✅ Record extraction methods and confidence scores

### 5. Validation
- ✅ Compare web results with existing data
- ✅ Flag discrepancies for review
- ✅ Update confidence scores

## Data Points Researched

### Operator-Specific Data

1. **Subscriber Numbers**
   - Current subscriber count
   - Historical trends
   - Market position

2. **Technical Specifications**
   - HbbTV version
   - CI+ version
   - Conditional Access systems

3. **Business Information**
   - Website URL
   - Developer portal
   - Parent company
   - Market share

4. **Process Information**
   - Specification availability
   - Test material availability
   - Gated process requirements
   - Whitelist systems
   - Branding agreements

## Search Query Strategy

### Query Generation

For each operator and gap, generate specific queries:

```
Operator: KPN
Gaps: subscribers, hbbtv_version, website

Queries:
1. "KPN subscribers 2024"
2. "KPN TV subscribers number"
3. "KPN HbbTV version specifications"
4. "KPN official website"
5. "KPN TV operator" (general validation)
```

### Query Prioritization

1. **High Priority:** Subscriber numbers, technical specs
2. **Medium Priority:** Business information, market share
3. **Low Priority:** Process flags, additional details

## Source Tracking

Every fact includes:

- **Source Type:** web_search, file, api, manual
- **Source URL:** Direct link to source document
- **Source Title:** Human-readable source name
- **Source Date:** When data was collected
- **Extraction Method:** How data was extracted
- **Confidence Score:** 0.0 to 1.0 data quality indicator
- **References:** External citations and links

## Data Validation

### Validation Process

1. **Cross-reference** web results with existing data
2. **Flag discrepancies** for manual review
3. **Update confidence scores** based on source quality
4. **Document validation** in fact metadata

### Confidence Scoring

- **0.9-1.0:** Official source, multiple confirmations
- **0.7-0.9:** Reliable source, single confirmation
- **0.5-0.7:** Unverified source, needs validation
- **0.0-0.5:** Low confidence, requires review

## Execution

### Run Workflow

```bash
# Research all operators
python3 agents/research_data_engineer/operator_research_workflow.py

# Research first 10 operators (for testing)
python3 agents/research_data_engineer/operator_research_workflow.py 10
```

### Output

- **Database:** Updated with new facts and sources
- **Results JSON:** `operator_research_results.json`
- **Log:** Console output with progress

## Integration with Web Search APIs

### Required Setup

The workflow is designed to integrate with web search APIs:

1. **Google Custom Search API**
2. **Bing Search API**
3. **DuckDuckGo API**
4. **SerpAPI**

### API Integration Example

```python
# In web_researcher.py
def search(self, query: str, max_results: int = 5) -> List[Dict]:
    # Call actual search API
    response = requests.get(
        'https://www.googleapis.com/customsearch/v1',
        params={
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': query,
            'num': max_results
        }
    )
    # Parse and return results
    return parse_search_results(response.json())
```

## Workflow Benefits

1. **Systematic:** Covers all operators methodically
2. **Comprehensive:** Identifies and fills all data gaps
3. **Validated:** Cross-references with existing data
4. **Traceable:** Full source tracking for every fact
5. **Repeatable:** Can be run periodically for updates

## Next Steps

1. **Integrate web search API** (Google, Bing, etc.)
2. **Enhance extraction patterns** for better data capture
3. **Add validation logic** for data quality checks
4. **Schedule periodic updates** for data freshness
5. **Generate reports** on data completeness

---

**Workflow Version:** 1.0
**Last Updated:** 2024-12-15
