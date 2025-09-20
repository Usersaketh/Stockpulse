import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import altair as alt
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import glob

# Add the parent directory to Python path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import configurations
try:
    from config.db_config import DATABASE_URL
    USE_DATABASE = True
    
    # Test database connection
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("🔗 Connected to Supabase database")
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        USE_DATABASE = False
        
except ImportError:
    st.warning("⚠️ Database configuration not found. Using CSV files.")
    USE_DATABASE = False

# Import stock universe configuration
try:
    from config.stock_universe import STOCK_UNIVERSE, get_all_sectors, get_tickers_by_sector
    STOCK_CONFIG_AVAILABLE = True
except ImportError:
    STOCK_CONFIG_AVAILABLE = False

def get_available_companies():
    """Dynamically discover available companies from database or CSV files"""
    available_companies = []
    
    if USE_DATABASE:
        try:
            # Get available tables from database
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'stock_%'
                """))
                tables = [row[0] for row in result]
                
                # Extract company names from table names
                for table in tables:
                    if table.startswith('stock_'):
                        company = table.replace('stock_', '').upper()
                        if '_NS' not in company:
                            company += '_NS'
                        available_companies.append(company)
                        
        except Exception as e:
            st.warning(f"Could not fetch from database: {e}")
    
    # Fallback: Check CSV files
    if not available_companies:
        # Try multiple possible locations for processed files
        possible_dirs = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "data", "processed"),
            os.path.join("data", "processed"),
            os.path.join("scripts", "data", "processed")
        ]
        
        for processed_dir in possible_dirs:
            if os.path.exists(processed_dir):
                csv_files = glob.glob(os.path.join(processed_dir, "*_processed.csv"))
                for file_path in csv_files:
                    filename = os.path.basename(file_path)
                    company = filename.replace('_processed.csv', '')
                    available_companies.append(company)
                
                if available_companies:  # Found files, break
                    st.info(f"📂 Found {len(available_companies)} companies in {processed_dir}")
                    break
    
    # Remove duplicates and sort
    available_companies = sorted(list(set(available_companies)))
    
    return available_companies

st.set_page_config(page_title="📈 StockPulse Dashboard", layout="wide")

st.title("📊 StockPulse – Financial Data Dashboard")
st.markdown("Interactive insights from NSE/BSE stocks pipeline")

# Get available companies dynamically
available_companies = get_available_companies()

# Sidebar
st.sidebar.header("⚙️ Controls")

if available_companies:
    # Create ticker options from available companies
    ticker_options = {}
    for company in available_companies:
        # Convert filename format back to display format
        display_name = company.replace("_", ".")
        if not display_name.endswith(".NS"):
            display_name += ".NS"
        ticker_options[display_name] = company
    
    # Add sector filter if stock universe is available
    if STOCK_CONFIG_AVAILABLE:
        st.sidebar.subheader("🏢 Sector Filter")
        sectors = ["All Sectors"] + [sector.title() for sector in get_all_sectors()]
        selected_sector = st.sidebar.selectbox("Filter by Sector", sectors)
        
        if selected_sector != "All Sectors":
            sector_tickers = get_tickers_by_sector(selected_sector.lower())
            # Filter ticker_options to only show companies from selected sector
            filtered_options = {k: v for k, v in ticker_options.items() 
                              if any(k.replace(".", "_") == ticker.replace(".", "_") 
                                   for ticker in sector_tickers)}
            ticker_options = filtered_options if filtered_options else ticker_options
    
    st.sidebar.subheader("📈 Stock Selection")
    selected_ticker = st.sidebar.selectbox("Choose a stock", list(ticker_options.keys()))
    metric = st.sidebar.selectbox("Metric", ["Close", "Daily_Return", "SMA_20"])
    
    # Show portfolio summary
    st.sidebar.subheader("📊 Portfolio Overview")
    st.sidebar.info(f"**Total Companies:** {len(available_companies)}")
    
    if STOCK_CONFIG_AVAILABLE:
        # Count companies by sector
        sector_counts = {}
        for company in available_companies:
            for sector, data in STOCK_UNIVERSE.items():
                if any(company.replace("_", ".") == ticker for ticker in data["tickers"]):
                    sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        if sector_counts:
            st.sidebar.write("**By Sector:**")
            for sector, count in sorted(sector_counts.items()):
                st.sidebar.write(f"  • {sector.title()}: {count}")
    
    # Convert display name to filename format
    ticker_file = ticker_options[selected_ticker]
    
else:
    st.error("❌ No stock data found! Please run the ETL pipeline first.")
    st.info("💡 Run `python scripts/pipeline.py` to fetch and process stock data.")
    st.stop()

# Load data from database or CSV files
@st.cache_data
def load_data(ticker_name):
    if USE_DATABASE:
        try:
            # Load from database
            table_name = f"stock_{ticker_name.lower()}"
            query = f"SELECT * FROM {table_name} ORDER BY date DESC"
            
            with engine.connect() as conn:
                df = pd.read_sql(query, conn, parse_dates=["date"])
                df.rename(columns={"date": "Date"}, inplace=True)
                df.set_index("Date", inplace=True)
                
                # Convert column names back to match original CSV format
                df.columns = [col.replace("_", " ").title() for col in df.columns]
                
                # Fix specific column names to match dashboard expectations
                column_mapping = {
                    'Daily Return': 'Daily_Return',
                    'Sma 20': 'SMA_20'
                }
                df.rename(columns=column_mapping, inplace=True)
                
                st.info(f"📊 Loaded {len(df)} records from database table '{table_name}'")
                return df
                
        except Exception as e:
            st.error(f"❌ Database error: {str(e)}")
            st.info("🔄 Falling back to CSV files...")
    
    # Fallback to CSV files
    try:
        # Try multiple possible locations for processed files
        possible_files = [
            f"data/processed/{ticker_name}_processed.csv",
            f"scripts/data/processed/{ticker_name}_processed.csv",
            f"../data/processed/{ticker_name}_processed.csv",
            f"../scripts/data/processed/{ticker_name}_processed.csv"
        ]
        
        for processed_file in possible_files:
            if os.path.exists(processed_file):
                df = pd.read_csv(processed_file, parse_dates=["Date"], index_col="Date")
                st.info(f"📂 Loaded {len(df)} records from CSV file: {processed_file}")
                return df
        
        st.error(f"❌ Data file not found for {ticker_name} in any location")
        st.info("💡 Searched locations: " + ", ".join(possible_files))
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

df = load_data(ticker_file)

if df is not None:
    # Show raw data
    st.subheader(f"📂 {selected_ticker} – Latest Records")
    st.dataframe(df.tail(10))

    # Price and SMA Chart
    st.subheader(f"📈 Price Trends with Technical Indicators for {selected_ticker}")
    
    if "Close" in df.columns:
        # Reset index to make Date a column for Altair
        df_chart = df.reset_index()
        
        # Create base price chart
        price_chart = (
            alt.Chart(df_chart)
            .mark_line(color='blue', strokeWidth=2)
            .encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("Close:Q", title="Price (₹)"),
                tooltip=["Date:T", "Close:Q", "Volume:Q"]
            )
        )
        
        # Add SMA line if available
        if "SMA_20" in df.columns:
            sma_chart = (
                alt.Chart(df_chart)
                .mark_line(color='orange', strokeWidth=2, strokeDash=[5, 5])
                .encode(
                    x="Date:T",
                    y="SMA_20:Q",
                    tooltip=["Date:T", "SMA_20:Q"]
                )
            )
            combined_chart = (price_chart + sma_chart).resolve_scale(y='shared')
        else:
            combined_chart = price_chart
            
        st.altair_chart(combined_chart, use_container_width=True)
        
        # Legend
        if "SMA_20" in df.columns:
            st.markdown("**Legend:** 🔵 Close Price | 🟠 20-day SMA")
    
    # Individual Metric Chart
    st.subheader(f"📊 {metric} Detailed View")
    
    # Check if the metric exists in the DataFrame
    if metric in df.columns:
        df_chart = df.reset_index()
        chart = (
            alt.Chart(df_chart)
            .mark_line(point=True)
            .encode(
                x="Date:T",
                y=f"{metric}:Q",
                tooltip=["Date:T", f"{metric}:Q"]
            )
            .properties(width=800, height=400)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.error(f"Column '{metric}' not found in data")

    # Returns Summary
    if "Daily_Return" in df.columns:
        st.subheader("📊 Returns Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Daily Return", f"{df['Daily_Return'].mean():.4f}")
        with col2:
            st.metric("Volatility (Std Dev)", f"{df['Daily_Return'].std():.4f}")
        with col3:
            st.metric("Total Return", f"{df['Daily_Return'].sum():.4f}")
            
        st.write("**Statistical Summary:**")
        st.write(df["Daily_Return"].describe())

    # Enhanced Technical Analysis
    if "SMA_20" in df.columns and "Close" in df.columns:
        st.subheader("� Technical Analysis")
        
        # Current vs SMA Analysis
        latest_close = df["Close"].iloc[-1]
        latest_sma = df["SMA_20"].iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if pd.notna(latest_sma):
                price_vs_sma = ((latest_close - latest_sma) / latest_sma) * 100
                signal = "🟢 BUY" if price_vs_sma > 0 else "🔴 SELL"
                st.metric(
                    "Price vs 20-day SMA", 
                    f"{price_vs_sma:.2f}%",
                    delta=signal
                )
            
        with col2:
            # Support and Resistance levels
            recent_high = df['Close'].rolling(20).max().iloc[-1]
            recent_low = df['Close'].rolling(20).min().iloc[-1]
            position_in_range = ((latest_close - recent_low) / (recent_high - recent_low) * 100) if recent_high != recent_low else 50
            st.metric(
                "Position in 20D Range",
                f"{position_in_range:.1f}%",
                delta=f"High: ₹{recent_high:.2f}, Low: ₹{recent_low:.2f}"
            )
            
        with col3:
            # Volume Analysis
            if "Volume" in df.columns:
                avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
                current_volume = df['Volume'].iloc[-1]
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
                volume_signal = "🟢 HIGH" if volume_ratio > 1.2 else "🟡 NORMAL" if volume_ratio > 0.8 else "🔴 LOW"
                st.metric(
                    "Volume vs 20D Avg",
                    f"{volume_ratio:.2f}x",
                    delta=volume_signal
                )
        
        # Additional Technical Indicators
        st.write("### 📊 Technical Indicators Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price momentum
            if len(df) >= 5:
                price_5d_change = ((df['Close'].iloc[-1] / df['Close'].iloc[-5]) - 1) * 100
                momentum_signal = "🟢 Bullish" if price_5d_change > 2 else "🔴 Bearish" if price_5d_change < -2 else "🟡 Neutral"
                st.write(f"**5-Day Momentum:** {price_5d_change:.2f}% {momentum_signal}")
            
            # Volatility
            if "Daily_Return" in df.columns:
                volatility_20d = df['Daily_Return'].rolling(20).std().iloc[-1] * 100
                vol_signal = "🔴 HIGH" if volatility_20d > 3 else "🟡 MEDIUM" if volatility_20d > 1.5 else "🟢 LOW"
                st.write(f"**20-Day Volatility:** {volatility_20d:.2f}% {vol_signal}")
                
        with col2:
            # Trend Analysis
            if pd.notna(latest_sma) and len(df) >= 10:
                sma_trend = df['SMA_20'].iloc[-1] > df['SMA_20'].iloc[-10]
                trend_signal = "🟢 Uptrend" if sma_trend else "🔴 Downtrend"
                st.write(f"**SMA Trend (10D):** {trend_signal}")
            
            # Price position
            if pd.notna(latest_sma):
                price_position = "🟢 Above SMA" if latest_close > latest_sma else "🔴 Below SMA"
                st.write(f"**Price Position:** {price_position}")
                
        # Trading Signals Summary
        st.write("### 🎯 Trading Signals")
        signals = []
        
        if pd.notna(latest_sma):
            if price_vs_sma > 2:
                signals.append("🟢 Strong Buy - Price well above SMA")
            elif price_vs_sma > 0:
                signals.append("🟡 Buy - Price above SMA")
            elif price_vs_sma > -2:
                signals.append("🟡 Hold - Price near SMA")
            else:
                signals.append("🔴 Sell - Price below SMA")
                
        if volume_ratio > 1.5:
            signals.append("🟢 High Volume Confirmation")
        elif volume_ratio < 0.5:
            signals.append("🔴 Low Volume Warning")
            
        for signal in signals:
            st.write(f"• {signal}")
            
        if not signals:
            st.write("• 🟡 Insufficient data for signals")
else:
    st.error("No data available. Please run the pipeline first: `python scripts/pipeline.py`")
