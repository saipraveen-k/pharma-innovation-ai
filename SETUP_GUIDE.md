# Pharma Innovation AI - Complete Setup Guide

## 📦 Project Structure

```
pharma-innovation-ai/
├── pharma_ai_main.py           # FastAPI Backend (main server)
├── config.py                   # Configuration settings ✅ NEW
├── streamlit_app.py            # Streamlit Frontend ✅ UPDATED
├── index.html                  # HTML Frontend (alternative)
├── reports/                    # Generated PDF reports
├── data/                       # Data files
├── logs/                       # Log files
└── .env                        # Environment variables (create this)
```

---

## 🚀 QUICK START (3 STEPS)

### Step 1: Install Dependencies

```bash
# Install all required packages
pip install fastapi uvicorn langchain langchain-openai pydantic reportlab pandas numpy streamlit requests python-dotenv
```

### Step 2: Configure Environment

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
LLM_MODEL=gpt-4
```

Or set environment variable in PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
```

### Step 3: Run Both Servers

**Terminal 1 - Start FastAPI Backend:**
```bash
python pharma_ai_main.py
```
Expected output:
```
════════════════════════════════════════════
PHARMA INNOVATION AGENTIC AI SYSTEM
════════════════════════════════════════════
🚀 Starting Uvicorn server...
📍 API Documentation: http://localhost:8000/docs
🔍 Try queries at: http://localhost:8000/search
════════════════════════════════════════════
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run streamlit_app.py
```
Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 🎯 USING THE STREAMLIT APP

### 1. **Open Streamlit**
   - Automatically opens at: `http://localhost:8501`
   - Or manually navigate there

### 2. **Enter Search Parameters**
   - **Molecule Name:** e.g., "Aspirin", "Metformin"
   - **Analysis Type:** Choose from 4 options
   - **Indication (optional):** e.g., "Type 2 Diabetes"
   - **Geographic Focus (optional):** e.g., "North America"

### 3. **Click "🚀 Analyze Innovation Opportunity"**
   - Shows loading spinner while processing
   - Results appear after analysis completes

### 4. **View Results**
   - **📊 Top Metrics:** Molecule, Type, Task ID, Status (4 columns)
   - **📈 Market Metrics:** Size, Growth Rate, Unmet Score (3 columns)
   - **📜 Patent Data:** Total, Active, Freedom to Operate (3 columns)
   - **🏥 Clinical Trials:** Ongoing Trials, Publications, Phase Distribution (3 columns)

### 5. **Explore Detailed Tabs**
   - **📊 Market Analysis:** Competitors, Top Indications
   - **📜 Patent Data:** Patent landscape and key patents
   - **🏥 Clinical Trials:** Trials by phase and ongoing studies
   - **🎯 Recommendations:** Strategic action items

### 6. **Download PDF Report**
   - Click **"📥 Download PDF Report"** button
   - PDF automatically downloads to your computer
   - Report includes all analysis, metrics, and recommendations

### 7. **View Search History**
   - Check sidebar for recent searches
   - Click to reload previous analyses

---

## 🔧 FIXES IMPLEMENTED

### ✅ Metrics Display Fixed
- **Before:** Metrics scattered in confusing grid
- **After:** Organized in 3 clear rows
  - Row 1: Market Analysis (3 metrics)
  - Row 2: Patent Analysis (3 metrics)
  - Row 3: Clinical Trials (3 metrics)

### ✅ PDF Download Fixed
- **Before:** Link didn't work properly
- **After:** 
  - Streamlit's native `st.download_button()` for direct download
  - Checks multiple possible file locations
  - Shows file details and timestamp
  - Browser open option as fallback

### ✅ Better Layout
- Added emoji icons to metrics for clarity
- Improved spacing with dividers
- Color-coded sections
- Better visual hierarchy

---

## 🌐 API ENDPOINTS (for reference)

### Health Check
```bash
GET http://localhost:8000/
```

### Search Analysis
```bash
POST http://localhost:8000/search
Content-Type: application/json

{
  "molecule_name": "Aspirin",
  "query_type": "unmet_needs",
  "indication": null,
  "geographic_focus": null
}
```

### Get Task Status
```bash
GET http://localhost:8000/task/{task_id}
```

### Download Report
```bash
GET http://localhost:8000/reports/{filename}
```

---

## 📋 EXAMPLE WORKFLOW

```
1. Open Streamlit: http://localhost:8501
   ↓
2. Enter: Molecule="Aspirin", Type="Unmet Needs Analysis"
   ↓
3. Click Analyze → Wait 5-10 seconds
   ↓
4. See Results:
   - Market size: $250M
   - Growth rate: 12.5%
   - Total patents: 28
   - Ongoing trials: 8
   - Key findings and recommendations
   ↓
5. Explore Tabs:
   - Market competitors
   - Patent landscape
   - Clinical trial details
   - Strategic recommendations
   ↓
6. Download PDF Report
   - Click "Download PDF"
   - File saves to Downloads
   ↓
7. Check History
   - Sidebar shows recent searches
   - Click to reload analysis
```

---

## 🐛 TROUBLESHOOTING

### Error: "Cannot connect to API"
**Solution:**
```bash
# Make sure FastAPI is running in Terminal 1
python pharma_ai_main.py
```

### Error: "PDF file not found"
**Solution:**
```bash
# Create reports directory
mkdir reports

# Check if PDF was generated
ls reports/
```

### Error: "Module not found"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
# Or install individually
pip install streamlit requests pandas fastapi uvicorn langchain
```

### Error: "OPENAI_API_KEY not set"
**Solution:**
```bash
# Set in PowerShell
$env:OPENAI_API_KEY="sk-your-key"

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### Streamlit takes too long to load results
**Solution:**
- Increase timeout in `streamlit_app.py` line ~143: `timeout=60`
- Check internet connection
- Verify OpenAI API is working

---

## 📊 FILE SIZES & PERFORMANCE

| File | Size | Purpose |
|------|------|---------|
| `pharma_ai_main.py` | ~8KB | Backend API |
| `streamlit_app.py` | ~15KB | Frontend UI |
| `config.py` | ~1KB | Settings |
| `index.html` | ~30KB | Alternative UI |
| PDF Reports | ~500KB-1MB | Generated outputs |

---

## 🎨 FEATURES SUMMARY

| Feature | Status | Location |
|---------|--------|----------|
| FastAPI Backend | ✅ Complete | `pharma_ai_main.py` |
| Streamlit UI | ✅ Updated | `streamlit_app.py` |
| HTML UI | ✅ Available | `index.html` |
| PDF Generation | ✅ Working | Backend + download |
| Search History | ✅ Implemented | Sidebar |
| Market Analysis | ✅ Included | Tab 1 |
| Patent Data | ✅ Included | Tab 2 |
| Clinical Trials | ✅ Included | Tab 3 |
| Recommendations | ✅ Included | Tab 4 |

---

## 🚀 NEXT STEPS

### Phase 2 (Optional Enhancements):
1. **Database Integration** - Store search results permanently
2. **User Authentication** - Login/accounts
3. **Advanced Charts** - Plotly/matplotlib visualizations
4. **Export to Excel** - In addition to PDF
5. **Comparison Tool** - Compare multiple molecules
6. **Real Data Integration** - Connect to actual APIs (IQVIA, USPTO, PubMed)

### Deploy to Cloud:
1. **Streamlit Cloud** - Free hosting for Streamlit apps
2. **Heroku/Railway** - For FastAPI backend
3. **Docker** - Containerize both services
4. **AWS/GCP** - Enterprise deployment

---

## 📞 SUPPORT

### Common Issues:
- **API not starting?** Check if port 8000 is already in use
- **Streamlit won't load?** Try `streamlit run streamlit_app.py --logger.level=debug`
- **PDF not downloading?** Ensure `reports/` directory exists and is writable

### Test the API:
Visit: `http://localhost:8000/docs` for Swagger UI
- Fully interactive API documentation
- Test endpoints directly
- See request/response formats

---

## ✅ STATUS

**Backend:** ✅ Ready (`pharma_ai_main.py`)
**Frontend:** ✅ Ready (`streamlit_app.py`) 
**Config:** ✅ Ready (`config.py`)
**HTML UI:** ✅ Available (`index.html`)

**All files created and tested!** 🎉

Run:
```bash
# Terminal 1
python pharma_ai_main.py

# Terminal 2
streamlit run streamlit_app.py
```

That's it! 🚀
