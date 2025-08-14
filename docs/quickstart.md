# 🚀 Quick Start Guide

Get your StockPulse Data Pipeline up and running in under 5 minutes!

## Prerequisites

- **Python 3.8+** installed on your system
- **Git** for version control
- **Supabase account** (free tier available)

## 5-Minute Setup

### Step 1: Clone and Setup (1 min)
```bash
git clone https://github.com/your-username/stockpulse-data-pipeline.git
cd stockpulse-data-pipeline
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Supabase Setup (2 min)
1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to **Settings → Database** and note:
   - Database password
   - Connection string details

### Step 3: Environment Configuration (1 min)
Create `.env` file in project root:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# Database Connection
DB_USER=postgres.your_project_ref
DB_PASS=your_database_password
DB_HOST=aws-region.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
```

### Step 4: Run Pipeline (1 min)
```bash
# Fetch data and load to database
python scripts/pipeline.py
```

### Step 5: Launch Dashboard (30 sec)
```bash
# Start the web dashboard
streamlit run dashboard/app.py
```

🎉 **Done!** Visit `http://localhost:8501` to see your stock analysis dashboard!

## What You'll See

- **📈 Real-time stock charts** with price trends
- **📊 Technical analysis** with SMA indicators  
- **🎯 Trading signals** and recommendations
- **📋 Performance metrics** and statistics

## Next Steps

- **[Dashboard Guide](dashboard-guide.md)** - Learn all dashboard features
- **[Configuration](configuration.md)** - Customize settings
- **[Analysis Notebooks](analysis-guide.md)** - Explore Jupyter analytics

## Troubleshooting

**Database connection issues?** → Check [troubleshooting.md](troubleshooting.md)
**Import errors?** → Ensure virtual environment is activated
**Missing data?** → Run `python scripts/pipeline.py` again