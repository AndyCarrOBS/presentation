# Operator Research Workflow - README

## ✅ Workflow Created

A systematic, methodical workflow to research all operator-specific information has been created.

## Overview

The workflow:
1. **Uses existing data** as reference
2. **Performs web search** to validate and enrich data
3. **Stores all data** with precise source tracking

## Workflow Process

```
For each operator:
  1. Assess existing data from database
  2. Identify data gaps
  3. Generate targeted search queries
  4. Execute web research (file + web)
  5. Extract structured data
  6. Validate against existing data
  7. Store with precise source tracking
```

## Key Features

### ✅ Data Assessment
- Identifies existing operator data
- Identifies missing data points
- Prioritizes gaps

### ✅ Research Planning
- Generates targeted search queries
- Uses operator + country context
- Creates specific queries for each gap

### ✅ Web Research
- Extracts from existing files first
- Falls back to web search APIs
- Supports multiple search APIs

### ✅ Data Extraction
- Subscriber numbers
- HbbTV/CI+ versions
- CA systems
- URLs and business information

### ✅ Source Tracking
- Every fact linked to source
- Source URL, title, date
- Extraction method
- Confidence score
- References

## Execution

### Basic Usage

```bash
# Research all operators
python3 agents/research_data_engineer/operator_research_workflow.py

# Research first 10 (testing)
python3 agents/research_data_engineer/operator_research_workflow.py 10
```

### With Web Search API (Optional)

```bash
# Configure API (choose one):
export GOOGLE_API_KEY="your-key"
export GOOGLE_CX="your-search-engine-id"

# OR
export BING_API_KEY="your-key"

# OR
export SERPAPI_KEY="your-key"

# Then run workflow
python3 agents/research_data_engineer/operator_research_workflow.py
```

## Output

- **Database:** Updated with new facts
- **Results JSON:** `operator_research_results.json`
- **Console:** Progress and statistics

## Current Status

✅ **Workflow created and functional**
✅ **File-based extraction working**
✅ **Source tracking implemented**
⚠️ **Web search requires API keys** (currently uses DuckDuckGo fallback)

## Documentation

- `RESEARCH_WORKFLOW.md` - Complete workflow documentation
- `workflow_guide.md` - Step-by-step guide
- `WORKFLOW_EXECUTION_GUIDE.md` - Execution instructions

---

**Status:** ✅ Ready for execution
**Version:** 1.0
