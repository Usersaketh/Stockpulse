from fetch_stocks import fetch_stock_data
from transform import clean_and_transform
from load_to_db import load_stock_data_to_db

def run_pipeline(load_to_database=True):
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    for ticker in tickers:
        print(f"\n🚀 Running pipeline for {ticker}")
        
        # Step 1: Fetch raw data
        df_raw = fetch_stock_data(ticker)
        if df_raw is not None:
            # Step 2: Transform and clean data
            ticker_clean = ticker.replace(".", "_")
            clean_and_transform(ticker_clean)
            
            # Step 3: Load to database (optional)
            if load_to_database:
                print(f"📊 Loading {ticker} to database...")
                load_stock_data_to_db(ticker_clean)
            else:
                print(f"⏭️ Skipping database load for {ticker}")
        else:
            print(f"❌ Failed to fetch data for {ticker}")

if __name__ == "__main__":
    # Run with database loading
    run_pipeline(load_to_database=True)
