import pandas as pd
import os

RAW_DIR = os.path.join("..", "data", "raw")
PROCESSED_DIR = os.path.join("..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_and_transform(ticker="RELIANCE_NS"):
    file_path = os.path.join(RAW_DIR, f"{ticker}.csv")
    if not os.path.exists(file_path):
        print(f"⚠️ Raw data not found for {ticker}")
        return None

    # Read CSV with clean format (Date as a column)
    df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")

    # Drop missing values
    df = df.dropna()

    # Add daily returns
    df["Daily_Return"] = df["Close"].pct_change()

    # Add 20-day moving average
    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    # Save processed data
    processed_path = os.path.join(PROCESSED_DIR, f"{ticker}_processed.csv")
    df.to_csv(processed_path)
    print(f"✅ Processed data saved → {processed_path}")
    return df

if __name__ == "__main__":
    import sys
    
    # Check if ticker provided as command line argument
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        print(f"🚀 Processing data for {ticker}")
        clean_and_transform(ticker)
    else:
        # Default behavior - process sample companies
        print("🚀 No ticker specified, processing default sample companies...")
        clean_and_transform("RELIANCE_NS")
        clean_and_transform("TCS_NS")
        clean_and_transform("INFY_NS")
