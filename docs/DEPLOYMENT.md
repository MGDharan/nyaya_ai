# NyayaAI – Deployment & Operations Guide

## 1. System Requirements

- **Operating System**: Windows 10/11, Ubuntu 22.04 LTS+, or macOS.
- **Python**: Version 3.10 to 3.15.
- **Memory**: 4 GB RAM minimum (8 GB recommended).
- **Disk Space**: 2 GB free space for legislation corpus and vector index.

---

## 2. Local Development Setup (Windows / Non-Docker)

NyayaAI is architected with a zero-native-build fallback (`SQLiteVectorStore` + pure-Python BM25) to run seamlessly on Windows without requiring Microsoft Visual C++ Build Tools.

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install pre-built runtime dependencies
pip install -r requirements-local.txt

# 4. Verify or configure .env
# Set GEMINI_API_KEY=your_key_here

# 5. Populate statutory vector index
python scripts/reingest_all.py

# 6. Run automated test suite
python -m pytest tests -v

# 7. Start the FastAPI Uvicorn Server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the web dashboard in your browser: `http://localhost:8000`

---

## 3. Docker Compose Deployment (Production)

For containerized deployments with PostgreSQL and pgvector:

```bash
# Build and start services
docker compose up --build -d

# Check container status
docker compose ps

# View container logs
docker compose logs -f backend
```

### Docker Compose Architecture:
- `backend`: FastAPI Python application with Uvicorn.
- `db`: PostgreSQL 16 container with `pgvector` pre-installed.
- Persistent volumes for PostgreSQL data and uploads.

---

## 4. Environment Variables Reference

| Variable Name | Default Value | Description |
|---|---|---|
| `APP_NAME` | `NyayaAI` | Application display name |
| `LLM_PROVIDER` | `gemini` | Primary LLM provider (`gemini` or `mock`) |
| `GEMINI_API_KEY` | - | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model name for synthesis |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `DATA_DIR` | `./data` | Local data and vector storage directory |
| `ADMIN_API_KEY` | - | Bearer token for administrative document ingestion |
| `TOP_K` | `7` | Number of statutory passages retrieved per query |
| `MAX_UPLOAD_MB` | `25` | Maximum upload size for PDF/DOCX ingestion |

