# 📊 Dashboard User Guide

Complete guide to using the StockPulse interactive dashboard.

## 🚀 Getting Started

Launch the dashboard:
```bash
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

## 🎛️ Dashboard Interface

### Sidebar Controls

**Stock Selection**
- Choose from: RELIANCE.NS, TCS.NS, INFY.NS
- Switch between stocks instantly

**Metric Selection**  
- **Close**: Stock closing prices
- **Daily_Return**: Daily percentage returns
- **SMA_20**: 20-day Simple Moving Average

## 📈 Main Dashboard Sections

### 1. Data Overview
- **Latest Records Table**: Last 10 trading days
- **Data Source**: Shows if using database or CSV fallback
- **Record Count**: Total data points loaded

### 2. Price Trends with Technical Indicators
- **Blue Line**: Current stock price
- **Orange Dashed Line**: 20-day SMA trend
- **Interactive Tooltips**: Hover for exact values
- **Zoom/Pan**: Click and drag to explore

### 3. Individual Metric Charts
- **Detailed View**: Focused chart for selected metric
- **Point Markers**: Individual data points
- **Time Series**: Full historical timeline

### 4. Returns Summary
**Key Metrics Display:**
- **Average Daily Return**: Mean percentage change
- **Volatility**: Standard deviation of returns
- **Total Return**: Cumulative return over period

**Statistical Summary Table:**
- Count, mean, std, min, max
- Quartile distributions (25%, 50%, 75%)

### 5. Technical Analysis

#### Price Analysis
- **Price vs SMA**: Percentage above/below moving average
- **Buy/Sell Signals**: 🟢 BUY / 🔴 SELL recommendations
- **Position in Range**: Current price within 20-day high/low

#### Volume Analysis
- **Volume Ratio**: Current vs 20-day average
- **Volume Signals**: 🟢 HIGH / 🟡 NORMAL / 🔴 LOW

#### Technical Indicators
- **5-Day Momentum**: Short-term price momentum
- **20-Day Volatility**: Risk assessment
- **SMA Trend**: Moving average direction
- **Price Position**: Above/below SMA status

#### Trading Signals
**Automated Recommendations:**
- 🟢 **Strong Buy**: Price well above SMA
- 🟡 **Buy**: Price above SMA  
- 🟡 **Hold**: Price near SMA
- 🔴 **Sell**: Price below SMA

**Volume Confirmation:**
- 🟢 **High Volume**: Strong market interest
- 🔴 **Low Volume**: Weak market participation

## 🔧 Advanced Features

### Data Refresh
- Dashboard updates automatically when new data is loaded
- Clear cache: Use Streamlit menu → "Clear cache"

### Multiple Stock Comparison
- Switch between stocks using sidebar
- Compare metrics across different companies
- Analyze relative performance

### Export Data
Data can be accessed programmatically:
```python
from config.db_config import DATABASE_URL
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
df = pd.read_sql("SELECT * FROM stock_reliance_ns", engine)
```

## 📊 Understanding the Metrics

### Price Metrics
- **Close**: End-of-day trading price
- **High/Low**: Daily trading range
- **Volume**: Number of shares traded

### Technical Indicators
- **SMA_20**: 20-day Simple Moving Average
  - Smooths price action
  - Identifies trend direction
  - Support/resistance levels

- **Daily_Return**: Daily percentage change
  - Formula: `(Today's Close - Yesterday's Close) / Yesterday's Close`
  - Measures day-to-day volatility

### Trading Signals Interpretation

| Signal | Meaning | Action |
|--------|---------|--------|
| 🟢 Strong Buy | Price >2% above SMA | Consider buying |
| 🟡 Buy | Price above SMA | Weak buy signal |
| 🟡 Hold | Price near SMA (±2%) | Wait for clarity |
| 🔴 Sell | Price below SMA | Consider selling |

### Volume Analysis
- **>1.5x Average**: High interest, strong conviction
- **0.8-1.5x Average**: Normal trading activity  
- **<0.8x Average**: Low interest, weak conviction

## 🚨 Important Notes

### Data Quality
- **Data Source**: Yahoo Finance via yfinance API
- **Update Frequency**: Manual pipeline runs
- **Historical Range**: Typically 60 days

### Limitations
- **Not Financial Advice**: For educational purposes only
- **Delayed Data**: May not reflect real-time prices
- **Limited Universe**: Only 3 stocks currently supported

### Best Practices
- **Cross-Reference**: Verify signals with multiple indicators
- **Risk Management**: Never risk more than you can afford
- **Continuous Learning**: Use for educational analysis

## 🔧 Troubleshooting

### Common Issues

**No data showing:**
```bash
# Reload data
python scripts/pipeline.py
```

**Connection errors:**
- Check `.env` file configuration
- Verify Supabase credentials
- Test database connection

**Performance issues:**
- Clear Streamlit cache
- Restart the dashboard
- Check system resources

**Chart not loading:**
- Refresh browser page
- Check browser console for errors
- Try different browser

## 🎯 Tips for Analysis

1. **Trend Analysis**: Look for SMA direction and price position
2. **Volume Confirmation**: High volume strengthens signals
3. **Multiple Timeframes**: Consider longer-term trends
4. **Risk Assessment**: Monitor volatility metrics
5. **Comparative Analysis**: Compare across stocks

---

*For technical issues, see [troubleshooting.md](troubleshooting.md)*