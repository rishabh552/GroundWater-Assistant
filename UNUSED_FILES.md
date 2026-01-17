# Project Organization

## ✅ Test Files Organized

All test and debug scripts have been moved to the `tests/` directory for better organization.

### Test/Debug Scripts (Located in `tests/`)
- `tests/test_all_imports.py` - Simple import test
- `tests/test_st.py` - Streamlit/torch version check
- `tests/test_rag_usage.py` - RAG testing script
- `tests/test_citation_format.py` - Citation format testing
- `tests/test_pdf_generation.py` - PDF generation testing
- `tests/debug_retrieval.py` - Retrieval debugging script
- `tests/verify_agent.py` - Agent verification script
- `tests/update_map_risks.py` - Map data generator
- `tests/test_llm.py` - LLM test wrapper (renamed from `llm.py`)

### Documentation Files (Keep)
- `RESPONSE_FORMAT.md` - ✅ Keep - Documents response format
- `README.md` - ✅ Keep - Main documentation

### Core Files (Do Not Remove)
- `app.py` - ✅ Streamlit application
- `ingest.py` - ✅ PDF ingestion CLI
- `requirements.txt` - ✅ Python dependencies
- `generated_map_data.json` - ✅ Map risk data
- `backend/**/*.py` - ✅ All core backend modules
- `api/**/*.py` - ✅ All FastAPI routes
- `web/**/*` - ✅ Next.js frontend
- `data/` - ✅ Data directory
- `vectorstore/` - ✅ FAISS index
- `models/` - ✅ Model cache

## Recommendation

### Production Deployment
For production deployment, you can exclude the entire `tests/` directory:
```bash
# In .gitignore or deployment script
tests/
```

Or remove it entirely:
```bash
rm -rf tests/
```

### Development
Keep the `tests/` directory for active development and debugging. All test utilities are now organized in one place.

## Summary
- **Total Python files**: 29
- **Core files (backend/api)**: 15
- **Main scripts**: 2 (app.py, ingest.py)
- **Test scripts (tests/)**: 9 (organized in tests/ folder)
- **Documentation**: 5 (README.md, QUICKSTART.md, PROJECT_SUMMARY.md, RESPONSE_FORMAT.md, UNUSED_FILES.md)

## Project Structure Benefits

✅ **Cleaner Root Directory**: Main application files are immediately visible
✅ **Organized Testing**: All test scripts in dedicated `tests/` folder
✅ **Easy Deployment**: Simply exclude `tests/` for production
✅ **Better Navigation**: Clear separation of concerns
✅ **Maintainable**: Easy to find and update test scripts
