import pandas as pd
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the parent directory to Python path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.db_config import DATABASE_URL
except ImportError:
    print("❌ Database configuration not found. Please check config/db_config.py")
    sys.exit(1)

PROCESSED_DIR = os.path.join("data", "processed")

def create_stock_table(engine, table_name):
    """
    Create a table for stock data if it doesn't exist
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
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
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()
        print(f"✅ Table '{table_name}' created/verified successfully")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Error creating table '{table_name}': {str(e)}")
        return False

def load_stock_data_to_db(ticker="RELIANCE_NS", table_name=None):
    """
    Load processed stock data from CSV to Supabase database
    """
    if table_name is None:
        table_name = f"stock_{ticker.lower()}"
    
    # Check if processed file exists
    csv_file = os.path.join(PROCESSED_DIR, f"{ticker}_processed.csv")
    if not os.path.exists(csv_file):
        print(f"⚠️ Processed data file not found: {csv_file}")
        return False
    
    try:
        # Create database engine with IPv4 preference
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "options": "-c default_transaction_isolation=read_committed",
                "application_name": "stockpulse"
            },
            pool_pre_ping=True,
            pool_recycle=300
        )
        
        # Create table if it doesn't exist
        if not create_stock_table(engine, table_name):
            return False
        
        # Read processed CSV data
        df = pd.read_csv(csv_file, parse_dates=["Date"])
        
        # Clean column names for database (lowercase, underscore)
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Load data to database (replace existing data)
        df.to_sql(
            table_name, 
            engine, 
            if_exists='replace',
            index=False,
            method='multi'
        )
        
        print(f"✅ Successfully loaded {len(df)} records for {ticker} → table '{table_name}'")
        
        # Show sample of loaded data
        with engine.connect() as conn:
            sample_query = f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT 3"
            result = conn.execute(text(sample_query))
            rows = result.fetchall()
            
            if rows:
                print(f"📊 Sample data from '{table_name}':")
                for row in rows:
                    print(f"   {row[0]} | Close: {row[1]} | Volume: {row[5]}")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Database error loading {ticker}: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error loading {ticker}: {str(e)}")
        return False

def load_all_stocks():
    """
    Load all processed stock data to database
    """
    stocks = ["RELIANCE_NS", "TCS_NS", "INFY_NS"]
    success_count = 0
    
    print("🚀 Loading all stock data to Supabase database...")
    
    for stock in stocks:
        print(f"\n📈 Processing {stock}...")
        if load_stock_data_to_db(stock):
            success_count += 1
        else:
            print(f"❌ Failed to load {stock}")
    
    print(f"\n✅ Successfully loaded {success_count}/{len(stocks)} stocks to database")
    return success_count == len(stocks)

def test_database_connection():
    """
    Test the database connection
    """
    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "options": "-c default_transaction_isolation=read_committed",
                "application_name": "stockpulse"
            },
            pool_pre_ping=True,
            pool_recycle=300
        )
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔗 Testing database connection...")
    if test_database_connection():
        print("\n" + "="*50)
        load_all_stocks()
    else:
        print("❌ Cannot proceed without database connection")
