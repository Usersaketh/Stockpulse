# 📈 StockPulse Data Pipeline

**StockPulse** is a comprehensive end-to-end ETL pipeline for Indian stock market data (NSE/BSE) with real-time analysis and visualization capabilities. Built with modern data engineering practices, it provides professional-grade financial analysis tools.

---

## 🚀 Features

- **🔄 Data Ingestion**: Automated fetching from Yahoo Finance API for NSE stocks
- **🛠️ ETL Pipeline**: Complete Extract, Transform, Load workflow with data validation
- **🗄️ Database Integration**: Supabase PostgreSQL backend for scalable data storage
- **📊 Interactive Dashboard**: Real-time Streamlit web application with advanced visualizations
- **📈 Technical Analysis**: Comprehensive indicators including SMA, momentum, volatility analysis
- **🎯 Trading Signals**: Automated buy/sell/hold recommendations with multi-factor analysis
- **📔 Jupyter Analytics**: In-depth data analysis and research notebooks
- **🔧 Modular Architecture**: Clean, maintainable code structure with configuration management

---

## 📊 Supported Stocks

- **RELIANCE.NS** - Reliance Industries Limited
- **TCS.NS** - Tata Consultancy Services  
- **INFY.NS** - Infosys Limited

*Easily extensible to add more NSE/BSE stocks*

---

## 🛠️ Tech Stack

### Backend & Data Processing
- **Python** - Core language with pandas, numpy for data manipulation
- **SQLAlchemy** - Database ORM and connection management
- **yfinance** - Yahoo Finance API integration
- **psycopg2** - PostgreSQL database adapter

### Database & Storage
- **Supabase** - PostgreSQL database-as-a-service
- **PostgreSQL** - Robust relational database for financial data

### Frontend & Visualization  
- **Streamlit** - Interactive web dashboard framework
- **Altair** - Declarative statistical visualization
- **Matplotlib/Seaborn** - Advanced plotting and analytics

### Development & Analysis
- **Jupyter** - Interactive data analysis notebooks
- **dotenv** - Environment configuration management

---

## 📂 Project Structure

```
stockpulse-data-pipeline/
├── 📁 data/                    # Data storage
│   ├── raw/                   # Yahoo Finance downloads  
│   └── processed/             # Clean, transformed data
├── 📁 scripts/                # ETL pipeline components
│   ├── fetch_stocks.py        # Data ingestion from Yahoo Finance
│   ├── transform.py           # Data cleaning and feature engineering
│   ├── load_to_db.py         # Database loading and management
│   └── pipeline.py           # Complete pipeline orchestration
├── 📁 dashboard/              # Web application
│   └── app.py                # Streamlit interactive dashboard
├── 📁 Notebooks/              # Data analysis and research
│   └── analysis.ipynb        # Comprehensive stock analysis
├── 📁 config/                 # Configuration management
│   └── db_config.py          # Database connection settings
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                   # Environment variables (not in repo)
└── 📄 README.md              # Project documentation
```

---

## ⚡ Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/your-username/stockpulse-data-pipeline.git
cd stockpulse-data-pipeline
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux  
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file with your Supabase credentials:
```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Database Connection (from Supabase Settings → Database)
DB_USER=postgres.your_project_ref
DB_PASS=your_database_password  
DB_HOST=aws-region.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
```

### 5. Run the Complete Pipeline
```bash
python scripts/pipeline.py
```

### 6. Launch the Dashboard
```bash
streamlit run dashboard/app.py
```

Visit `http://localhost:8501` to access the interactive dashboard!

---

## 📈 Dashboard Features

### 🎯 Real-time Visualizations
- **Price Trends**: Interactive line charts with SMA overlays
- **Technical Indicators**: Momentum, volatility, and volume analysis  
- **Comparative Analysis**: Multi-stock performance comparison

### 🔧 Technical Analysis
- **Moving Averages**: 20-day SMA with trend analysis
- **Support & Resistance**: Dynamic level identification
- **Volume Analysis**: Trading volume vs historical averages
- **Risk Metrics**: Volatility and return calculations

### 📊 Trading Intelligence
- **Buy/Sell Signals**: Automated recommendation engine
- **Position Analysis**: Current price vs technical levels
- **Trend Detection**: Multi-timeframe trend identification
- **Risk Assessment**: Comprehensive risk-return profiling

---

## 🔍 Analysis Capabilities

### 📊 Data Analysis (Jupyter Notebooks)
- **Price Trend Analysis**: Historical price movements and patterns
- **Technical Indicators**: RSI, MACD, Bollinger Bands calculation
- **Risk-Return Metrics**: Sharpe ratio, maximum drawdown, VaR
- **Correlation Analysis**: Inter-stock relationship analysis
- **Volatility Assessment**: Historical and implied volatility analysis

### 📈 Key Metrics
- Daily returns and cumulative performance
- Rolling volatility and risk metrics  
- Support/resistance level identification
- Volume profile and liquidity analysis
- Sector correlation and market beta

---

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Yahoo Finance │───▶│  ETL Pipeline    │───▶│   Supabase DB   │
│      API        │    │  (Transform)     │    │  (PostgreSQL)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Data Analysis   │    │   Streamlit     │
                       │   (Jupyter)      │    │   Dashboard     │
                       └──────────────────┘    └─────────────────┘
```

---

## 🔧 Configuration

### Environment Setup
The application uses environment variables for secure configuration:

- **Database credentials** for Supabase connection
- **API keys** and authentication tokens  
- **Application settings** and feature flags

### Database Schema
```sql
-- Stock data table structure
CREATE TABLE stock_[ticker] (
    date DATE PRIMARY KEY,
    close DECIMAL(10, 2),
    high DECIMAL(10, 2), 
    low DECIMAL(10, 2),
    open DECIMAL(10, 2),
    volume BIGINT,
    daily_return DECIMAL(8, 6),
    sma_20 DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Advanced Usage

### Custom Stock Addition
```python
# In scripts/pipeline.py, add new tickers:
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
```

### Database Queries
```python
# Direct database access for custom analysis
from config.db_config import DATABASE_URL
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
df = pd.read_sql("SELECT * FROM stock_reliance_ns", engine)
```

### Extending Analysis
```python
# Add custom technical indicators
def calculate_rsi(prices, window=14):
    # Custom RSI implementation
    pass
```

---

## 📚 Learning Outcomes

This project demonstrates:

- **Modern Data Engineering**: ETL pipeline design and implementation
- **Database Integration**: PostgreSQL operations and optimization  
- **Web Application Development**: Interactive dashboard creation
- **Financial Analysis**: Technical indicator calculation and interpretation
- **Data Visualization**: Professional-grade chart and plot creation
- **API Integration**: Real-time data fetching and processing
- **Configuration Management**: Secure credential and environment handling

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)  
5. **Open** a Pull Request

---

## 🙏 Acknowledgments

- **Yahoo Finance** for providing free stock market data API
- **Supabase** for the excellent PostgreSQL database platform
- **Streamlit** for the intuitive web application framework
- **Python Data Science Community** for the amazing ecosystem of tools

---

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join GitHub Discussions for community support

---

**Built with ❤️ for Indian stock market analysis and data engineering education**