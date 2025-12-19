# OpenAI-Powered Research Workflow Setup

## ✅ Updated to Use OpenAI API

The operator research workflow has been updated to use OpenAI API for intelligent data extraction instead of Google Search.

## Setup

### API Key Configuration

The OpenAI API key has been configured. You can set it via:

```bash
# Option 1: Environment variable (recommended)
export OPENAI_API_KEY="your-openai-api-key-here"

# Option 2: Pass as command line argument
python3 agents/research_data_engineer/operator_research_workflow.py 10 "sk-proj-..."
```

## How It Works

### 1. URL Discovery (DuckDuckGo)
- Uses free DuckDuckGo API to find relevant URLs
- No API key required
- Fetches web page content

### 2. Intelligent Extraction (OpenAI)
- Uses OpenAI GPT-4o-mini to extract structured data
- Extracts from web content intelligently
- Handles various formats and phrasings
- Returns structured JSON

### 3. Data Storage
- Stores extracted data with source tracking
- Records extraction method as "openai_extraction"
- Sets confidence scores based on source quality

## Benefits of OpenAI Approach

1. **Intelligent Extraction:** Understands context and various phrasings
2. **Structured Output:** Returns clean, structured JSON
3. **Cost Efficient:** Uses GPT-4o-mini for lower costs
4. **No Search API Needed:** Uses free DuckDuckGo for URL discovery
5. **Better Accuracy:** AI understands context better than regex

## Execution

```bash
# Set API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Run workflow
python3 agents/research_data_engineer/operator_research_workflow.py

# Or with limit
python3 agents/research_data_engineer/operator_research_workflow.py 10
```

## Data Extraction

OpenAI extracts:
- Subscriber numbers (converts "2.1 million" → 2100000)
- HbbTV/CI+ versions (extracts version numbers)
- CA systems (extracts system names)
- URLs (extracts full URLs)
- Business information (parent company, market share)

## Cost Considerations

- **Model:** GPT-4o-mini (cost-efficient)
- **Usage:** ~1-2 API calls per operator
- **Estimated cost:** ~$0.01-0.02 per operator
- **For 106 operators:** ~$1-2 total

## Files Updated

1. `web_researcher.py` - Added OpenAI integration
2. `extract_with_openai.py` - New OpenAI extraction module
3. `operator_research_workflow.py` - Updated to use OpenAI

---

**Status:** ✅ Ready with OpenAI API
**API Key:** Configured
**Model:** GPT-4o-mini
