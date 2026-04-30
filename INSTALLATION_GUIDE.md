# Installation Guide - Mutual Fund FAQ Assistant

## ⚠️ Issue Detected

Python is not properly installed on your system or not added to PATH.

---

## Solution: Install Python

### Option 1: Install from python.org (Recommended)

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.10 or higher for Windows

2. **Install Python:**
   - Run the installer
   - ⚠️ **IMPORTANT:** Check ✅ "Add Python to PATH" during installation
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   - Open a NEW Command Prompt or PowerShell window
   - Run: `python --version`
   - You should see: `Python 3.10.x` or higher

---

### Option 2: Install from Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.10" or "Python 3.11"
3. Click "Install"
4. Verify: Open terminal and run `python --version`

---

## After Installing Python

### Quick Setup (Automated)

1. **Double-click:** `SETUP_AND_RUN.bat`
   - This will automatically:
     - Create virtual environment
     - Install all dependencies
     - Run Phase 1 setup

2. **Follow the prompts**

---

### Manual Setup

If you prefer manual setup:

```bash
# 1. Navigate to project
cd "c:\Users\Admin\Desktop\rag chat box"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate.bat

# 4. Install dependencies
cd "phase 1"
pip install -r requirements.txt

# 5. Run Phase 1 setup
cd src
python phase1_setup.py
```

---

## Configure API Key

After successful setup:

1. Open: `phase 1\.env`
2. Replace `your_groq_api_key_here` with your actual key
3. Get free API key from: https://console.groq.com

```env
GROQ_API_KEY=gsk_your_actual_api_key
```

---

## Verify Installation

Run these commands to verify:

```bash
# Check Python version
python --version

# Check if pip works
pip --version

# Test imports
python -c "import requests; import pandas; print('✅ All imports successful!')"
```

---

## Troubleshooting

### Issue: "python is not recognized"
**Solution:** 
- Reinstall Python
- Make sure to check "Add Python to PATH"
- Restart your terminal/computer

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Virtual environment not activating
**Solution:**
```bash
# Try PowerShell
cd "phase 1"
..\venv\Scripts\python.exe -m pip install -r requirements.txt
..\venv\Scripts\python.exe src\phase1_setup.py
```

---

## Next Steps After Setup

1. ✅ Install Python
2. ✅ Run `SETUP_AND_RUN.bat`
3. ✅ Configure GROQ_API_KEY in `.env`
4. ✅ Verify Phase 1 setup runs successfully
5. 🚀 Proceed to Phase 2 implementation

---

## Need Help?

1. Check logs in: `phase 1\logs\`
2. Review documentation in: `docs\`
3. Read: `phase 1\README.md`

---

**Python Download:** https://www.python.org/downloads/  
**Groq API:** https://console.groq.com
