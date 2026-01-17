# Jal-Rakshak - Project Summary

## Overview
Jal-Rakshak is an AI-powered groundwater advisory system that helps Tamil Nadu farmers make informed decisions about borewell drilling using government data.

## Architecture

### Backend (Python)
- **Agent**: Custom ReAct loop with reasoning, action, observation cycle
- **LLM**: IBM Granite 3.0 8B Instruct model
- **RAG**: FAISS vector database with semantic search
- **PDF Parser**: Docling for structure-aware document ingestion
- **APIs**: FastAPI for RESTful endpoints

### Frontend
- **Modern UI**: Next.js 15 + TypeScript + Tailwind CSS
- **Classic UI**: Streamlit for rapid prototyping
- **Components**: Chat interface, interactive map, report generation

## Key Features

### 1. Intelligent Agent
- Searches knowledge base automatically
- Uses tools (cost calculator, crop feasibility)
- Prevents redundant searches
- Provides natural language + citations

### 2. Multi-format Responses
```
[Natural conversational advice]
---
📊 Retrieved Data from Reports:
- Specific metrics with sources
- Page numbers and document names
```

### 3. Multi-lingual Support
- Tamil, Hindi, English
- Automatic language detection
- Response translation

### 4. PDF Reports
- Professional groundwater feasibility reports
- Downloadable from both interfaces

### 5. Interactive Map
- District-wise risk visualization
- Color-coded classifications
- Real-time risk levels

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI/ML** | IBM Granite 3.0 8B | Language generation |
| **Embeddings** | sentence-transformers | Semantic search |
| **Vector DB** | FAISS | Document retrieval |
| **PDF Parsing** | Docling | Structure-aware ingestion |
| **Backend** | FastAPI | RESTful API |
| **Frontend** | Next.js 15 | Modern web app |
| **Classic UI** | Streamlit | Rapid prototyping |
| **Reports** | ReportLab | PDF generation |
| **Translation** | Google Translate | Multi-lingual |

## File Structure

### Core Application Files
- `app.py` - Streamlit interface
- `ingest.py` - PDF ingestion CLI
- `requirements.txt` - Python dependencies
- `generated_map_data.json` - District risk data

### Backend Module (`backend/`)
- `agent.py` - ReAct agent implementation
- `llm.py` - Granite model integration
- `retriever.py` - FAISS search
- `ingest.py` - Document processing
- `prompts.py` - System prompts
- `tools.py` - Agent tools
- `translator.py` - Multi-lingual support
- `report_generator.py` - PDF reports
- `map_utils.py` - Map generation
- `config.py` - Configuration

### API Layer (`api/`)
- `main.py` - FastAPI application
- `routes/chat.py` - Chat endpoint
- `routes/report.py` - Report generation
- `routes/map.py` - Map data

### Frontend (`web/`)
- `app/` - Next.js app router
- `components/` - React components
  - `ChatArea.tsx` - Chat interface
  - `MessageBubble.tsx` - Message display
  - `InteractiveMap.tsx` - Map component
  - `Sidebar.tsx` - Navigation
- `package.json` - Node dependencies

### Data
- `data/pdfs/` - Government reports
- `vectorstore/` - FAISS index (generated)
- `models/` - Model cache
- `generated_map_data.json` - District risks

### Testing (`tests/` directory)
- `test_llm.py` - LLM testing
- `test_rag_usage.py` - RAG testing
- `test_citation_format.py` - Citation testing
- `test_pdf_generation.py` - PDF testing
- `verify_agent.py` - Agent verification
- `debug_retrieval.py` - Search debugging
- `update_map_risks.py` - Map data generator
- `test_all_imports.py` - Import verification
- `test_st.py` - Environment check

## Dependencies

### Python (requirements.txt)
- transformers, torch - LLM
- langchain* - RAG framework
- faiss-cpu - Vector search
- docling - PDF parsing
- fastapi, uvicorn - API
- streamlit - Classic UI
- reportlab - PDF reports
- googletrans - Translation

### Node.js (web/package.json)
- next, react - Frontend framework
- tailwindcss - Styling
- typescript - Type safety
- lucide-react - Icons

## Running the Application

### Option 1: Streamlit (Quick Start)
```bash
python ingest.py  # First time only
streamlit run app.py
```

### Option 2: FastAPI + Next.js (Production)
```bash
# Terminal 1: Backend
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd web && npm run dev
```

## Recent Improvements

1. ✅ Enhanced RAG usage with mandatory citations
2. ✅ Dual response format (natural + data)
3. ✅ Fixed PDF report download
4. ✅ Improved retriever formatting
5. ✅ Better error handling
6. ✅ Updated documentation

## Next Steps

- Add more CGWB district reports
- Implement user authentication
- Add historical trend analysis
- Create mobile app version
- Add crop recommendation system
- Integrate real-time rainfall data

## Responsible AI

- No hallucination - only uses retrieved data
- Source citations for verification
- Explicit data freshness warnings
- Transparent reasoning process
- Multi-step logic visible to users

---

**Version**: 1.2
**Last Updated**: January 17, 2026
**License**: MIT
