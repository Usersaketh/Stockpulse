# 🛠️ Troubleshooting Guide

Common issues and solutions for StockPulse Data Pipeline.

## 🔍 Database Connection Issues

### Problem: "Database connection failed"

**Symptoms:**
```
❌ Database connection failed: (psycopg2.OperationalError) 
connection to server failed: FATAL: Tenant or user not found
```

**Solutions:**

1. **Check Supabase Credentials**
   ```bash
   # Verify .env file exists and has correct values
   cat .env
   ```

2. **Username Format Issue**
   ```env
   # Wrong ❌
   DB_USER=postgres
   
   # Correct ✅  
   DB_USER=postgres.your_project_ref
   ```

3. **Database Password**
   - Go to Supabase Dashboard → Settings → Database
   - Reset password if needed
   - Update `.env` file

4. **Host Configuration**
   ```env
   # For pooler connection (recommended)
   DB_HOST=aws-region.pooler.supabase.com
   DB_PORT=6543
   
   # For direct connection (alternative)
   DB_HOST=db.your-project.supabase.co  
   DB_PORT=5432
   ```

### Problem: "Host name could not be translated"

**Solution:**
Check your internet connection and Supabase host URL:
```bash
# Test DNS resolution
nslookup aws-1-ap-south-1.pooler.supabase.com
```

## 🐍 Python Environment Issues

### Problem: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'yfinance'
```

**Solutions:**

1. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   pip list | grep streamlit
   pip list | grep yfinance
   ```

### Problem: Python Version Compatibility

**Symptoms:**
```
SyntaxError: f-string expression part cannot include a backslash
```

**Solution:**
Ensure Python 3.8+ is installed:
```bash
python --version
# Should show Python 3.8.0 or higher
```

## 📊 Dashboard Issues

### Problem: Dashboard Won't Start

**Symptoms:**
```
Error while loading page
Streamlit server error
```

**Solutions:**

1. **Check Port Availability**
   ```bash
   # Kill existing Streamlit processes
   taskkill /f /im streamlit.exe  # Windows
   pkill -f streamlit  # macOS/Linux
   ```

2. **Use Different Port**
   ```bash
   streamlit run dashboard/app.py --server.port 8502
   ```

3. **Clear Cache**
   ```bash
   # Delete Streamlit cache
   rm -rf ~/.streamlit  # macOS/Linux
   rmdir /s %USERPROFILE%\.streamlit  # Windows
   ```

### Problem: "Column 'Daily_Return' not found"

**Solution:**
This indicates data loading issues. Run pipeline again:
```bash
python scripts/pipeline.py
```

### Problem: Charts Not Displaying

**Solutions:**

1. **Browser Compatibility**
   - Use Chrome, Firefox, or Edge
   - Disable ad blockers
   - Clear browser cache

2. **Check Data**
   ```python
   # Test data availability
   python scripts/debug_columns.py
   ```

## 📈 Data Pipeline Issues

### Problem: No Data Downloaded

**Symptoms:**
```
⚠️ No data found for RELIANCE.NS
Empty DataFrame returned
```

**Solutions:**

1. **Check Internet Connection**
   ```bash
   ping finance.yahoo.com
   ```

2. **Verify Ticker Symbols**
   ```python
   # Test individual stock download
   import yfinance as yf
   data = yf.download("RELIANCE.NS", period="5d")
   print(data)
   ```

3. **Update yfinance**
   ```bash
   pip install --upgrade yfinance
   ```

### Problem: Data Not Loading to Database

**Symptoms:**
```
❌ Failed to load RELIANCE_NS
Database error loading data
```

**Solutions:**

1. **Test Database Connection**
   ```bash
   python scripts/test_connection.py
   ```

2. **Check Table Permissions**
   - Verify Supabase project permissions
   - Ensure database user has write access

3. **Manual Data Verification**
   ```bash
   # Check if CSV files exist
   ls data/processed/
   
   # Verify CSV content
   head -5 data/processed/RELIANCE_NS_processed.csv
   ```

## 🔧 Configuration Issues

### Problem: Environment Variables Not Loaded

**Symptoms:**
```
❌ Missing database environment variables
DB_PASS: None
```

**Solutions:**

1. **Check .env File Location**
   ```bash
   # Must be in project root directory
   ls -la .env
   ```

2. **Verify .env Format**
   ```env
   # No spaces around = sign
   DB_USER=postgres.project_ref
   DB_PASS=your_password
   ```

3. **Load Environment Manually**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   import os
   print(os.getenv('DB_USER'))
   ```

## 🚀 Performance Issues

### Problem: Slow Dashboard Loading

**Solutions:**

1. **Clear Streamlit Cache**
   - Use Streamlit menu: "Clear cache"
   - Or restart dashboard

2. **Reduce Data Size**
   ```python
   # In dashboard/app.py, limit data
   query = f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT 100"
   ```

3. **Database Optimization**
   ```sql
   -- Add index for better performance
   CREATE INDEX idx_date ON stock_reliance_ns(date);
   ```

### Problem: High Memory Usage

**Solutions:**

1. **Optimize Data Loading**
   ```python
   # Load only required columns
   df = pd.read_csv(file, usecols=['Date', 'Close', 'Volume'])
   ```

2. **Chunk Processing**
   ```python
   # Process large files in chunks
   for chunk in pd.read_csv(file, chunksize=1000):
       process_chunk(chunk)
   ```

## 🔐 Security Issues

### Problem: Exposed Credentials

**Prevention:**
```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Remove .env from git history if committed
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### Problem: Supabase Connection Limits

**Solution:**
- Use connection pooling
- Close connections properly
- Monitor Supabase dashboard for limits

## 📞 Getting Help

### Debug Information Collection

When reporting issues, include:

1. **System Information**
   ```bash
   python --version
   pip list
   uname -a  # macOS/Linux
   systeminfo  # Windows
   ```

2. **Error Logs**
   ```bash
   # Capture full error output
   python scripts/pipeline.py > debug.log 2>&1
   ```

3. **Configuration (Sanitized)**
   ```bash
   # Remove sensitive data before sharing
   cat .env | sed 's/=.*/=***/'
   ```

### Support Channels

- **GitHub Issues**: https://github.com/username/stockpulse-data-pipeline/issues
- **GitHub Discussions**: For questions and community help
- **Email**: For urgent issues (if provided)

### Before Reporting

1. **Search existing issues** for similar problems
2. **Try basic troubleshooting** steps above
3. **Update dependencies** to latest versions
4. **Test with minimal configuration**

---

## 🔄 Reset Everything

If all else fails, complete reset:

```bash
# 1. Stop all processes
pkill -f streamlit
pkill -f python

# 2. Remove virtual environment
rm -rf venv

# 3. Recreate environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 4. Reload data
python scripts/pipeline.py

# 5. Restart dashboard
streamlit run dashboard/app.py
```

---

*Still having issues? Create a [GitHub Issue](https://github.com/username/stockpulse-data-pipeline/issues) with detailed error logs.*