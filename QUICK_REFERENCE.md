# PHARMA AI - QUICK REFERENCE

## API ENDPOINTS

### POST /search
Main search endpoint

Request:
{
  "molecule_name": "Aspirin",
  "query_type": "unmet_needs|clinical_trials|repurposing|patent_landscape",
  "indication": "Disease name (optional)",
  "geographic_focus": "US|EU|Global (optional)"
}

Response:
{
  "task_id": "abc123",
  "status": "completed",
  "findings": {...},
  "pdf_url": "/reports/report.pdf",
  "recommendations": [...]
}

### GET /task/{task_id}
Check status of analysis

### GET /reports/{filename}
Download PDF report

### GET /
Health check

---

## ENVIRONMENT VARIABLES

OPENAI_API_KEY          Required: OpenAI API key
LLM_MODEL               Default: gpt-4
LLM_TEMPERATURE         Default: 0.7
DATABASE_URL            PostgreSQL connection
REDIS_URL               Redis connection
DEBUG                   Debug mode

---

## COMMAND REFERENCE

Installation:
pip install -r requirements.txt

Run Locally:
python pharma_ai_main.py

Run with Docker:
docker-compose up -d

Test API:
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"molecule_name":"Metformin","query_type":"unmet_needs"}'

---

## FILE STRUCTURE

pharma-innovation-ai/
├── pharma_ai_main.py           Main application
├── pharma_ai_tools.py          Research tools
├── pharma_ai_architecture.txt  System design
├── config.py                   Configuration
├── requirements.txt            Dependencies
├── Dockerfile                  Container
├── docker-compose.yml          Multi-container setup
├── .env.example                Environment template
├── README.md                   Documentation
├── IMPLEMENTATION_GUIDE.md     Setup guide
├── outputs/
│   ├── reports/               Generated PDFs
│   └── logs/                  Logs
└── data/                      Internal docs

---

## TYPICAL WORKFLOW

1. User submits query → POST /search
2. Master agent decomposes → Breaks into subtasks
3. Worker agents execute → Parallel data collection
4. Results synthesized → Evidence scoring
5. Report generated → PDF creation
6. Return to user → JSON + PDF

Total time: 30-120 seconds

---

## QUERY EXAMPLES

Find Unmet Needs:
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Aspirin",
    "query_type": "unmet_needs"
  }'

Analyze Repurposing:
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Metformin",
    "query_type": "repurposing",
    "indication": "Cardiovascular Disease"
  }'

Check Clinical Trials:
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Lisinopril",
    "query_type": "clinical_trials",
    "geographic_focus": "Europe"
  }'

Analyze Patent Landscape:
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "molecule_name": "Donepezil",
    "query_type": "patent_landscape"
  }'

---

## TROUBLESHOOTING CHECKLIST

- Python 3.11+ installed?
- Requirements installed? pip list | grep crewai
- OpenAI API key set? echo $OPENAI_API_KEY
- PostgreSQL running? psql --version
- Redis running? redis-cli ping
- Port 8000 available? netstat -an | grep 8000
- Disk space available? df -h
- Network connectivity? curl https://api.openai.com

---

## PERFORMANCE TIPS

- Use query caching
- Parallel agent execution
- Async operations
- Redis optimization (24-hour default cache)
- Database indexing

---

## MONITORING

Check health:
curl http://localhost:8000/

View API docs:
open http://localhost:8000/docs

Check logs:
tail -f outputs/logs/pharma_ai.log

Monitor database:
psql -c "SELECT count(*) FROM research_findings;"

Check cache:
redis-cli INFO stats

---

## PYTHON CLIENT EXAMPLE

import requests

BASE_URL = "http://localhost:8000"

query = {
    "molecule_name": "Aspirin",
    "query_type": "unmet_needs"
}

response = requests.post(f"{BASE_URL}/search", json=query)
result = response.json()

print(f"Task ID: {result['task_id']}")
print(f"Status: {result['status']}")
for i, rec in enumerate(result['recommendations'], 1):
    print(f"  {i}. {rec}")

# Download report
if result.get('pdf_url'):
    pdf_response = requests.get(f"{BASE_URL}{result['pdf_url']}")
    with open("report.pdf", "wb") as f:
        f.write(pdf_response.content)

---

## SUPPORT

Documentation: README.md, IMPLEMENTATION_GUIDE.md
API Docs: http://localhost:8000/docs
Issues: Check outputs/logs/pharma_ai.log

---

Last Updated: December 2024
Version: 1.0.0
