"""
Stock Universe Configuration for StockPulse ETL Pipeline
Organized by sectors and market caps for comprehensive market coverage
"""

# NSE Stock Universe - Organized by Sectors
STOCK_UNIVERSE = {
    "technology": {
        "description": "Information Technology & Software Services",
        "tickers": [
            "TCS.NS",        # Tata Consultancy Services
            "INFY.NS",       # Infosys
            "WIPRO.NS",      # Wipro
            "HCLTECH.NS",    # HCL Technologies
            "TECHM.NS",      # Tech Mahindra
            "MINDTREE.NS",   # Mindtree
            "MPHASIS.NS",    # Mphasis
            "LTI.NS",        # L&T Infotech
        ]
    },
    
    "banking": {
        "description": "Banking & Financial Services",
        "tickers": [
            "HDFCBANK.NS",   # HDFC Bank
            "ICICIBANK.NS",  # ICICI Bank
            "SBIN.NS",       # State Bank of India
            "KOTAKBANK.NS",  # Kotak Mahindra Bank
            "AXISBANK.NS",   # Axis Bank
            "INDUSINDBK.NS", # IndusInd Bank
            "FEDERALBNK.NS", # Federal Bank
            "BANDHANBNK.NS", # Bandhan Bank
        ]
    },
    
    "energy": {
        "description": "Oil, Gas & Energy",
        "tickers": [
            "RELIANCE.NS",   # Reliance Industries
            "ONGC.NS",       # Oil & Natural Gas Corp
            "IOC.NS",        # Indian Oil Corporation
            "BPCL.NS",       # Bharat Petroleum
            "GAIL.NS",       # GAIL India
            "HINDPETRO.NS",  # Hindustan Petroleum
            "ADANIGREEN.NS", # Adani Green Energy
            "TATAPOWER.NS",  # Tata Power
        ]
    },
    
    "pharmaceuticals": {
        "description": "Pharmaceuticals & Healthcare",
        "tickers": [
            "SUNPHARMA.NS",  # Sun Pharmaceutical
            "DRREDDY.NS",    # Dr. Reddy's Labs
            "CIPLA.NS",      # Cipla
            "DIVISLAB.NS",   # Divi's Laboratories
            "BIOCON.NS",     # Biocon
            "LUPIN.NS",      # Lupin
            "AUROPHARMA.NS", # Aurobindo Pharma
            "TORNTPHARM.NS", # Torrent Pharmaceuticals
        ]
    },
    
    "fmcg": {
        "description": "Fast Moving Consumer Goods",
        "tickers": [
            "HINDUNILVR.NS", # Hindustan Unilever
            "ITC.NS",        # ITC
            "BRITANNIA.NS",  # Britannia Industries
            "DABUR.NS",      # Dabur India
            "MARICO.NS",     # Marico
            "GODREJCP.NS",   # Godrej Consumer Products
            "COLPAL.NS",     # Colgate-Palmolive
            "NESTLEIND.NS",  # Nestle India
        ]
    },
    
    "automobile": {
        "description": "Automotive & Auto Components",
        "tickers": [
            "MARUTI.NS",     # Maruti Suzuki
            "TATAMOTORS.NS", # Tata Motors
            "M&M.NS",        # Mahindra & Mahindra
            "BAJAJ-AUTO.NS", # Bajaj Auto
            "HEROMOTOCO.NS", # Hero MotoCorp
            "EICHERMOT.NS",  # Eicher Motors
            "ASHOKLEY.NS",   # Ashok Leyland
            "BOSCHLTD.NS",   # Bosch
        ]
    },
    
    "metals": {
        "description": "Metals & Mining",
        "tickers": [
            "TATASTEEL.NS",  # Tata Steel
            "HINDALCO.NS",   # Hindalco Industries
            "JSWSTEEL.NS",   # JSW Steel
            "SAIL.NS",       # Steel Authority of India
            "COALINDIA.NS",  # Coal India
            "VEDL.NS",       # Vedanta
            "JINDALSTEL.NS", # Jindal Steel & Power
            "NMDC.NS",       # NMDC
        ]
    },
    
    "infrastructure": {
        "description": "Infrastructure & Construction",
        "tickers": [
            "LT.NS",         # Larsen & Toubro
            "ULTRACEMCO.NS", # UltraTech Cement
            "GRASIM.NS",     # Grasim Industries
            "SHREECEM.NS",   # Shree Cement
            "RAMCOCEM.NS",   # Ramco Cements
            "ACC.NS",        # ACC
            "AMBUJACEMENT.NS", # Ambuja Cements
            "INFRATEL.NS",   # Bharti Infratel
        ]
    },
    
    "telecom": {
        "description": "Telecommunications",
        "tickers": [
            "BHARTIARTL.NS", # Bharti Airtel
            "IDEA.NS",       # Vodafone Idea (Vi)
        ]
    },
    
    "utilities": {
        "description": "Power & Utilities",
        "tickers": [
            "POWERGRID.NS",  # Power Grid Corporation
            "NTPC.NS",       # NTPC
            "TATAPOWER.NS",  # Tata Power
            "ADANIPOWER.NS", # Adani Power
            "JSPL.NS",       # Jindal Steel & Power
        ]
    }
}

# Market Cap Classifications
MARKET_CAP_CATEGORIES = {
    "large_cap": [
        "TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "LT.NS", "SBIN.NS", "ITC.NS", "KOTAKBANK.NS", "HINDUNILVR.NS"
    ],
    
    "mid_cap": [
        "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "AXISBANK.NS", "ULTRACEMCO.NS",
        "MARUTI.NS", "SUNPHARMA.NS", "BAJAJ-AUTO.NS", "DRREDDY.NS", "BRITANNIA.NS"
    ],
    
    "small_cap": [
        "MINDTREE.NS", "MPHASIS.NS", "FEDERALBNK.NS", "BANDHANBNK.NS",
        "LUPIN.NS", "AUROPHARMA.NS", "GODREJCP.NS", "EICHERMOT.NS"
    ]
}

# Predefined ticker sets for different use cases
TICKER_SETS = {
    "nifty_50_sample": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
        "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "LT.NS", "ITC.NS",
        "AXISBANK.NS", "BHARTIARTL.NS", "MARUTI.NS", "ASIANPAINT.NS", "HCLTECH.NS"
    ],
    
    "tech_focused": STOCK_UNIVERSE["technology"]["tickers"],
    
    "banking_focused": STOCK_UNIVERSE["banking"]["tickers"],
    
    "diversified_portfolio": [
        # One from each sector
        "TCS.NS", "HDFCBANK.NS", "RELIANCE.NS", "SUNPHARMA.NS",
        "HINDUNILVR.NS", "MARUTI.NS", "TATASTEEL.NS", "LT.NS",
        "BHARTIARTL.NS", "POWERGRID.NS"
    ],
    
    "comprehensive": [
        ticker for sector_data in STOCK_UNIVERSE.values()
        for ticker in sector_data["tickers"]
    ]
}

# Sector weights for portfolio analysis
SECTOR_WEIGHTS = {
    "technology": 0.20,      # 20%
    "banking": 0.18,         # 18%
    "energy": 0.15,          # 15%
    "fmcg": 0.12,           # 12%
    "pharmaceuticals": 0.10, # 10%
    "automobile": 0.08,      # 8%
    "metals": 0.07,         # 7%
    "infrastructure": 0.05,  # 5%
    "telecom": 0.03,        # 3%
    "utilities": 0.02        # 2%
}

def get_tickers_by_sector(sector_name: str) -> list:
    """Get all tickers for a specific sector"""
    return STOCK_UNIVERSE.get(sector_name, {}).get("tickers", [])

def get_tickers_by_market_cap(market_cap: str) -> list:
    """Get tickers by market cap category"""
    return MARKET_CAP_CATEGORIES.get(market_cap, [])

def get_ticker_set(set_name: str) -> list:
    """Get predefined ticker set"""
    return TICKER_SETS.get(set_name, [])

def get_all_sectors() -> list:
    """Get list of all available sectors"""
    return list(STOCK_UNIVERSE.keys())

def get_sector_info(sector_name: str) -> dict:
    """Get sector information including description and tickers"""
    return STOCK_UNIVERSE.get(sector_name, {})

def print_stock_universe_summary():
    """Print a summary of the stock universe"""
    print("🏢 StockPulse Stock Universe Summary")
    print("=" * 50)
    
    total_stocks = sum(len(sector["tickers"]) for sector in STOCK_UNIVERSE.values())
    print(f"Total Stocks: {total_stocks}")
    print(f"Total Sectors: {len(STOCK_UNIVERSE)}")
    
    print("\n📊 Sector Breakdown:")
    for sector, data in STOCK_UNIVERSE.items():
        print(f"  {sector.title()}: {len(data['tickers'])} stocks - {data['description']}")
    
    print("\n💹 Market Cap Distribution:")
    for cap_type, tickers in MARKET_CAP_CATEGORIES.items():
        print(f"  {cap_type.replace('_', ' ').title()}: {len(tickers)} stocks")
    
    print("\n📈 Available Ticker Sets:")
    for set_name, tickers in TICKER_SETS.items():
        print(f"  {set_name}: {len(tickers)} stocks")