"""
PharmaRep Master - Streamlit Dashboard
Advanced pharmaceutical intelligence and research analysis platform
"""


import streamlit as st
import requests
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import os
from config import settings


# Page configuration
st.set_page_config(
    page_title="PharmaRep Master",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS with HIGH CONTRAST - optimized for dark theme
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    
    /* Force bright text colors */
    body, div, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #1a4d4d 0%, #0d3333 100%);
        padding: 1.2rem;
        border-radius: 0.5rem;
        border-left: 5px solid #00CED1;
        box-shadow: 0 2px 8px rgba(0,206,209,0.3);
    }
    
    .stMetric label {
        color: #00FFD9 !important;
        font-weight: bold;
        font-size: 14px;
    }
    
    .stMetric [data-testid="metric-container"] {
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 28px;
    }
    
    .metric-row {
        margin-bottom: 1.5rem;
    }
    
    /* Headings */
    h1 {
        color: #00FFD9 !important;
        font-weight: bold;
    }
    
    h2 {
        color: #00CED1 !important;
        font-weight: bold;
    }
    
    h3 {
        color: #00CED1 !important;
    }
    
    h4 {
        color: #00FFD9 !important;
    }
    
    /* Input/Select styling */
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: #FFFFFF !important;
        border: 1px solid #00CED1 !important;
    }
    
    .stSelectbox select {
        background-color: #1a1a2e !important;
        color: #FFFFFF !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #008080 !important;
        color: #FFFFFF !important;
        border: 1px solid #00CED1 !important;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #00CED1 !important;
        color: #000000 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stSuccess {
        background-color: #0d3f1f !important;
        color: #00FF88 !important;
    }
    
    .stError {
        background-color: #3f0d0d !important;
        color: #FF6B6B !important;
    }
    
    .stWarning {
        background-color: #3f2f0d !important;
        color: #FFD700 !important;
    }
    
    .stInfo {
        background-color: #0d1f3f !important;
        color: #87CEEB !important;
    }
    
    /* Text styling */
    p {
        color: #FFFFFF !important;
    }
    
    /* Tables */
    .streamlit-expanderHeader {
        background-color: #1a4d4d !important;
        color: #00FFD9 !important;
    }
    
    /* Divider */
    hr {
        border-color: #00CED1 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        color: #FFFFFF !important;
        background-color: #0d1a1a !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #008080 !important;
        color: #00FFD9 !important;
        border-bottom: 3px solid #00CED1 !important;
    }
    
    /* Sidebar */
    .sidebar {
        background-color: #0d1a1a !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #B0E0E6 !important;
    }
    
    </style>
""", unsafe_allow_html=True)


# API Configuration
API_BASE_URL = "http://localhost:8000"
REPORTS_DIR = Path.cwd() / "reports"


# Ensure reports directory exists
REPORTS_DIR.mkdir(exist_ok=True)


# Initialize session state
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "search_history" not in st.session_state:
    st.session_state.search_history = []


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════


st.markdown("# <span style='color:#00FFD9; font-weight: bold;'>💊 PharmaRep Master</span>", unsafe_allow_html=True)
st.markdown("<span style='color:#00CED1; font-size: 16px;'>*Advanced Pharmaceutical Intelligence Platform*</span>", unsafe_allow_html=True)
st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════


with st.sidebar:
    st.markdown("## <span style='color:#00FFD9'>⚙️ Configuration</span>", unsafe_allow_html=True)
    st.markdown(f"**API URL:** `{API_BASE_URL}`")
    
    # API Status
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected", icon="✅")
        else:
            st.error("❌ API Connection Failed")
    except:
        st.error("❌ Cannot reach API", icon="❌")
    
    st.divider()
    
    # History
    st.markdown("## <span style='color:#00FFD9'>📋 Recent Searches</span>", unsafe_allow_html=True)
    if st.session_state.search_history:
        for i, search in enumerate(st.session_state.search_history[-5:]):
            if st.button(
                f"📌 {search['molecule']} - {search['query_type']}",
                key=f"history_{i}"
            ):
                st.session_state.search_results = search['results']
                st.rerun()
    else:
        st.caption("No recent searches")
    
    st.divider()
    
    # About
    st.markdown("## <span style='color:#00FFD9'>ℹ️ About</span>", unsafe_allow_html=True)
    st.caption(
        "PharmaRep Master analyzes pharmaceutical innovation opportunities using "
        "market data, patent landscapes, clinical trials, and scientific literature."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH SECTION
# ═══════════════════════════════════════════════════════════════════════════════


col1, col2 = st.columns([2, 1])


with col1:
    st.markdown("## <span style='color:#00FFD9'>🔍 Search Pharmaceutical Innovation</span>", unsafe_allow_html=True)


with col2:
    if st.button("🔄 Clear Results", use_container_width=True):
        st.session_state.search_results = None
        st.rerun()


st.markdown("### <span style='color:#00CED1'>Enter Analysis Parameters</span>", unsafe_allow_html=True)


col1, col2 = st.columns(2)


with col1:
    molecule_name = st.text_input(
        "Molecule Name *",
        placeholder="e.g., Aspirin, Metformin, Lisinopril",
        help="Enter the pharmaceutical compound name"
    )


with col2:
    query_type = st.selectbox(
        "Analysis Type *",
        options=[
            "unmet_needs",
            "clinical_trials",
            "repurposing",
            "patent_landscape"
        ],
        format_func=lambda x: {
            "unmet_needs": "🎯 Unmet Needs Analysis",
            "clinical_trials": "🏥 Clinical Trials Landscape",
            "repurposing": "♻️ Drug Repurposing Opportunities",
            "patent_landscape": "📜 Patent Landscape Analysis"
        }.get(x, x),
        help="Select the type of pharmaceutical analysis"
    )


col1, col2 = st.columns(2)


with col1:
    indication = st.text_input(
        "Indication (Optional)",
        placeholder="e.g., Type 2 Diabetes, Hypertension",
        help="Medical condition or disease indication"
    )


with col2:
    geographic_focus = st.text_input(
        "Geographic Focus (Optional)",
        placeholder="e.g., North America, Europe, Global",
        help="Geographic region for analysis"
    )


# Search Button
col1, col2, col3 = st.columns([2, 1, 1])


with col1:
    search_button = st.button(
        "🚀 Analyze Innovation Opportunity",
        use_container_width=True,
        type="primary"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE SEARCH
# ═══════════════════════════════════════════════════════════════════════════════


if search_button:
    if not molecule_name or not query_type:
        st.error("❌ Please fill in required fields (Molecule Name and Analysis Type)")
    else:
        query = {
            "molecule_name": molecule_name,
            "query_type": query_type,
            "indication": indication if indication else None,
            "geographic_focus": geographic_focus if geographic_focus else None
        }
        
        with st.spinner("🔬 Analyzing pharmaceutical innovation landscape..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/search",
                    json=query,
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json()
                    st.session_state.search_results = results
                    
                    st.session_state.search_history.append({
                        "molecule": molecule_name,
                        "query_type": query_type,
                        "timestamp": datetime.now().isoformat(),
                        "results": results
                    })
                    
                    st.success(f"✅ Analysis completed for {molecule_name}")
                    st.rerun()
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.error(response.text)
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
                st.info("Make sure FastAPI is running: `python pharma_ai_main.py`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY RESULTS
# ═══════════════════════════════════════════════════════════════════════════════


if st.session_state.search_results:
    results = st.session_state.search_results
    findings = results["findings"]
    
    st.divider()
    st.markdown("## <span style='color:#00FFD9'>📊 Analysis Results</span>", unsafe_allow_html=True)
    
    # Result Header - 4 Metrics in One Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🧬 Molecule",
            results["molecule"],
            delta="✓ Complete"
        )
    
    with col2:
        st.metric(
            "📋 Analysis Type",
            findings["analysis_type"].replace("_", " ").title(),
            delta="✓ Ready"
        )
    
    with col3:
        st.metric(
            "🔢 Task ID",
            results["task_id"][:8]
        )
    
    with col4:
        st.metric(
            "✅ Status",
            results["status"]
        )
    
    st.markdown("<div class='metric-row'></div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MARKET & INNOVATION METRICS - 3 ROWS OF 3 METRICS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    st.markdown("### <span style='color:#00FFD9'>📈 Market & Innovation Metrics</span>", unsafe_allow_html=True)
    
    # Row 1: Market Analysis
    if "market_analysis" in findings:
        market = findings["market_analysis"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💰 Market Size",
                market.get("current_market_size", "N/A")
            )
        
        with col2:
            st.metric(
                "📊 Growth Rate",
                market.get("market_growth_rate", "N/A")
            )
        
        with col3:
            unmet_score = market.get("unmet_needs_score", 0)
            score_pct = f"{unmet_score:.1%}" if isinstance(unmet_score, (int, float)) else unmet_score
            st.metric(
                "🎯 Unmet Needs Score",
                score_pct
            )
        
        st.markdown("<div class='metric-row'></div>", unsafe_allow_html=True)
    
    # Row 2: Patent Analysis
    if "patent_analysis" in findings:
        patent = findings["patent_analysis"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📜 Total Patents",
                patent.get("total_patents", "N/A")
            )
        
        with col2:
            st.metric(
                "✅ Active Patents",
                patent.get("active_patents", "N/A")
            )
        
        with col3:
            st.metric(
                "🔓 Freedom to Operate",
                patent.get("freedom_to_operate", "N/A")
            )
        
        st.markdown("<div class='metric-row'></div>", unsafe_allow_html=True)
    
    # Row 3: Clinical Trials
    if "clinical_trials" in findings:
        trials = findings["clinical_trials"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🏥 Ongoing Trials",
                trials.get("total_trials", "N/A")
            )
        
        with col2:
            st.metric(
                "📚 Total Publications",
                findings.get("scientific_literature", {}).get("total_publications", "N/A")
            )
        
        with col3:
            st.metric(
                "🔬 Phase Distribution",
                f"1:{trials['trials_by_phase'].get('Phase 1', 0)} 2:{trials['trials_by_phase'].get('Phase 2', 0)} 3:{trials['trials_by_phase'].get('Phase 3', 0)}"
            )
        
        st.markdown("<div class='metric-row'></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # KEY FINDINGS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    st.markdown("### <span style='color:#00FFD9'>📋 Key Findings</span>", unsafe_allow_html=True)
    
    if findings.get("key_findings"):
        for finding in findings["key_findings"]:
            st.success(f"✓ {finding}")
    else:
        st.info("No key findings available")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # DETAILED ANALYSIS TABS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Market Analysis", "📜 Patent Data", "🏥 Clinical Trials", "🎯 Recommendations"]
    )
    
    with tab1:
        if "market_analysis" in findings:
            market = findings["market_analysis"]
            st.markdown("#### <span style='color:#00CED1'>Market Overview</span>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Competitors:**")
                if "competitors" in market:
                    competitors_df = pd.DataFrame(market["competitors"])
                    st.dataframe(competitors_df, use_container_width=True)
            
            with col2:
                st.write("**Top Indications:**")
                if "top_indications" in market:
                    indications_df = pd.DataFrame(market["top_indications"])
                    st.dataframe(indications_df, use_container_width=True)
        else:
            st.info("No market analysis data available")
    
    with tab2:
        if "patent_analysis" in findings:
            patent = findings["patent_analysis"]
            st.markdown("#### <span style='color:#00CED1'>Patent Landscape</span>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Patents", patent.get("total_patents", "N/A"))
                st.metric("Active Patents", patent.get("active_patents", "N/A"))
            
            with col2:
                st.metric("Freedom to Operate", patent.get("freedom_to_operate", "N/A"))
            
            st.write("**Key Patents:**")
            if "key_patents" in patent:
                patents_df = pd.DataFrame(patent["key_patents"])
                st.dataframe(patents_df, use_container_width=True)
        else:
            st.info("No patent analysis data available")
    
    with tab3:
        if "clinical_trials" in findings:
            trials = findings["clinical_trials"]
            st.markdown("#### <span style='color:#00CED1'>Clinical Trial Landscape</span>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Phase 1", trials["trials_by_phase"].get("Phase 1", 0))
            with col2:
                st.metric("Phase 2", trials["trials_by_phase"].get("Phase 2", 0))
            with col3:
                st.metric("Phase 3", trials["trials_by_phase"].get("Phase 3", 0))
            with col4:
                st.metric("Phase 4", trials["trials_by_phase"].get("Phase 4", 0))
            
            st.write("**Ongoing Trials:**")
            if "ongoing_trials" in trials:
                trials_df = pd.DataFrame(trials["ongoing_trials"])
                st.dataframe(trials_df, use_container_width=True)
        else:
            st.info("No clinical trial data available")
    
    with tab4:
        st.markdown("#### <span style='color:#00CED1'>Strategic Recommendations</span>", unsafe_allow_html=True)
        
        if results.get("recommendations"):
            for i, rec in enumerate(results["recommendations"], 1):
                st.info(f"**{i}.** {rec}")
        else:
            st.info("No recommendations available")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # RISKS SECTION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    if findings.get("risks"):
        st.markdown("### <span style='color:#FF6B6B'>⚠️ Risk Assessment</span>", unsafe_allow_html=True)
        for risk in findings["risks"]:
            st.warning(f"⚠️ {risk}")
        st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PDF DOWNLOAD SECTION - FIXED (DUAL METHOD)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    st.markdown("### <span style='color:#00FFD9'>📄 Report Download</span>", unsafe_allow_html=True)
    
    pdf_url = results.get("pdf_url", "")
    if pdf_url:
        try:
            pdf_filename = Path(pdf_url).name
            
            # Try multiple locations for the PDF
            possible_paths = [
                settings.reports_dir / pdf_filename,  # Config-based path
                REPORTS_DIR / pdf_filename,           # Local reports dir
                Path(pdf_url),                        # Direct path if absolute
            ]
            
            pdf_path = None
            for path in possible_paths:
                if path.exists():
                    pdf_path = path
                    break
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.success("✅ PDF Report Generated")
                st.markdown("""
                **Download Full Report**
                - Comprehensive PDF with detailed analysis
                - Market insights and recommendations
                - Patent landscape assessment
                - Clinical trial overview
                """)
                
                if pdf_path:
                    # ✅ METHOD 1: Direct file download (RECOMMENDED)
                    try:
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=pdf_file.read(),
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"❌ Error reading file: {str(e)}")
                else:
                    # ✅ METHOD 2: Download from API endpoint (FALLBACK)
                    st.info("📥 Downloading from API...")
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}{pdf_url}",
                            timeout=30
                        )
                        if response.status_code == 200:
                            st.download_button(
                                label="📥 Download PDF Report (from API)",
                                data=response.content,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.warning(f"⚠️ API returned status {response.status_code}")
                            st.info("Try opening in browser: [Click here to open]("+f"{API_BASE_URL}{pdf_url}"+")")
                    except Exception as e:
                        st.error(f"❌ API download error: {str(e)}")
            
            with col2:
                st.markdown("**Report Details**")
                st.caption(f"**File:** `{pdf_filename}`")
                st.caption(f"**URL:** `/reports/{pdf_filename}`")
                st.caption(f"**Generated:** {results.get('timestamp', 'Unknown')}")
                
                if st.button("🌐 Open in Browser", use_container_width=True):
                    st.info(f"[Click here to open PDF]({API_BASE_URL}{pdf_url})")
        
        except Exception as e:
            st.error(f"❌ Error with PDF download: {str(e)}")
    else:
        st.warning("⚠️ No PDF URL available")
    
    st.divider()
    
    # Raw JSON Data (for developers)
    with st.expander("🔧 Raw JSON Data"):
        st.json(results)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════


st.divider()
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='color: #00FFD9; font-weight: bold; font-size: 18px;'>💊 PharmaRep Master</p>
        <p style='color: #00CED1; font-size: 0.9rem;'>Powered by LangChain, FastAPI & Streamlit</p>
        <p style='color: #B0E0E6; font-size: 0.8rem;'>© 2024 Advanced Pharmaceutical Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)
