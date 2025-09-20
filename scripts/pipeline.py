from fetch_stocks import fetch_stock_data
from transform import clean_and_transform
from load_to_db import load_stock_data_to_db
import sys
import os

# Add config path to import stock universe
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.stock_universe import get_ticker_set, print_stock_universe_summary

def run_pipeline(load_to_database=True, ticker_set="diversified_portfolio"):
    """
    Run the StockPulse ETL pipeline for multiple companies
    
    Args:
        load_to_database (bool): Whether to load data to database
        ticker_set (str): Which set of tickers to process
                         Options: 'nifty_50_sample', 'tech_focused', 'banking_focused', 
                                'diversified_portfolio', 'comprehensive'
    """
    # Get tickers from configuration
    tickers = get_ticker_set(ticker_set)
    
    if not tickers:
        print(f"❌ Invalid ticker set: {ticker_set}")
        print("Available sets: nifty_50_sample, tech_focused, banking_focused, diversified_portfolio, comprehensive")
        return
    
    print(f"🚀 Starting StockPulse ETL Pipeline")
    print(f"📊 Processing {len(tickers)} companies using '{ticker_set}' set")
    print("=" * 60)
    
    successful_companies = 0
    failed_companies = 0

    for i, ticker in enumerate(tickers, 1):
        print(f"\n[{i}/{len(tickers)}] 🚀 Running pipeline for {ticker}")
        
        try:
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
                    print(f"✅ Successfully processed {ticker}")
                    successful_companies += 1
                else:
                    print(f"⏭️ Skipping database load for {ticker}")
                    successful_companies += 1
            else:
                print(f"❌ Failed to fetch data for {ticker}")
                failed_companies += 1
                
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")
            failed_companies += 1
    
    # Summary Report
    print("\n" + "=" * 60)
    print("📈 PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total Companies: {len(tickers)}")
    print(f"✅ Successful: {successful_companies}")
    print(f"❌ Failed: {failed_companies}")
    print(f"📊 Success Rate: {(successful_companies/len(tickers)*100):.1f}%")
    
    if successful_companies > 0:
        print(f"\n🎉 Pipeline completed! {successful_companies} companies processed successfully.")
    else:
        print(f"\n⚠️ Pipeline completed with issues. Please check the logs.")

if __name__ == "__main__":
    import argparse
    
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='StockPulse ETL Pipeline')
    parser.add_argument('--ticker-set', 
                       choices=['nifty_50_sample', 'tech_focused', 'banking_focused', 
                               'diversified_portfolio', 'comprehensive'],
                       default='diversified_portfolio',
                       help='Which set of tickers to process (default: diversified_portfolio)')
    parser.add_argument('--no-db', action='store_true', 
                       help='Skip database loading (process only)')
    parser.add_argument('--show-universe', action='store_true',
                       help='Show available stock universe and exit')
    
    args = parser.parse_args()
    
    if args.show_universe:
        print_stock_universe_summary()
        exit(0)
    
    # Run pipeline with specified parameters
    load_to_db = not args.no_db
    run_pipeline(load_to_database=load_to_db, ticker_set=args.ticker_set)
