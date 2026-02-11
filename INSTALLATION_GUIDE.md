# 📦 Installation & Setup Guide

Complete step-by-step guide to get **Aadhaar Insight AI** running on your machine.

---

## ⚡ Quick Start (5 minutes)

### For Windows Users (PowerShell)

```powershell
# 1. Navigate to project directory
cd "c:\project directory"
# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app1.py
```

### For Mac/Linux Users

```bash
# 1. Navigate to project directory
cd enrollment_dashboard

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app1.py
```

---

## 🔍 Detailed Installation

### Step 1: Prerequisites Check

**Windows:**
```powershell
python --version    # Should be 3.8+
pip --version
```

**Mac/Linux:**
```bash
python3 --version   # Should be 3.8+
pip3 --version
```

### Step 2: Create Virtual Environment

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy project cleanup

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Verify creation
ls venv  # Should show Scripts, Lib, pyvenv.cfg
```

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Verify creation
ls venv  # Should show bin, lib, pyvenv.cfg
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Mac/Linux (Bash/Zsh):**
```bash
source venv/bin/activate
```

**Verification:** You should see `(venv)` in your terminal prompt.

### Step 4: Upgrade pip

**All Platforms:**
```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt
```

**Individual package verification:**
```bash
pip list  # Shows all installed packages
```

### Step 6: Verify Installation

```bash
# Test imports
python -c "import streamlit; import pandas; import plotly; print('✅ All dependencies installed!')"
```

---

## 🎯 Running the Application

### First Time Run

```bash
streamlit run app1.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install Watchdog.
```

### Open in Browser
Navigate to `http://localhost:8501` or it should open automatically.

### Subsequent Runs

Simply run:
```bash
streamlit run app1.py
```

---

## 📊 Data Setup

### 1. Prepare Your Data

Ensure `unified_enrolment_data.csv` exists with required columns:

```csv
date,state,district,pincode,Total Enrolments,Total Updates,age_0_5,MBU_Gap_Index,Migration_Intensity,Weighted_Effort
```

### 2. Place in Project Directory

```
enrollment_dashboard/
├── app1.py
├── requirements.txt
├── unified_enrolment_data.csv  ← Place here
└── README.md
```

### 3. Verify Data Format

```bash
# Quick Python check
python -c "
import pandas as pd
df = pd.read_csv('unified_enrolment_data.csv')
print(f'Rows: {len(df)}')
print(f'Columns: {list(df.columns)}')
print(df.head())
"
```

---

## ⚙️ Configuration

### Streamlit Config (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#4e73df"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = false
maxUploadSize = 200
```

---

## 🚨 Troubleshooting

### Issue: Python not found

**Solution:**
```powershell
# Windows: Check Python installation
py --version

# If not in PATH, reinstall Python with "Add Python to PATH" option
```

### Issue: Virtual environment won't activate

**Windows PowerShell Error:** "cannot be loaded because running scripts is disabled"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: `pip install` fails

```bash
# Upgrade pip first
pip install --upgrade pip

# Then try again
pip install -r requirements.txt

# If still fails, install individually
pip install streamlit pandas plotly numpy scikit-learn statsmodels
```

### Issue: "No module named streamlit"

```bash
# Ensure virtual environment is activated (should see (venv) in prompt)
which python  # or 'where python' on Windows

# Should show path inside venv folder

# If not activated, activate it
```

### Issue: Port 8501 already in use

```bash
# Run on different port
streamlit run app1.py --server.port 8502
```

### Issue: App freezes or runs slowly

```bash
# Clear Streamlit cache
streamlit cache clear

# Run with reduced data
# Filter date range in sidebar to smaller period
```

---

## 🧹 Cleanup & Deactivation

### Deactivate Virtual Environment

```bash
# All platforms
deactivate
```

### Remove Virtual Environment (if needed)

```bash
# Windows
rmdir /s venv

# Mac/Linux
rm -rf venv
```

---

## 🔄 Development Workflow

### After Making Code Changes

1. **Save file** → Streamlit auto-reloads
2. **Click "Rerun"** if auto-reload doesn't work
3. **Check console** for error messages

### Example Workflow

```bash
# 1. Activate environment
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# 2. Run app
streamlit run app1.py

# 3. Make changes to app1.py
# (editor: make code changes)

# 4. Streamlit automatically reruns
# (app updates in browser)

# 5. When done, deactivate
deactivate
```

---

## 📝 Dependency Management

### Update a Package

```bash
pip install --upgrade streamlit
```

### Update All Packages

```bash
pip install -r requirements.txt --upgrade
```

### Generate requirements.txt from environment

```bash
pip freeze > requirements.txt
```

---

## ✅ Verification Checklist

Before reporting issues:

- [ ] Python version is 3.8+
- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] All packages installed successfully (`pip list`)
- [ ] `unified_enrolment_data.csv` exists in project folder
- [ ] CSV has required columns
- [ ] App runs: `streamlit run app1.py`
- [ ] Browser opens to `http://localhost:8501`
- [ ] Can filter data by date and state

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Plotly Charts](https://plotly.com/python/)
- [Scikit-learn ML](https://scikit-learn.org/stable/)
- [StatsModels Time Series](https://www.statsmodels.org/stable/tsa.html)

---

## 💡 Pro Tips

1. **Keep terminal open** to see debug messages
2. **Use Streamlit sidebar** for quick parameter tuning
3. **Cache expensive operations** with `@st.cache_data`
4. **Test with small datasets first** for quick iteration
5. **Use `streamlit run app1.py -- --logger.level=debug`** for verbose output

---

**Still Having Issues?** 

Ensure all steps are completed in order. If problems persist, create a fresh virtual environment and reinstall.

---

**Last Updated:** January 2025  
**Version:** 1.0.0
