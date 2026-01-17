# Jal-Rakshak: Groundwater Risk Advisor 🌊

An AI-powered advisory system for Tamil Nadu farmers to assess groundwater availability before drilling borewells.

## Features

### Core Functionality
- **ReAct Agent**: Intelligent agent that thinks, searches, and provides actionable advice
- **PDF Ingestion**: Parse complex CGWB/PWD reports while preserving table structure using IBM Docling
- **RAG (Retrieval-Augmented Generation)**: Semantic search over government groundwater reports
- **Natural Language + Citations**: Provides both conversational advice AND raw data citations
- **Risk Assessment**: Clear classifications (Safe/Semi-Critical/Critical/Over-Exploited)
- **Multi-lingual Support**: Tamil, Hindi, English translation support
- **Interactive Map**: Tamil Nadu district-wise risk visualization
- **PDF Report Generation**: Download detailed feasibility reports

### Technical Features
- **Source Citation**: Every response includes document name and page numbers
- **Tool Integration**: Borewell cost estimation, crop feasibility checks
- **Dual Interface**: Streamlit app + FastAPI/Next.js modern web app

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js 15 + TypeScript + Tailwind CSS |
| **Backend API** | FastAPI + Uvicorn |
| **Classic UI** | Streamlit (Python) |
| **LLM Engine** | IBM Granite 3.0 8B Instruct (State-of-the-art efficiency) |
| **Agent Framework** | Custom ReAct Loop Implementation |
| **Hardware** | NVIDIA GPU (CUDA via PyTorch) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| **Vector Store** | FAISS (Dense Retrieval) |
| **PDF Parsing** | Docling (Structure-aware ingestion) |
| **Translation** | Google Translate API (Multi-lingual support) |
| **PDF Reports** | ReportLab |

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ (for Next.js frontend)
- 8GB RAM minimum (16GB recommended)
- ~5GB disk space for models
- NVIDIA GPU with CUDA (optional, for faster inference)

### Backend Setup

```bash
# Navigate to project directory
cd c:\project\1m1b\jal-rakshak

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt
```

### Frontend Setup (Next.js)

```bash
# Navigate to web directory
cd web

# Install Node.js dependencies
npm install
```

### First Run (Downloads Model)

```bash
# Test LLM setup (downloads ~8GB model on first run)
python llm.py

# Ingest PDF reports from data/pdfs/
python ingest.py

# Option 1: Run Streamlit app
streamlit run app.py

# Option 2: Run FastAPI + Next.js (separate terminals)
# Terminal 1: Start FastAPI backend
uvicorn api.main:app --reload --port 8000

# Terminal 2: Start Next.js frontend
cd web
npm run dev
```

## Usage

### Data Ingestion

1. **Add PDFs**: Place CGWB/State groundwater reports in `data/pdfs/`
2. **Ingest**: Run `python ingest.py` to process and index the documents
3. **Verify**: Check `vectorstore/` directory for FAISS index files

### Using the Application

#### Streamlit Interface
```bash
streamlit run app.py
```
- Open http://localhost:8501
- Enter queries like "Can I drill a borewell in Chennai?"
- Get natural language responses + cited data
- Download PDF reports
- View interactive risk map

#### Next.js Interface
```bash
# Terminal 1: Backend
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd web && npm run dev
```
- Open http://localhost:3000
- Modern chat interface with real-time agent responses
- District risk indicators
- PDF report downloads

### API Endpoints

**POST /api/chat**
```json
{
  "query": "What is the groundwater status in Salem?",
  "language": "en"  // optional: en, ta, hi
}
```

**POST /api/report**
```json
{
  "query": "Risk assessment",
  "location": "Chennai",
  "risk_level": "Critical",
  "full_response": "...agent response..."
}
```

**GET /api/districts**
- Returns district-wise risk data for map visualization

## Project Structure

```
jal-rakshak/
├── app.py                      # Streamlit web interface
├── ingest.py                   # PDF ingestion CLI
├── requirements.txt            # Python dependencies
├── generated_map_data.json     # District risk data for map
│
├── backend/                    # Core backend modules
│   ├── agent.py                # ReAct agent implementation
│   ├── llm.py                  # Granite model integration
│   ├── retriever.py            # FAISS vector search
│   ├── ingest.py               # PDF parsing with Docling
│   ├── prompts.py              # System prompts for agent
│   ├── config.py               # Configuration settings
│   ├── tools.py                # Agent tools (cost calc, crop feasibility)
│   ├── translator.py           # Multi-lingual translation
│   ├── report_generator.py     # PDF report generation
│   └── map_utils.py            # Interactive map generation
│
├── api/                        # FastAPI backend
│   ├── main.py                 # FastAPI application
│   └── routes/
│       ├── chat.py             # Chat endpoint
│       ├── report.py           # PDF report endpoint
│       └── map.py              # Map data endpoint
│
├── web/                        # Next.js frontend
│   ├── app/                    # Next.js app router
│   ├── components/             # React components
│   ├── package.json            # Node.js dependencies
│   └── tsconfig.json           # TypeScript config
│
├── tests/                      # Test & debug scripts
│   ├── test_llm.py             # LLM testing
│   ├── test_rag_usage.py       # RAG testing
│   ├── test_citation_format.py # Citation testing
│   ├── test_pdf_generation.py  # PDF testing
│   ├── verify_agent.py         # Agent verification
│   ├── debug_retrieval.py      # Search debugging
│   └── update_map_risks.py     # Map data updater
│
├── data/
│   └── pdfs/                   # Place PDF reports here
│
├── vectorstore/                # FAISS index (auto-generated)
└── models/                     # Downloaded models cache
```

## Data Sources

- [CGWB Ground Water Level Bulletins](https://cgwb.gov.in/)
- [Tamil Nadu State Ground Water Reports](https://www.tn.gov.in/)

## Agent Features

The ReAct agent provides:
- **Intelligent Search**: Automatically searches the knowledge base for relevant data
- **Tool Usage**: 
  - `search_knowledge_base(query)` - Searches government reports
  - `estimate_borewell_cost(depth_ft)` - Calculates drilling costs
  - `check_crop_feasibility(depth, crop)` - Checks crop viability
- **Loop Prevention**: Detects and prevents redundant searches
- **Dual Response Format**:
  - Natural conversational advice
  - 📊 Retrieved Data section with citations

## Response Format Example

```
I need to give you important advice about Chennai's groundwater situation...

According to the Chennai District Report 2023 (Page 12), the extraction 
is at 85.3% with water levels at 12.4 meters below ground level...

[Natural language explanation and recommendations]

---
📊 Retrieved Data from Reports:

Source: Chennai_District_Report_2023.pdf, Page 12
- Groundwater Extraction: 85.3%
- Water Level Depth: 12.4 meters below ground level
- Classification: Semi-Critical
- Recharge Rate: 245 MCM/year
- Annual Extraction: 209 MCM/year
```

## Responsible AI

- ⚠️ Data freshness is explicitly stated in responses
- ⚠️ "Data not found" returned for unknown blocks (no hallucination)
- ⚠️ Source citations enable verification
- ⚠️ Agent uses only retrieved data, never fabricates statistics
- ⚠️ Multi-step reasoning logged for transparency

## Testing

```bash
# Test PDF generation
python tests/test_pdf_generation.py

# Test RAG usage
python tests/test_rag_usage.py

# Test citation format
python tests/test_citation_format.py

# Test agent
python tests/verify_agent.py

# Test LLM
python tests/test_llm.py

# Debug retrieval
python tests/debug_retrieval.py
```

## License

MIT License - See LICENSE file
