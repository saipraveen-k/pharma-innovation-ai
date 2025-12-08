# PHARMA AI IMPLEMENTATION GUIDE
## Step-by-Step Deployment & Customization

## TABLE OF CONTENTS

1. Pre-Deployment Checklist
2. Local Development Setup  
3. Production Deployment
4. Customization Guide
5. Integration Examples
6. Troubleshooting

---

## PRE-DEPLOYMENT CHECKLIST

Before deploying to production, ensure:

### Infrastructure
- PostgreSQL 15+ installed and running
- Redis 7+ installed and running
- Docker and Docker Compose available
- Minimum 4GB RAM, 2 CPU cores
- Disk space: 50GB+ for reports and logs
- Network: Outbound HTTPS access to APIs

### API Keys & Credentials
- OpenAI API key obtained and tested
- IQVIA API credentials (if available)
- EXIM Trade database access (if available)
- PubMed API registration (optional)
- AWS S3 credentials for report storage (optional)

### Security Setup
- SSL/TLS certificates configured
- Database password changed from default
- Environment variables secured
- Firewall rules configured
- RBAC policy defined

### Monitoring
- Prometheus configured
- Sentry account created
- Log aggregation setup
- Alert thresholds defined

---

## LOCAL DEVELOPMENT SETUP

### Step 1: Environment Preparation

```bash
mkdir pharma-innovation-ai
cd pharma-innovation-ai
git init
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
git clone <repo> .
pip install -r requirements.txt
python -c "import crewai; import fastapi; print('OK')"
```

### Step 3: Configure Environment

```bash
cp .env.example .env
# Edit .env with your values:
# OPENAI_API_KEY=sk-...
# DATABASE_URL=sqlite:///pharma_ai.db
# DEBUG=True
```

### Step 4: Run Application

```bash
python pharma_ai_main.py
# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Step 5: Test Endpoints

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Aspirin",
    "query_type": "unmet_needs"
  }'
```

---

## PRODUCTION DEPLOYMENT

### Docker Compose (Recommended)

#### Step 1: Prepare Infrastructure

```bash
mkdir /opt/pharma-ai
cd /opt/pharma-ai
cp -r path/to/pharma-innovation-ai/* .
cp .env.example .env
nano .env
```

#### Step 2: Deploy

```bash
docker-compose build
docker-compose up -d
docker-compose ps
docker-compose logs -f pharma-ai
```

#### Step 3: Setup SSL/TLS

```bash
sudo certbot certonly --standalone -d pharma-ai.company.com
# Configure nginx with SSL
```

---

## CUSTOMIZATION GUIDE

### Adding New Data Sources

Create a new tool in pharma_ai_tools.py:

```python
class CustomDataTool(ResearchTool):
    def __init__(self):
        super().__init__(
            name="Custom Data Analyzer",
            description="Analyze custom data source"
        )

    def execute(self, **kwargs):
        # Your implementation
        result = {"data": "..."}
        self.cache_result("key", result)
        return result
```

### Customizing Agent Prompts

Modify agent configuration in pharma_ai_main.py to adjust behavior.

---

## INTEGRATION EXAMPLES

### Load Internal PDFs

```python
from langchain.document_loaders import PDFLoader
from langchain_community.vectorstores import Chroma

loader = PDFLoader("document.pdf")
docs = loader.load()
# Process and store in vector DB
```

### Connect to ERP System

```python
class ERPIntegration:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_project_status(self, project_id: str):
        # Fetch from ERP
        pass
```

---

## TROUBLESHOOTING

### "ModuleNotFoundError: crewai"
```bash
pip install crewai crewai-tools
```

### "OpenAI API authentication failed"
```bash
echo $OPENAI_API_KEY
```

### "PostgreSQL connection refused"
```bash
sudo systemctl status postgresql
```

### "Memory error"
```bash
# Increase Docker memory limit
```

### "Cache hit rate low"
```bash
CACHE_TTL_HOURS=72
```

---

## PERFORMANCE OPTIMIZATION

### Multi-level Caching

Use Redis (fast, distributed) + In-memory (LRU) + Database caching

### Async/Await for Parallel Calls

Execute API calls concurrently with asyncio

### Database Indexing

Create indexes on frequently queried columns

---

## MONITORING & ALERTING

### Key Metrics

- api_requests_total
- api_request_duration
- cache_hit_rate
- agents_active
- reports_generated
- error_rate

### Alert Thresholds

- Error rate > 5%: Critical
- Latency p95 > 5s: Warning
- Cache hit rate < 50%: Warning

---

**Next Steps:**
1. Follow pre-deployment checklist
2. Choose deployment option
3. Customize for your use case
4. Deploy to production
5. Monitor and optimize
