# PashuSeva - System Architecture

## 1. Project Overview
PashuSeva is an AI-powered animal care information system designed to help dairy farmers.

## 2. Technology Stack
- Python
- FastAPI
- Streamlit
- Gemini API
- LangGraph
- ChromaDB
- Docker and Docker Compose

## 3. System Components
- Streamlit: Farmer-facing interface.
- FastAPI: Backend API.
- RAG: Retrieves relevant NDDB document information.
- ChromaDB: Stores document embeddings.
- Gemini: Generates responses using retrieved context.

## 4. Docker Architecture
- API container: Port 8000
- UI container: Port 8501
- Both containers run as non-root appuser.
- Both containers have health checks.
- UI waits for API health before starting.
- Local data is mounted into the API container.

## 5. Testing
- Pytest
- Ruff
- Docker smoke tests
- API health check
- UI availability check

## 6. Persistent Storage
ChromaDB data is stored in data/chroma_db.
The local data directory is mounted at /app/data.

## 7. Application URLs
- UI: http://localhost:8501
- API: http://localhost:8000
- API Health: http://localhost:8000/health
