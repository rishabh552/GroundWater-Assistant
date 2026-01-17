<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/IBM_Granite-3.0_8B-052FAD?style=for-the-badge&logo=ibm&logoColor=white" alt="IBM Granite"/>
</p>

<h1 align="center">💧 GroundWater Assistant</h1>

<p align="center">
  <strong>AI-powered groundwater risk advisory system for Tamil Nadu farmers</strong>
</p>

<p align="center">
  <em>Leveraging RAG and ReAct agents to provide data-driven borewell drilling recommendations</em>
</p>

---

## 📋 Overview

GroundWater Assistant is an intelligent advisory system that helps farmers and officials assess groundwater availability before drilling borewells. It combines **Retrieval-Augmented Generation (RAG)** with a **ReAct agent framework** to provide accurate, citation-backed recommendations from government reports.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| 🤖 **Agentic AI** | ReAct loop with tool use for intelligent multi-step reasoning |
| 📄 **Document RAG** | Semantic search over CGWB/PWD government reports |
| 🗺️ **Interactive Map** | District-wise risk visualization with click-to-query |
| 📊 **Risk Classification** | Clear categorization (Safe → Semi-Critical → Critical → Over-Exploited) |
| 📝 **PDF Reports** | Downloadable feasibility assessments |
| 🌐 **Multi-lingual** | Tamil, Hindi, and English support |

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Leaflet Maps |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **LLM Engine** | IBM Granite 3.0 8B Instruct (via HuggingFace Transformers) |
| **Agent Framework** | Custom ReAct implementation with tool integration |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **PDF Parsing** | IBM Docling (structure-aware extraction) |
| **Translation** | mtranslate + langdetect (no API key required) |
| **PDF Generation** | ReportLab |
| **Hardware** | NVIDIA GPU with CUDA (optional, recommended) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- 8GB RAM minimum (16GB recommended)
- ~5GB disk space for models
- NVIDIA GPU with CUDA (optional)

### Installation

```bash
# Clone and navigate to project
cd "GroundWater Assistant"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Install as editable package (enables imports from any directory)
pip install -e .

# Install frontend dependencies
cd web && npm install && cd ..
```

### First Run

```bash
# 1. Ingest PDF reports (place files in data/pdfs/ first)
python ingest.py

# 2. Start the backend API
uvicorn api.main:app --reload --port 8000

# 3. Start the frontend (new terminal)
cd web && npm run dev
```

**Access the application:**
- 🌐 **Web App**: http://localhost:3000
- 📡 **API Docs**: http://localhost:8000/docs

---

## 📁 Project Structure

```
GroundWater Assistant/
├── api/                        # FastAPI backend
│   ├── main.py                 # Application entry point
│   └── routes/                 # API endpoints
│       ├── chat.py             # /api/chat - Agent queries
│       ├── report.py           # /api/report - PDF generation
│       └── map.py              # /api/districts - Map data
│
├── backend/                    # Core business logic
│   ├── agent.py                # ReAct agent implementation
│   ├── llm.py                  # LLM integration (Granite)
│   ├── retriever.py            # FAISS vector search
│   ├── ingest.py               # Document processing
│   ├── prompts.py              # System prompts
│   ├── tools.py                # Agent tools
│   ├── translator.py           # Multi-lingual support
│   └── report_generator.py     # PDF report creation
│
├── web/                        # Next.js frontend
│   ├── app/                    # App router pages
│   └── components/             # React components
│
├── data/pdfs/                  # Input: Government reports
├── vectorstore/                # Output: FAISS index
├── models/                     # Cached model files
│
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Package configuration
└── generated_map_data.json     # District risk data
```

---

## 🔌 API Reference

### Chat Endpoint

```http
POST /api/chat
Content-Type: application/json

{
  "query": "What is the groundwater status in Chennai?",
  "language": "en"  // Optional: en, ta, hi
}
```

**Response:**
```json
{
  "response": "Based on the Chennai District Report...",
  "risk_level": "Over-Exploited",
  "sources": ["Chennai_Report_2023.pdf"]
}
```

### Report Generation

```http
POST /api/report
Content-Type: application/json

{
  "query": "Borewell feasibility assessment",
  "location": "Chennai",
  "risk_level": "Critical",
  "full_response": "..."
}
```

### District Data

```http
GET /api/districts
```

Returns GeoJSON-compatible district risk data for map visualization.

---

## 🤖 Agent Architecture

The system uses a **ReAct (Reasoning + Acting)** agent that:

1. **Thinks** - Analyzes the user query
2. **Acts** - Calls appropriate tools
3. **Observes** - Processes tool results
4. **Repeats** - Until final answer is ready

### Available Tools

| Tool | Purpose |
|------|---------|
| `search_knowledge_base(query)` | RAG search over government reports |
| `estimate_borewell_cost(depth_ft)` | Calculate drilling cost estimates |
| `check_crop_feasibility(depth, crop)` | Assess crop viability at water depth |

### Response Format

```markdown
I need to give you important advice about Chennai's groundwater situation...

According to the Chennai District Report 2023 (Page 12), the extraction 
is at 85.3% with water levels at 12.4 meters below ground level...

[Natural language recommendations]

---
📊 **Retrieved Data from Reports:**

**Source:** Chennai_District_Report_2023.pdf, Page 12
- Groundwater Extraction: 85.3%
- Water Level Depth: 12.4m below ground level
- Classification: Semi-Critical
```

---

## 🗺️ District Coverage

The system covers **36 districts** of Tamil Nadu with risk classifications:

| Risk Level | Districts | Percentage |
|------------|-----------|------------|
| 🔴 Over-Exploited | 16 | 44% |
| 🟠 Critical | 2 | 6% |
| 🟡 Semi-Critical | 6 | 17% |
| 🟢 Safe | 9 | 25% |
| ⚪ Unknown | 4 | 11% |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Individual test modules
python tests/test_llm.py           # LLM functionality
python tests/test_rag_usage.py     # RAG pipeline
python tests/verify_agent.py       # Agent behavior
python tests/test_pdf_generation.py # Report generation
```

---

## 📚 Data Sources

- [Central Ground Water Board (CGWB)](https://cgwb.gov.in/) - Ground Water Level Bulletins
- [Tamil Nadu State Reports](https://www.tn.gov.in/) - District-wise assessments

---

## ⚠️ Responsible AI

| Principle | Implementation |
|-----------|----------------|
| **Transparency** | All responses include source citations with page numbers |
| **No Hallucination** | "Data not found" returned for unknown locations |
| **Data Freshness** | Report dates explicitly stated in responses |
| **Auditability** | Multi-step reasoning logged for review |
| **Verification** | Users can cross-check cited documents |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ for Tamil Nadu farmers</sub>
</p>
