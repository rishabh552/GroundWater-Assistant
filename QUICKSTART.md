# Quick Start Guide - Jal-Rakshak

## 🚀 Installation (5 minutes)

### Step 1: Python Backend Setup

```bash
# Navigate to project
cd c:\project\1m1b\jal-rakshak

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Add PDF Data

```bash
# Place your CGWB/groundwater reports in:
data/pdfs/

# Process and index the documents
python ingest.py
```

### Step 3: Test the Setup

```bash
# Test LLM (downloads ~8GB model on first run)
python llm.py

# Expected output: Model loads successfully and generates a response
```

## 🎯 Running the Application

### Option A: Streamlit (Easiest)

```bash
streamlit run app.py
```
- Open: http://localhost:8501
- Features: Full interface with chat, map, and reports

### Option B: FastAPI + Next.js (Modern)

**Terminal 1 - Backend:**
```bash
uvicorn api.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd web
npm install  # First time only
npm run dev
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## ✅ Verify Installation

### Test Checklist

1. **LLM Loading**: `python tests/test_llm.py` should generate text
2. **Retriever**: `python tests/debug_retrieval.py` should search documents
3. **Agent**: `python tests/verify_agent.py` should run ReAct loop
4. **PDF Generation**: `python tests/test_pdf_generation.py` should create PDF

### Expected Behavior

✅ Model downloads automatically on first run (~8GB)
✅ FAISS index created in `vectorstore/`
✅ Agent provides natural language + citations
✅ PDF reports download successfully

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### "Vectorstore not found"
```bash
python ingest.py
```

### CUDA/GPU issues
```bash
# Install CPU-only version
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Translation errors
```bash
pip install googletrans==3.1.0a0
```

### Next.js errors
```bash
cd web
rm -rf node_modules package-lock.json
npm install
```

## 📊 Usage Examples

### Example Queries

1. "Can I drill a borewell in Chennai?"
2. "What is the groundwater status in Salem?"
3. "How much does a 500ft borewell cost?"
4. "Is Coimbatore safe for groundwater extraction?"
5. "Can I grow paddy in Kallakurichi?"

### Expected Response Format

```
[Natural Language Advice]
Based on the Chennai District Report 2023, I need to give you 
important information about drilling borewells in Chennai...

[Recommendations and explanations]

---
📊 Retrieved Data from Reports:

Source: Chennai_District_Report_2023.pdf, Page 12
- Groundwater Extraction: 85.3%
- Water Level Depth: 12.4 meters below ground level
- Classification: Semi-Critical
- Recharge Rate: 245 MCM/year
```

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file:
```bash
LLM_MODEL_ID=ibm-granite/granite-3.0-8b-instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K_RESULTS=5
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.1
```

### Model Settings

Edit `backend/config.py`:
- `LLM_MODEL_ID` - Change LLM model
- `EMBEDDING_MODEL` - Change embedding model
- `TOP_K_RESULTS` - Number of search results
- `CHUNK_SIZE` - Document chunk size

## 📚 Resources

- **Documentation**: README.md
- **Project Structure**: PROJECT_SUMMARY.md
- **Unused Files**: UNUSED_FILES.md
- **Response Format**: RESPONSE_FORMAT.md
- **API Docs**: http://localhost:8000/docs (when running)

## 🎓 Learning Path

1. Start with `python tests/test_llm.py` to understand the LLM
2. Run `python ingest.py` to see document processing
3. Try `python tests/verify_agent.py` to see agent reasoning
4. Use `streamlit run app.py` for full interface
5. Explore API with `uvicorn api.main:app --reload`

## 💡 Tips

- Keep `data/pdfs/` organized by district
- Run `ingest.py` after adding new PDFs
- Use GPU for faster inference (if available)
- Check API docs at `/docs` for integration
- Test scripts help verify each component

## 🚦 Production Checklist

- [ ] All PDFs ingested and indexed
- [ ] LLM downloads completed
- [ ] Environment variables configured
- [ ] Backend running (port 8000)
- [ ] Frontend running (port 3000)
- [ ] Test queries return valid responses
- [ ] PDF downloads working
- [ ] Map displays district data

---

**Need Help?**
- Check error logs in terminal output
- Review configuration in `backend/config.py`
- Verify Python version: `python --version` (requires 3.10+)
- Verify Node version: `node --version` (requires 18+)

**Ready to go!** Start with: `streamlit run app.py`
