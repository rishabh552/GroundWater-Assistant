# Test & Debug Scripts

This folder contains test scripts and debugging utilities for Jal-Rakshak development.

## Test Scripts

### Core Component Tests

**`test_llm.py`** - LLM Model Testing
```bash
python tests/test_llm.py
```
Tests Granite model loading and basic text generation.

**`test_rag_usage.py`** - RAG System Testing
```bash
python tests/test_rag_usage.py
```
Verifies that the agent uses RAG and searches the knowledge base.

**`test_citation_format.py`** - Citation Format Testing
```bash
python tests/test_citation_format.py
```
Checks that responses include both natural language and data citations.

**`test_pdf_generation.py`** - PDF Report Testing
```bash
python tests/test_pdf_generation.py
```
Validates PDF report generation functionality.

**`test_all_imports.py`** - Import Verification
```bash
python tests/test_all_imports.py
```
Quick check for missing dependencies.

**`test_st.py`** - Environment Check
```bash
python tests/test_st.py
```
Verifies sentence-transformers and torch installation.

## Debug Utilities

**`debug_retrieval.py`** - Search Debugging
```bash
python tests/debug_retrieval.py
```
Debug vector search and retrieval quality.

**`verify_agent.py`** - Agent Verification
```bash
python tests/verify_agent.py
```
Test the ReAct agent loop with sample queries.

**`update_map_risks.py`** - Map Data Generator
```bash
python tests/update_map_risks.py
```
Update `generated_map_data.json` with district risk levels.

## Running All Tests

```bash
# Run from project root
cd C:\project\1m1b\jal-rakshak

# Individual tests
python tests/test_llm.py
python tests/test_rag_usage.py
python tests/test_citation_format.py
python tests/test_pdf_generation.py
python tests/verify_agent.py
```

## Test Requirements

All tests require:
- Virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- Vector store indexed: `python ingest.py` (for retrieval tests)
- Model downloaded (happens automatically on first run)

## Expected Outputs

### ✅ Success Indicators
- `test_llm.py`: Model loads and generates text
- `test_rag_usage.py`: Agent searches knowledge base
- `test_citation_format.py`: Response has 📊 data section
- `test_pdf_generation.py`: PDF file created with correct header
- `verify_agent.py`: Agent completes reasoning loop

### ❌ Common Issues
- "Vectorstore not found": Run `python ingest.py`
- "Module not found": Run `pip install -r requirements.txt`
- "CUDA errors": Use CPU-only torch or install CUDA toolkit

## Development Workflow

1. Make changes to core code
2. Run relevant tests to verify
3. Fix any failing tests
4. Run full test suite before committing

## Notes

- Tests are optional for production deployment
- Keep for active development and debugging
- Some tests may take time due to model loading
- GPU acceleration recommended for faster execution
