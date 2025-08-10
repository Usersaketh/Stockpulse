import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Save raw data into data/raw/
RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_stock_data(ticker="RELIANCE.NS", days=60):
    """
    Fetch NSE/BSE stock data using Yahoo Finance
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    if df.empty:
        print(f"⚠️ No data found for {ticker}")
        return None

    # Clean up the multi-level columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    
    # Reset index to make Date a regular column
    df.reset_index(inplace=True)

    file_path = os.path.join(RAW_DIR, f"{ticker.replace('.', '_')}.csv")
    df.to_csv(file_path, index=False)
    print(f"✅ Saved raw data for {ticker} → {file_path}")
    return df

if __name__ == "__main__":
    fetch_stock_data("RELIANCE.NS")
    fetch_stock_data("TCS.NS")
    fetch_stock_data("INFY.NS")
