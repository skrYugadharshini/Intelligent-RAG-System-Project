# Intelligent RAG System for Enterprise Policy Management

## Project Overview
This project is an Intelligent Retrieval-Augmented Generation (RAG) system built for enterprise policy management. It handles policy retrieval, security filtering, version control, and AI-based answer generation using Groq LLM.

---

## Features
- Vector-based semantic search using ChromaDB
- Policy versioning and deprecation handling
- Security clearance filtering
- Environment and region-aware retrieval
- Conflict resolution (superseded policies removed)
- AI-generated answers using Groq LLM
- REST API using FastAPI

---

## Tech Stack
- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Groq API (LLM)
- Power BI (Visualization)

---

## Project Structure
RAG_Assessment/
- api.py → FastAPI backend
- ingest.py → Data ingestion & embedding creation
- retrieval.py → RAG retrieval logic
- docs.json → Policy dataset
- chroma_db/ → Vector database
- requirements.txt → Dependencies
- PolicyDashboard.pbix → Power BI dashboard

---

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Ingest data
python ingest.py

### 3. Run API server
python -m uvicorn api:app

### 4. Open API docs
http://127.0.0.1:8000/docs

---

## API Endpoint

### POST /query

Request:
{
  "question": "string",
  "context": {
    "environment": "production",
    "region": "emea"
  },
  "user_clearance": ["internal", "confidential"]
}

Response:
{
  "answer": "string",
  "sources": [],
  "overall_confidence": 0.0
}

---

## Key Design Decisions
- ChromaDB used for efficient vector similarity search
- SentenceTransformer used for embeddings
- Security filtering applied before LLM processing
- Deprecated policies excluded or down-ranked
- Groq LLM used for fast inference

---

## Known Limitations
- No authentication layer implemented
- Confidence score is simplified
- No caching layer
- Basic prompt engineering used

---

## Author
Student Project - Intelligent RAG System