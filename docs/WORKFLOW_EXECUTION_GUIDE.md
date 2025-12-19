# Operator Research Workflow - Execution Guide

## ✅ Workflow Created

A systematic workflow has been created to methodically research all operator-specific information.

## Workflow Process

### Step 1: Data Assessment
- ✅ Get all operators from database
- ✅ Identify existing data for each operator
- ✅ Identify data gaps systematically

### Step 2: Research Planning
- ✅ Generate targeted search queries for missing data
- ✅ Use operator name + country context
- ✅ Prioritize high-value data points

### Step 3: Web Research
- ✅ Execute search queries via APIs
- ✅ Extract structured data from results
- ✅ Validate against existing data

### Step 4: Data Storage
- ✅ Store new facts with precise source tracking
- ✅ Add references (URLs, documents)
- ✅ Record extraction methods and confidence scores

## Current Implementation

### ✅ Completed
- Workflow structure and logic
- Data gap identification
- Query generation
- Data extraction patterns
- Source tracking system
- File-based extraction (from existing markdown files)

### ⚠️ Requires Configuration
- **Web Search API Integration**
  - Currently uses file extraction + DuckDuckGo fallback
  - For full functionality, configure one of:
    - Google Custom Search API
    - Bing Search API
    - SerpAPI

## How to Use

### 1. Setup (Optional - for web search)

```bash
# Option 1: Google Custom Search API
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CX="your-search-engine-id"

# Option 2: Bing Search API
export BING_API_KEY="your-api-key"

# Option 3: SerpAPI
export SERPAPI_KEY="your-api-key"
```

### 2. Run Workflow

```bash
# Research all operators
python3 agents/research_data_engineer/operator_research_workflow.py

# Research first 10 operators (for testing)
python3 agents/research_data_engineer/operator_research_workflow.py 10
```

### 3. Review Results

- **Database:** Updated with new facts
- **Results JSON:** `operator_research_results.json`
- **Console:** Progress and statistics

## Data Points Researched

### For Each Operator:
1. **Subscriber Numbers** - Current subscriber count
2. **HbbTV Version** - Technical specification version
3. **CI+ Version** - CI Plus specification version
4. **CA Systems** - Conditional Access systems used
5. **Website URL** - Official website
6. **Developer Portal** - Developer resources URL
7. **Market Share** - Percentage of pay-TV market
8. **Parent Company** - Ownership information
9. **Platform Type** - Delivery method (IPTV, Cable, Satellite)
10. **Process Flags** - Test material, gated process, whitelist, branding

## Source Tracking

Every fact includes:
- **Source Type:** web_search, file, api
- **Source URL:** Direct link to source document
- **Source Title:** Human-readable source name
- **Source Date:** When data was collected
- **Extraction Method:** How data was extracted
- **Confidence Score:** 0.0-1.0 data quality indicator
- **References:** External citations and links

## Workflow Benefits

1. **Systematic:** Covers all operators methodically
2. **Comprehensive:** Identifies and fills all data gaps
3. **Validated:** Cross-references with existing data
4. **Traceable:** Full source tracking for every fact
5. **Repeatable:** Can be run periodically for updates
6. **Scalable:** Handles large numbers of operators

## Current Status

✅ **Workflow created and functional**
✅ **File-based extraction working**
✅ **Source tracking implemented**
⚠️ **Web search requires API keys** (currently uses DuckDuckGo fallback)

## Next Steps

1. **Configure search API** (optional but recommended)
2. **Run workflow** on all operators
3. **Review and validate** extracted data
4. **Update master JSON** with new data
5. **Schedule periodic updates** for data freshness

---

**Workflow Version:** 1.0
**Status:** ✅ Ready for execution
**Created:** 2024-12-15
