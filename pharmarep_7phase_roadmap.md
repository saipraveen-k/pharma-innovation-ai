# PharmaRep Master - Complete 7-Phase Deployment Roadmap

## 📋 COMPLETE PROJECT PHASES

### Phase 1: Environment Setup & Dependencies (30 min) ✅
**Status:** Complete

**What's Done:**
- ✅ Python environment configured
- ✅ Virtual environment setup
- ✅ All dependencies installed
  - FastAPI, Uvicorn
  - Streamlit
  - LangChain
  - ReportLab (PDF generation)
  - Pandas, NumPy
  - Requests

**Next Steps:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install fastapi uvicorn streamlit langchain-openai pandas numpy reportlab requests
```

---

### Phase 2: PostgreSQL & Redis Setup (20 min) ⏳

**What's Needed:**

**PostgreSQL Database:**
```sql
-- Create database
CREATE DATABASE pharmarep_master;

-- Create search history table
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE,
    molecule_name VARCHAR(255),
    query_type VARCHAR(50),
    findings JSONB,
    pdf_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table (for Phase 4)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create audit log table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(255),
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Redis Cache:**
```bash
# Install Redis
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server
# Windows: Download from https://github.com/microsoftarchive/redis/releases

# Start Redis
redis-server
```

**Python Integration:**
```python
import psycopg2
import redis

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="pharmarep_master",
    user="postgres",
    password="your_password"
)

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

---

### Phase 3: Real API Integrations (60 min) ⏳

**ClinicalTrials.gov API:**
```python
import requests

def get_clinical_trials(molecule_name, indication):
    url = "https://clinicaltrials.gov/api/query/full_studies"
    params = {
        "expr": f"{molecule_name} AND {indication}",
        "fmt": "json",
        "pageSize": 10
    }
    response = requests.get(url, params=params)
    return response.json()
```

**PubMed API (Scientific Literature):**
```python
from Bio import Entrez

def get_pubmed_articles(molecule_name, indication):
    Entrez.email = "your_email@example.com"
    search_term = f"{molecule_name}[Title] AND {indication}[Title]"
    handle = Entrez.esearch(db="pubmed", term=search_term, retmax=100)
    records = Entrez.read(handle)
    return records
```

**USPTO Patent API:**
```python
def get_patent_data(molecule_name):
    url = "https://developer.uspto.gov/ibd-api/v1/application/publications"
    headers = {"Accept": "application/json"}
    params = {"searchText": f'"{molecule_name}"', "limit": 50}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

**IQVIA Market Insights (with API key):**
```python
def get_market_data(molecule_name, api_key):
    url = "https://api.iqvia.com/v1/market/insights"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "molecule": molecule_name,
        "market_type": "pharmaceutical",
        "regions": ["North America", "Europe", "Asia"]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

---

### Phase 4: Authentication & Security (30 min) ⏳

**JWT Authentication:**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# Setup
app = FastAPI()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key-here"

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Verify JWT token
def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
@app.post("/login")
async def login(username: str, password: str):
    # Verify user from database
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

# Protected endpoint
@app.get("/search")
async def search(token: dict = Depends(verify_token)):
    return {"message": "Authenticated"}
```

**Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/search")
@limiter.limit("10/minute")
async def search_innovation_opportunities(request: Request, query: SearchQuery):
    # Rate limited to 10 requests per minute
    pass
```

**CORS Security:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Phase 5: Testing Suite (60 min) ⏳

**Unit Tests:**
```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_search_api():
    response = client.post("/search", json={
        "molecule_name": "Aspirin",
        "query_type": "unmet_needs"
    })
    assert response.status_code == 200
    assert "findings" in response.json()

def test_authentication():
    response = client.post("/login", json={
        "username": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_molecule():
    response = client.post("/search", json={
        "molecule_name": "",
        "query_type": "unmet_needs"
    })
    assert response.status_code == 400
```

**Integration Tests:**
```python
def test_full_workflow():
    # 1. Login
    login_response = client.post("/login", json={
        "username": "test_user",
        "password": "test_password"
    })
    token = login_response.json()["access_token"]
    
    # 2. Search
    headers = {"Authorization": f"Bearer {token}"}
    search_response = client.post(
        "/search",
        headers=headers,
        json={"molecule_name": "Aspirin", "query_type": "unmet_needs"}
    )
    assert search_response.status_code == 200
    
    # 3. Get results
    task_id = search_response.json()["task_id"]
    results_response = client.get(f"/task/{task_id}", headers=headers)
    assert results_response.status_code == 200
```

**Run Tests:**
```bash
pytest tests/ -v --cov=. --cov-report=html
```

---

### Phase 6: Docker Deployment (60 min) ⏳

**Dockerfile for Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "pharma_ai_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile for Frontend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install streamlit

COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "streamlit_app_darkmode.py", "--server.port=8501"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: pharmarep_master
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/pharmarep_master
      REDIS_URL: redis://redis:6379
    command: python pharma_ai_main.py

  frontend:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      API_BASE_URL: http://backend:8000

volumes:
  postgres_data:
```

**Deploy:**
```bash
docker-compose up -d
```

---

### Phase 7: Monitoring & Performance (30 min) ⏳

**Application Logging:**
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

**Performance Monitoring:**
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
search_counter = Counter('searches_total', 'Total searches', ['query_type'])
search_duration = Histogram('search_duration_seconds', 'Search duration')

@app.post("/search")
async def search_innovation_opportunities(query: SearchQuery):
    start_time = time.time()
    try:
        # ... search logic
        search_counter.labels(query_type=query.query_type).inc()
    finally:
        search_duration.observe(time.time() - start_time)
```

**Health Checks:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health/ready")
async def readiness_check():
    # Check database connection
    # Check Redis connection
    # Check API integrations
    return {"ready": True}
```

---

## 📊 FINAL DEPLOYMENT CHECKLIST

| Phase | Component | Status | Time |
|-------|-----------|--------|------|
| **1** | Environment Setup | ✅ | 30 min |
| **2** | PostgreSQL & Redis | ⏳ | 20 min |
| **3** | Real API Integrations | ⏳ | 60 min |
| **4** | Authentication & Security | ⏳ | 30 min |
| **5** | Full Testing Suite | ⏳ | 60 min |
| **6** | Docker Deployment | ⏳ | 60 min |
| **7** | Monitoring & Performance | ⏳ | 30 min |
| | **TOTAL** | ⏳ | **3.5-4 hrs** |

---

## 🚀 DEPLOYMENT COMMANDS

### Quick Start (Development):
```bash
# Terminal 1
python pharma_ai_main.py

# Terminal 2
streamlit run streamlit_app_darkmode.py
```

### Production (Docker):
```bash
docker-compose up -d
```

### Monitor:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

---

## ✅ WHAT YOU'LL HAVE AFTER ALL 7 PHASES

✅ Fully functional pharmaceutical intelligence system
✅ PostgreSQL database with persistent storage
✅ Redis caching for performance
✅ Real API integrations (ClinicalTrials, PubMed, USPTO, IQVIA)
✅ JWT authentication & security
✅ 90%+ test coverage
✅ Docker containerized & scalable
✅ Prometheus monitoring
✅ Production-ready deployment

---

**Estimated Total Time: 3.5-4 hours**
**Result: FULLY FUNCTIONAL PRODUCTION SYSTEM**
