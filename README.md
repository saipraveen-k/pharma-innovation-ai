# 🧪 PHARMA INNOVATION AGENTIC AI SYSTEM

## Overview

**PharmaAI** is an enterprise-grade **Agentic AI system** that accelerates pharmaceutical innovation by automating the discovery of new product opportunities using coordinated AI agents.

### 🎯 What It Does

- **Scans** regulatory databases, clinical trials, patents, and scientific literature
- **Identifies** unmet medical needs and repurposing opportunities  
- **Analyzes** market potential, competitive landscape, and patent freedom
- **Generates** comprehensive PDF reports with recommendations in **hours instead of months**

### 🚀 Key Capabilities

| Feature | Benefit |
|---------|---------|
| **7 Specialized Agents** | Each focuses on specific data domain (patents, trials, markets, etc.) |
| **Multi-Source Integration** | ClinicalTrials.gov, USPTO, PubMed, IQVIA, internal PDFs |
| **Async Task Orchestration** | Parallel execution for faster results |
| **Evidence-Based Scoring** | Scientific methodology for opportunity ranking |
| **Automated Report Generation** | Professional PDFs with charts and citations |
| **Enterprise Security** | RBAC, audit logging, secure APIs |

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│        USER INTERFACE (FastAPI)             │
│  POST /search?molecule=X&query_type=Y       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    MASTER ORCHESTRATOR (Query Router)       │
│  - Decomposes queries into tasks            │
│  - Assigns to appropriate agents            │
│  - Synthesizes results                      │
└─────────────────────────────────────────────┘
                    ↓
        ┌───────────────────────┬───────────────────────┐
        ↓                       ↓                       ↓
    ┌─────────┐           ┌─────────┐           ┌─────────┐
    │Patent   │           │Clinical │           │ IQVIA   │
    │Agent    │           │Trials   │           │ Market  │
    │         │           │Agent    │           │ Agent   │
    └─────────┘           └─────────┘           └─────────┘
        ↓                       ↓                       ↓
    ┌─────────┐           ┌─────────┐           ┌─────────┐
    │Web      │           │Internal │           │Report   │
    │Intel    │           │Knowledge│           │Gen      │
    │Agent    │           │Agent    │           │Agent    │
    └─────────┘           └─────────┘           └─────────┘
                    ↓
            ┌─────────────────┐
            │ Result Synthesis│
            │ Evidence Scoring│
            │ Report Creation │
            └─────────────────┘
                    ↓
        ┌───────────────────────┐
        │  PDF Report + JSON    │
        │  Recommendations      │
        │  Archived in DB       │
        └───────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Data Sources |
|-------|------|--------------|
| **IQVIA Insights** | Market analysis, competition, trends | Market reports, IQVIA API, financial data |
| **Patent Landscape** | IP analysis, freedom-to-operate | USPTO, WIPO, Google Patents |
| **Clinical Trials** | Research status, ongoing studies | ClinicalTrials.gov, WHO ICTRP |
| **Web Intelligence** | Scientific articles, regulations | PubMed, ScienceDirect, FDA/EMA sites |
| **Internal Knowledge** | Company strategy, prior research | Internal PDFs, vector DB |
| **EXIM Trade** | Market access, regional trends | Trade databases, customs data |
| **Report Generation** | PDF synthesis, visualizations | All above agents + templates |

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional but recommended)
- OpenAI API key (for GPT-4)
- PostgreSQL 15+ (production)

### Quick Start (Local Development)

#### 1. Clone Repository
```bash
git clone https://github.com/yourorg/pharma-innovation-ai.git
cd pharma-innovation-ai
```

#### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
export OPENAI_API_KEY="sk-your-key-here"
```

#### 5. Run Application
```bash
python pharma_ai_main.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment (Recommended)

#### 1. Build & Run with Docker Compose
```bash
docker-compose up -d
```

This starts:
- **PharmaAI API** on port 8000
- **PostgreSQL Database** on port 5432
- **Redis Cache** on port 6379
- **Prometheus Monitoring** on port 9090

#### 2. View Logs
```bash
docker-compose logs -f pharma-ai
```

#### 3. Stop Services
```bash
docker-compose down
```

---

## API Usage Guide

### 1. Basic Query Endpoint

**POST** `/search`

#### Request Body
```json
{
  "molecule_name": "Metformin",
  "query_type": "unmet_needs",
  "indication": "Type 2 Diabetes (optional)",
  "geographic_focus": "US (optional)"
}
```

#### Query Types
- `unmet_needs` - Find unmet medical needs for molecule
- `clinical_trials` - Analyze ongoing clinical trials
- `repurposing` - Identify repurposing opportunities
- `patent_landscape` - Analyze patent landscape

#### Response
```json
{
  "task_id": "a1b2c3d4",
  "molecule": "Metformin",
  "status": "completed",
  "findings": {
    "market_analysis": {...},
    "patent_analysis": {...},
    "clinical_trials": {...},
    "key_findings": [...],
    "opportunities": [...],
    "recommendations": [...]
  },
  "pdf_url": "/reports/pharma_research_metformin_a1b2c3d4.pdf",
  "recommendations": [
    "Explore combination therapy with SGLT2 inhibitors",
    "Investigate pediatric indication opportunity",
    ...
  ],
  "timestamp": "2024-12-08T12:30:45.123Z"
}
```

### 2. Check Task Status

**GET** `/task/{task_id}`

```bash
curl http://localhost:8000/task/a1b2c3d4
```

Response:
```json
{
  "task_id": "a1b2c3d4",
  "status": "completed",
  "molecule": "Metformin",
  "pdf_url": "/reports/pharma_research_metformin_a1b2c3d4.pdf"
}
```

### 3. Download Report

**GET** `/reports/{filename}`

```bash
curl http://localhost:8000/reports/pharma_research_metformin_a1b2c3d4.pdf \
  -o report.pdf
```

### 4. Health Check

**GET** `/`

```bash
curl http://localhost:8000/
```

### Example cURL Commands

```bash
# Find unmet needs for Aspirin
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Aspirin",
    "query_type": "unmet_needs"
  }'

# Analyze repurposing for Metformin
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Metformin",
    "query_type": "repurposing",
    "indication": "Cardiovascular Disease"
  }'

# Get clinical trial landscape for Lisinopril
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Lisinopril",
    "query_type": "clinical_trials",
    "geographic_focus": "Europe"
  }'
```

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Send query
query = {
    "molecule_name": "Metformin",
    "query_type": "unmet_needs",
    "indication": "Type 2 Diabetes"
}

response = requests.post(f"{BASE_URL}/search", json=query)
result = response.json()

task_id = result["task_id"]
print(f"Task ID: {task_id}")
print(f"Status: {result['status']}")
print(f"PDF: {result['pdf_url']}")

# Save recommendations
with open("recommendations.json", "w") as f:
    json.dump(result["recommendations"], f, indent=2)

# Download report
report = requests.get(f"{BASE_URL}{result['pdf_url']}")
with open("report.pdf", "wb") as f:
    f.write(report.content)
```

---

## Configuration

### Environment Variables

```bash
# OpenAI API
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7

# Database
DATABASE_URL=postgresql://user:pass@localhost/pharma_ai
REDIS_URL=redis://localhost:6379/0

# Paths
OUTPUT_DIR=./outputs
REPORTS_DIR=./outputs/reports
LOGS_DIR=./outputs/logs

# Features
ENABLE_CACHING=True
CACHE_TTL_HOURS=24
DEBUG=False
```

### Database Setup

```sql
-- Initialize PostgreSQL database
CREATE DATABASE pharma_ai;
CREATE USER pharma_admin WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE pharma_ai TO pharma_admin;

-- Tables will be auto-created by SQLAlchemy ORM
python -m alembic upgrade head
```

---

## Advanced Usage

### Custom Agent Configuration

Edit agent prompts in `pharma_ai_main.py`:

```python
def create_iqvia_agent(self) -> Agent:
    return Agent(
        role="Market Intelligence Analyst",
        goal="Your custom goal here",
        backstory="Your custom backstory",
        llm=self.llm,
        tools=[...]
    )
```

### Adding New Data Sources

1. Create a new tool in `pharma_ai_tools.py`:
```python
class MyCustomTool(ResearchTool):
    def execute(self, **kwargs):
        # Your implementation
        pass
```

2. Register in `ToolManager`

3. Add to agent task assignments

### Caching Strategy

Results are cached for 24 hours by default:

```python
# Clear cache
rm -rf ./outputs/cache

# Modify TTL in config.py
CACHE_TTL_HOURS=48  # 2 days
```

### Scaling to Multiple Instances

1. Use load balancer (nginx, HAProxy)
2. Share Redis and PostgreSQL
3. Deploy multiple FastAPI instances

```bash
# Run 4 Uvicorn workers
gunicorn pharma_ai_main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## Monitoring & Observability

### Application Metrics

Prometheus metrics available at: `http://localhost:9090`

Key metrics:
- Request latency by agent
- Cache hit rate
- API errors
- Database connection pool

### Logging

Logs stored in `./outputs/logs/pharma_ai.log`

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

View logs:
```bash
tail -f outputs/logs/pharma_ai.log
grep "ERROR" outputs/logs/pharma_ai.log
```

### Error Tracking

Enable Sentry integration:
```bash
export SENTRY_DSN="https://your-sentry-dsn"
```

---

## Troubleshooting

### Common Issues

**Issue**: OpenAI API timeout
```
Solution: Increase LLM_TIMEOUT in config
or reduce LLM_MAX_TOKENS
```

**Issue**: Database connection errors
```
Solution: Verify PostgreSQL is running
and DATABASE_URL is correct
```

**Issue**: PDF generation fails
```
Solution: Check disk space in outputs/ directory
and verify ReportLab installation
```

**Issue**: Clinical trials API errors
```
Solution: ClinicalTrials.gov API occasionally times out
The system has built-in retry logic with exponential backoff
```

---

## Project Structure

```
pharma-innovation-ai/
├── pharma_ai_main.py          # Main FastAPI application
├── pharma_ai_tools.py         # Agent tools and utilities
├── pharma_ai_architecture.txt # System architecture docs
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-container orchestration
├── .env.example               # Environment template
├── outputs/                   # Generated reports and logs
│   ├── reports/              # PDF reports
│   └── logs/                 # Application logs
├── data/                      # Internal knowledge base
├── tests/                     # Unit and integration tests
├── docs/                      # Additional documentation
└── README.md                  # This file
```

---

## Testing

### Unit Tests

```bash
pytest tests/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v --timeout=30
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_tests.py --host=http://localhost:8000
```

---

## Performance Benchmarks

Expected performance on 2-core CPU with 4GB RAM:

| Query Type | Agents Invoked | Avg Time | Max Time |
|------------|----------------|----------|----------|
| Unmet Needs | 5 | 45s | 90s |
| Patent Landscape | 3 | 25s | 60s |
| Clinical Trials | 4 | 35s | 75s |
| Repurposing | 6 | 60s | 120s |

*Times vary based on API availability and data volume*

---

## Contributing

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black pharma_ai_*.py

# Lint
flake8 pharma_ai_*.py

# Type checking
mypy pharma_ai_*.py
```

### Create Feature Branch

```bash
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

---

## Security

### Best Practices

1. **Never commit API keys** - Use .env files
2. **Use HTTPS in production** - Enable SSL/TLS
3. **Implement rate limiting** - Prevent API abuse
4. **Validate all inputs** - Sanitize user queries
5. **Audit logging** - Track all searches and reports
6. **Database encryption** - Encrypt sensitive data at rest

### API Authentication (Production)

```python
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/search")
async def search(query: SearchQuery, credentials: HTTPAuthCredentials = Depends(security)):
    # Verify JWT token
    verify_token(credentials.credentials)
    # ... continue
```

---

## Roadmap

### v1.1 (Q1 2025)
- [ ] Human-in-the-loop feedback integration
- [ ] Multi-language support
- [ ] Real-time streaming results
- [ ] Mobile app integration

### v1.2 (Q2 2025)
- [ ] ML model for opportunity scoring
- [ ] Historical trend analysis
- [ ] Competitor intelligence dashboard
- [ ] Integration with ERP systems

### v2.0 (Q3 2025)
- [ ] Voice-based query interface
- [ ] Advanced visualization engine
- [ ] Predictive analytics
- [ ] Full GraphQL API

---

## License

Proprietary - All rights reserved

---

## Support & Contact

- **Issues**: GitHub Issues
- **Email**: innovation-ai@pharmacompany.com
- **Slack**: #pharma-ai-team
- **Documentation**: https://docs.pharma-ai.internal/

---

## Acknowledgments

Built with:
- OpenAI GPT-4
- CrewAI Framework
- LangChain
- FastAPI

---

**Last Updated**: December 8, 2024
**Version**: 1.0.0-beta
