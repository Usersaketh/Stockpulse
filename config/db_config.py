import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Get traditional database parameters
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "6543")  # Supabase pooler port
DB_NAME = os.getenv("DB_NAME", "postgres")

# Construct the DATABASE_URL for Supabase
if all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    # URL-encode the password to handle special characters
    encoded_password = quote_plus(DB_PASS)
    # Standard Supabase connection with proper SSL and pooling settings
    DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require&connect_timeout=10&application_name=stockpulse"
    print(f"🔗 Database URL configured: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
elif SUPABASE_URL and SUPABASE_ANON_KEY:
    # Fallback: construct from Supabase URL (though this won't work for direct connections)
    print("⚠️ Using Supabase URL and anon key - please set DB_PASS in .env file")
    DATABASE_URL = None
else:
    DATABASE_URL = None
    print("❌ Missing database environment variables")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_NAME: {DB_NAME}")
    print(f"DB_PASS: {'***' if DB_PASS else 'None'}")
    print(f"SUPABASE_URL: {'***' if SUPABASE_URL else 'None'}")
    print(f"SUPABASE_ANON_KEY: {'***' if SUPABASE_ANON_KEY else 'None'}")
