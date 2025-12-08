"""
PHARMAREP MASTER
Advanced pharmaceutical intelligence and research analysis platform

Master implementation with LangChain orchestration


Author: AI Research Team
Date: December 2024
"""


import os
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import uuid


# Core imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


# LangChain for agents
from langchain_openai import ChatOpenAI


# Data processing
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# Vector DB for internal knowledge
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter


# Config
from config import settings


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════


class SearchQuery(BaseModel):
    """User search query model"""
    molecule_name: str
    query_type: str  # "unmet_needs", "clinical_trials", "repurposing", "patent_landscape"
    indication: Optional[str] = None
    geographic_focus: Optional[str] = None



class TaskResult(BaseModel):
    """Result from a worker agent"""
    agent_name: str
    status: str  # "completed", "pending", "error"
    data: Dict[str, Any]
    timestamp: str



class ResearchReport(BaseModel):
    """Final research report"""
    task_id: str
    molecule: str
    timestamp: str
    findings: Dict[str, Any]
    pdf_path: Optional[str] = None
    recommendations: List[str]



# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA GENERATORS (For demonstration)
# ═══════════════════════════════════════════════════════════════════════════════


class MockDataGenerator:
    """Generates realistic mock data for demo purposes"""


    @staticmethod
    def get_market_data(molecule: str) -> Dict:
        """Mock IQVIA market insights"""
        return {
            "molecule": molecule,
            "current_market_size": f"${np.random.randint(50, 500)}M",
            "market_growth_rate": f"{np.random.uniform(5, 25):.1f}%",
            "competitors": [
                {"name": f"Competitor {i}", "market_share": f"{np.random.randint(5, 30)}%"}
                for i in range(1, 4)
            ],
            "top_indications": [
                {"indication": "Type 2 Diabetes", "revenue": "$250M"},
                {"indication": "Hypertension", "revenue": "$180M"},
                {"indication": "Rheumatoid Arthritis", "revenue": "$120M"}
            ],
            "unmet_needs_score": np.random.uniform(0.6, 0.95)
        }


    @staticmethod
    def get_patent_data(molecule: str) -> Dict:
        """Mock Patent Landscape data"""
        return {
            "molecule": molecule,
            "total_patents": np.random.randint(15, 50),
            "active_patents": np.random.randint(8, 25),
            "expiring_patents": [
                {"patent_id": f"US{10000000 + i}", "expiry_date": f"202{4+j}-{np.random.randint(1,12):02d}"}
                for i, j in enumerate(range(5))
            ],
            "freedom_to_operate": f"{np.random.uniform(0.6, 0.95):.2f}",
            "key_patents": [
                {"title": "Formulation of X", "owner": "Company A", "status": "Active"},
                {"title": "Mechanism of Y", "owner": "Company B", "status": "Expiring 2026"}
            ]
        }


    @staticmethod
    def get_clinical_trial_data(molecule: str) -> Dict:
        """Mock Clinical Trials data"""
        return {
            "molecule": molecule,
            "total_trials": np.random.randint(5, 20),
            "trials_by_phase": {
                "Phase 1": np.random.randint(1, 5),
                "Phase 2": np.random.randint(2, 8),
                "Phase 3": np.random.randint(1, 5),
                "Phase 4": np.random.randint(0, 3)
            },
            "ongoing_trials": [
                {
                    "trial_id": f"NCT{10000000 + i}",
                    "indication": indication,
                    "phase": phase,
                    "status": "Recruiting",
                    "sponsor": f"Institution {i}"
                }
                for i, indication, phase in [
                    (1, "Type 2 Diabetes", "Phase 3"),
                    (2, "Cardiovascular Disease", "Phase 2"),
                    (3, "Chronic Kidney Disease", "Phase 2")
                ]
            ]
        }


    @staticmethod
    def get_scientific_literature(molecule: str) -> Dict:
        """Mock scientific literature data"""
        return {
            "molecule": molecule,
            "total_publications": np.random.randint(100, 500),
            "recent_publications": [
                {
                    "title": f"Novel mechanisms of {molecule} in disease X",
                    "authors": "Smith, J. et al.",
                    "journal": "Nature Medicine",
                    "year": 2024,
                    "relevance_score": 0.92
                },
                {
                    "title": f"Clinical efficacy of {molecule} in patient population Y",
                    "authors": "Johnson, A. et al.",
                    "journal": "JAMA",
                    "year": 2024,
                    "relevance_score": 0.85
                }
            ],
            "research_trends": ["Combination therapies", "Personalized medicine", "Novel dosage forms"]
        }



# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR (Master Agent Logic)
# ═══════════════════════════════════════════════════════════════════════════════


class PharmaOrchestrator:
    """Master orchestrator that coordinates all worker agents"""


    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=settings.llm_temperature
        )
        self.results = {}
        self.task_history = []


    def decompose_query(self, query: SearchQuery) -> Dict[str, List[str]]:
        """Decompose user query into subtasks"""


        task_mapping = {
            "unmet_needs": [
                "patent_analysis",
                "clinical_trials_analysis",
                "scientific_literature",
                "market_analysis",
                "synthesis"
            ],
            "clinical_trials": [
                "clinical_trials_analysis",
                "scientific_literature",
                "synthesis"
            ],
            "repurposing": [
                "patent_analysis",
                "scientific_literature",
                "clinical_trials_analysis",
                "market_analysis",
                "synthesis"
            ],
            "patent_landscape": [
                "patent_analysis",
                "market_analysis",
                "synthesis"
            ]
        }


        tasks = task_mapping.get(query.query_type, task_mapping["unmet_needs"])


        return {
            "query_type": query.query_type,
            "molecule": query.molecule_name,
            "tasks": tasks,
            "priority": "high" if query.query_type == "patent_landscape" else "normal"
        }


    def execute_parallel_tasks(self, query: SearchQuery, task_plan: Dict) -> Dict[str, TaskResult]:
        """Execute agent tasks in parallel"""


        results = {}
        logger.info(f"Executing tasks for {query.molecule_name}: {task_plan['tasks']}")


        # Execute each task
        if "market_analysis" in task_plan["tasks"]:
            results["market"] = TaskResult(
                agent_name="IQVIA Insights Agent",
                status="completed",
                data=MockDataGenerator.get_market_data(query.molecule_name),
                timestamp=datetime.now().isoformat()
            )


        if "patent_analysis" in task_plan["tasks"]:
            results["patents"] = TaskResult(
                agent_name="Patent Landscape Agent",
                status="completed",
                data=MockDataGenerator.get_patent_data(query.molecule_name),
                timestamp=datetime.now().isoformat()
            )


        if "clinical_trials_analysis" in task_plan["tasks"]:
            results["clinical_trials"] = TaskResult(
                agent_name="Clinical Trials Agent",
                status="completed",
                data=MockDataGenerator.get_clinical_trial_data(query.molecule_name),
                timestamp=datetime.now().isoformat()
            )


        if "scientific_literature" in task_plan["tasks"]:
            results["literature"] = TaskResult(
                agent_name="Web Intelligence Agent",
                status="completed",
                data=MockDataGenerator.get_scientific_literature(query.molecule_name),
                timestamp=datetime.now().isoformat()
            )


        return results


    def synthesize_findings(self, query: SearchQuery, results: Dict[str, TaskResult]) -> Dict:
        """Synthesize findings and generate recommendations"""


        synthesis = {
            "molecule": query.molecule_name,
            "analysis_type": query.query_type,
            "timestamp": datetime.now().isoformat(),
            "summary": f"Comprehensive analysis of {query.molecule_name}",
            "key_findings": [],
            "opportunities": [],
            "risks": [],
            "recommendations": []
        }


        # Synthesize from market data
        if "market" in results:
            market_data = results["market"].data
            synthesis["market_analysis"] = market_data
            synthesis["key_findings"].append(f"Market size: {market_data['current_market_size']}")
            synthesis["key_findings"].append(f"Growth rate: {market_data['market_growth_rate']}")


        # Synthesize from patents
        if "patents" in results:
            patent_data = results["patents"].data
            synthesis["patent_analysis"] = patent_data
            synthesis["key_findings"].append(f"Freedom to operate: {patent_data['freedom_to_operate']}")
            if float(patent_data["freedom_to_operate"]) < 0.7:
                synthesis["risks"].append("Patent landscape crowded - freedom-to-operate concerns")


        # Synthesize from clinical trials
        if "clinical_trials" in results:
            trial_data = results["clinical_trials"].data
            synthesis["clinical_trials"] = trial_data
            synthesis["key_findings"].append(f"Ongoing trials: {trial_data['total_trials']}")


        # Generate recommendations
        synthesis["recommendations"] = [
            "Conduct detailed competitive analysis for target indications",
            "Explore combination therapy opportunities",
            "Evaluate alternative dosage forms (patch, spray, extended-release)",
            "Assess pediatric and geriatric population needs",
            "Review regulatory pathways for accelerated approval"
        ]


        return synthesis


    def generate_report(self, query: SearchQuery, synthesis: Dict) -> str:
        """Generate PDF report"""


        report_id = str(uuid.uuid4())[:8]
        report_filename = f"pharma_research_{query.molecule_name}_{report_id}.pdf"
        report_path = settings.reports_dir / report_filename


        # Create PDF
        doc = SimpleDocTemplate(str(report_path), pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()


        # Header with branding
        elements.append(Paragraph(
            f"<b>💊 PharmaRep Master</b>",
            styles['Heading3']
        ))
        elements.append(Paragraph(
            f"<i>Advanced Pharmaceutical Intelligence Platform</i>",
            styles['Normal']
        ))
        elements.append(Spacer(1, 6))


        # Title
        title = Paragraph(
            f"<b>Advanced Pharmaceutical Intelligence Analysis: {query.molecule_name}</b>",
            styles['Heading1']
        )
        elements.append(title)
        elements.append(Spacer(1, 12))


        # Executive Summary
        elements.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
        elements.append(Paragraph(synthesis["summary"], styles['BodyText']))
        elements.append(Spacer(1, 12))


        # Key Findings
        elements.append(Paragraph("<b>Key Findings</b>", styles['Heading2']))
        for finding in synthesis["key_findings"]:
            elements.append(Paragraph(f"• {finding}", styles['BodyText']))
        elements.append(Spacer(1, 12))


        # Opportunities
        if synthesis["opportunities"]:
            elements.append(Paragraph("<b>Opportunities</b>", styles['Heading2']))
            for opp in synthesis["opportunities"]:
                elements.append(Paragraph(f"• {opp}", styles['BodyText']))
            elements.append(Spacer(1, 12))


        # Risks
        if synthesis["risks"]:
            elements.append(Paragraph("<b>Risk Assessment</b>", styles['Heading2']))
            for risk in synthesis["risks"]:
                elements.append(Paragraph(f"⚠️ {risk}", styles['BodyText']))
            elements.append(Spacer(1, 12))


        # Recommendations
        elements.append(Paragraph("<b>Recommendations</b>", styles['Heading2']))
        for i, rec in enumerate(synthesis["recommendations"], 1):
            elements.append(Paragraph(f"{i}. {rec}", styles['BodyText']))


        # Footer with branding
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(
            f"<i>Report generated by PharmaRep Master: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"<i>© 2024 PharmaRep Master - Advanced Pharmaceutical Intelligence Platform</i>",
            styles['Normal']
        ))


        # Build PDF
        doc.build(elements)
        logger.info(f"PDF report generated: {report_path}")


        return str(report_path)


    async def process_query(self, query: SearchQuery) -> ResearchReport:
        """Main orchestration method"""


        task_id = str(uuid.uuid4())
        logger.info(f"Processing query {task_id}: {query.molecule_name}")


        # Step 1: Decompose query
        task_plan = self.decompose_query(query)
        logger.info(f"Task plan: {task_plan}")


        # Step 2: Execute parallel tasks
        results = self.execute_parallel_tasks(query, task_plan)
        logger.info(f"Completed {len(results)} agent tasks")


        # Step 3: Synthesize findings
        synthesis = self.synthesize_findings(query, results)


        # Step 4: Generate report
        pdf_path = self.generate_report(query, synthesis)


        # Create final report object
        report = ResearchReport(
            task_id=task_id,
            molecule=query.molecule_name,
            timestamp=datetime.now().isoformat(),
            findings=synthesis,
            pdf_path=pdf_path,
            recommendations=synthesis["recommendations"]
        )


        self.results[task_id] = report
        logger.info(f"Query processing completed: {task_id}")


        return report



# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════


app = FastAPI(
    title="PharmaRep Master",
    description="Advanced pharmaceutical intelligence and research analysis platform",
    version="1.0.0"
)


orchestrator = PharmaOrchestrator()



@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PharmaRep Master",
        "timestamp": datetime.now().isoformat()
    }



@app.post("/search")
async def search_innovation_opportunities(query: SearchQuery) -> Dict:
    """
    Main search endpoint for pharma innovation analysis


    Example queries:
    - Find unmet needs for a molecule
    - Analyze clinical trial landscape
    - Evaluate repurposing opportunities
    - Assess patent landscape
    """


    try:
        logger.info(f"Received query: {query.molecule_name}")


        # Process query through orchestrator
        report = await orchestrator.process_query(query)


        return {
            "task_id": report.task_id,
            "molecule": report.molecule,
            "status": "completed",
            "findings": report.findings,
            "pdf_url": f"/reports/{Path(report.pdf_path).name}",
            "recommendations": report.recommendations,
            "timestamp": report.timestamp
        }


    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/task/{task_id}")
async def get_task_status(task_id: str) -> Dict:
    """Get status of a specific analysis task"""


    if task_id in orchestrator.results:
        report = orchestrator.results[task_id]
        return {
            "task_id": task_id,
            "status": "completed",
            "molecule": report.molecule,
            "pdf_url": f"/reports/{Path(report.pdf_path).name}" if report.pdf_path else None
        }


    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")



@app.get("/reports/{filename}")
async def download_report(filename: str):
    """Download a generated report PDF"""


    file_path = settings.reports_dir / filename
    if file_path.exists():
        return file_path


    raise HTTPException(status_code=404, detail=f"Report {filename} not found")



if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHARMAREP MASTER")
    print("="*80)
    print("\n🚀 Starting Uvicorn server...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("🔍 Try queries at: http://localhost:8000/search")
    print("\n" + "="*80 + "\n")


    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
