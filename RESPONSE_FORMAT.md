# Agent Response Format - Natural Language + Citations

## What Changed:

The agent now provides **BOTH** natural language advice **AND** raw cited data from the vector database.

## New Response Structure:

```
[Natural Conversational Part]
I need to give you some important advice about Chennai...

According to the Chennai District Report 2023, the situation is...
[Explanation of what the data means]
[Actionable recommendations]

---

📊 Retrieved Data from Reports:

Source: Chennai_District_Report_2023.pdf, Page 12
- Groundwater Extraction: 85.3%
- Water Level Depth: 12.4 meters below ground level
- Classification: Semi-Critical
- Recharge Rate: 245 MCM/year
- Annual Extraction: 209 MCM/year
- Stage of Development: 85.3%
```

## What the Agent Will Include:

### 1. Natural Language (Existing):
- ✅ Conversational tone
- ✅ Explanations of what data means
- ✅ Practical advice
- ✅ Risk assessments
- ✅ Recommendations

### 2. Raw Data Section (NEW):
- ✅ Exact water levels from PDFs
- ✅ Extraction percentages
- ✅ Recharge rates
- ✅ Classifications
- ✅ Document names
- ✅ Page numbers
- ✅ All numerical data found in vector database

## Files Modified:

1. **backend/prompts.py**: Updated agent system prompt with mandatory data section
2. **backend/retriever.py**: Enhanced context formatting with emojis and structure
3. **test_citation_format.py**: Test script to verify the format

## How It Works:

1. Agent searches vector database for relevant documents
2. Receives FULL context from retrieval (water levels, percentages, sources)
3. Generates natural language response explaining the data
4. Appends "📊 Retrieved Data from Reports" section with raw citations
5. User gets both easy-to-understand advice AND verifiable source data
