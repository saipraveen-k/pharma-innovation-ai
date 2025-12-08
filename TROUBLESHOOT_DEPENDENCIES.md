# TROUBLESHOOTING: DEPENDENCY INSTALLATION ISSUES

## Problem You're Facing

```
ERROR: Could not find a version that satisfies the requirement httpx_mock==0.25.2
ERROR: Ignored the following versions that require a different python version
```

This happens because:
1. **Python version mismatch** - Some packages require Python 3.11+ but you may have 3.9 or 3.10
2. **Package version conflicts** - httpx_mock 0.25.2 may not exist or be incompatible
3. **Dependency resolution** - pip can't resolve all version constraints simultaneously

---

## SOLUTION: Step-by-Step Fix

### Step 1: Check Your Python Version
```bash
python --version
```

**Expected Output:**
```
Python 3.9.x, 3.10.x, or 3.11.x
```

If you have Python 3.8 or lower:
```bash
# Install Python 3.11 (recommended)
# macOS
brew install python@3.11

# Linux (Ubuntu)
sudo apt-get install python3.11

# Windows
# Download from python.org
```

---

### Step 2: Use the Fixed Requirements File

I've created `requirements_fixed.txt` with corrected versions:

```bash
# Replace the old requirements.txt
cp requirements_fixed.txt requirements.txt

# Reinstall dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

---

### Step 3: If Still Having Issues - Install Step by Step

**Option A: Install core packages first**
```bash
# Step 1: Install essentials
pip install fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.5.0

# Step 2: Verify installation
python -c "import fastapi; print('✅ FastAPI installed')"

# Step 3: Install data packages
pip install pandas==2.1.3 numpy==1.26.2

# Step 4: Install database packages
pip install sqlalchemy==2.0.23 psycopg2-binary==2.9.9 redis==5.0.1

# Step 5: Install AI packages
pip install openai==1.3.0 langchain==0.0.339

# Step 6: Install testing packages
pip install pytest==7.4.3 pytest-asyncio==0.21.1 pytest-cov==4.1.0 httpx==0.25.2

# Step 7: Install monitoring
pip install prometheus-client==0.19.0

# Step 8: Verify all imports
python -c "
import fastapi
import sqlalchemy
import pandas
import openai
import pytest
print('✅ All core packages installed successfully!')
"
```

**Option B: Install minimal + upgrade incrementally**
```bash
# Fresh start
pip install --upgrade pip

# Install absolute essentials only
pip install \
  fastapi==0.104.1 \
  uvicorn==0.24.0 \
  pydantic==2.5.0 \
  sqlalchemy==2.0.23 \
  psycopg2-binary==2.9.9 \
  openai==1.3.0 \
  pytest==7.4.3

# Test this works
python pharma_ai_main.py

# Then add more as needed
pip install pandas numpy matplotlib plotly
```

---

### Step 4: If httpx_mock Still Fails

httpx_mock 0.25.2 may be too specific. Try:

```bash
# Option 1: Use latest httpx_mock
pip install httpx-mock --upgrade

# Option 2: Use httpx directly (no mock)
pip install httpx==0.25.2

# Option 3: Skip mocking for now
# Remove httpx_mock from requirements.txt
# Use pytest-mock instead:
pip install pytest-mock==3.12.0
```

Update your test file to use pytest-mock:
```python
# Instead of httpx_mock, use pytest-mock
import pytest
from unittest.mock import patch, MagicMock

def test_search(mocker):
    """Test with mock instead of httpx_mock"""
    mock_requests = mocker.patch('requests.get')
    mock_requests.return_value.json.return_value = {"trials": [...]}
    
    # Your test code
    assert True
```

---

### Step 5: Create Minimal Requirements File (If All Else Fails)

**File: `requirements_minimal.txt`**
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
openai==1.3.0
langchain==0.0.339
requests==2.31.0
pandas==2.1.3
numpy==1.26.2
pytest==7.4.3
pytest-asyncio==0.21.1
python-dotenv==1.0.0
prometheus-client==0.19.0
```

Install minimal:
```bash
pip install -r requirements_minimal.txt
```

Then add packages one at a time as needed.

---

### Step 6: Verify Installation

**Quick test script:**
```bash
# Create: test_imports.py
python << 'EOF'
import sys
print(f"Python version: {sys.version}")

packages = [
    ("fastapi", "FastAPI"),
    ("pydantic", "Pydantic"),
    ("sqlalchemy", "SQLAlchemy"),
    ("pandas", "Pandas"),
    ("openai", "OpenAI"),
    ("pytest", "Pytest"),
    ("redis", "Redis"),
]

failed = []
for module, name in packages:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError as e:
        print(f"❌ {name}: {e}")
        failed.append(name)

if failed:
    print(f"\n⚠️ Failed to import: {', '.join(failed)}")
    print("Run: pip install -r requirements_fixed.txt")
else:
    print("\n🎉 All packages installed successfully!")
EOF
```

Run it:
```bash
python test_imports.py
```

---

## SPECIFIC FIXES FOR YOUR ERROR

### For: `httpx_mock==0.25.2` not found

**Solution:**
```bash
# Remove from requirements.txt or use this instead
pip install httpx==0.25.2
pip install pytest-mock==3.12.0

# Update your test to use pytest-mock (see Step 4)
```

### For: pytest-asyncio version mismatch

**Solution:**
```bash
# Your Python version needs to match
python --version  # Check version

# If Python 3.9 or 3.10:
pip install pytest-asyncio==0.21.1

# If Python 3.11+:
pip install pytest-asyncio==0.23.0
```

### For: General dependency conflicts

**Nuclear option - start fresh:**
```bash
# Deactivate and remove venv
deactivate
rm -rf venv/  # Windows: rmdir /s venv

# Create new venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install fresh
pip install --upgrade pip
pip install -r requirements_fixed.txt --no-cache-dir
```

---

## EXPECTED OUTPUT AFTER SUCCESS

```
Successfully installed:
✅ fastapi
✅ uvicorn
✅ pydantic
✅ sqlalchemy
✅ psycopg2-binary
✅ redis
✅ pandas
✅ numpy
✅ openai
✅ langchain
✅ pytest
✅ prometheus-client
[... and 30+ more packages ...]

Successfully installed 50 packages in 3.45s
```

---

## VERIFY IT WORKS

```bash
# Test import
python -c "import pharma_ai_main; print('✅ Ready to use!')"

# Test FastAPI
python pharma_ai_main.py
# Should show: Uvicorn running on http://127.0.0.1:8000

# In another terminal:
curl http://localhost:8000/
# Should return: {"status":"healthy"}
```

---

## STILL HAVING ISSUES?

Try this diagnostic:
```bash
# Show Python info
python -c "import sys; print(f'Python: {sys.version}'); print(f'Executable: {sys.executable}')"

# Show pip info
pip --version
pip list | grep -E "fastapi|sqlalchemy|pydantic"

# Try installing one package verbosely
pip install fastapi -v

# Check internet connection
pip index versions fastapi
```

---

**TL;DR Quick Fix:**
```bash
cp requirements_fixed.txt requirements.txt
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
python -c "import fastapi; print('✅ Success')"
```

---
