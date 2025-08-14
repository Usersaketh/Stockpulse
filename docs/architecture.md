# 🏗️ Architecture Overview

Understanding the StockPulse Data Pipeline system design and data flow.

## 🎯 System Overview

StockPulse is a **modern ETL pipeline** designed for financial data processing with real-time visualization capabilities.

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Yahoo Finance │───▶│  ETL Pipeline    │───▶│   Supabase DB   │
│      API        │    │  (Transform)     │    │  (PostgreSQL)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                        │
         │                       ▼                        ▼
         │              ┌──────────────────┐    ┌─────────────────┐
         └──────────────▶│  Data Analysis   │    │   Streamlit     │
                        │   (Jupyter)      │    │   Dashboard     │
                        └──────────────────┘    └─────────────────┘
```

## 🔄 Data Flow Architecture

### 1. **Data Ingestion Layer**
- **Source**: Yahoo Finance API via `yfinance` library
- **Frequency**: On-demand (manual trigger)
- **Data**: OHLCV (Open, High, Low, Close, Volume) data
- **Timeframe**: 60 days historical data

### 2. **Processing Layer**
- **Transformation**: Data cleaning and feature engineering
- **Validation**: Data quality checks and error handling
- **Enrichment**: Technical indicators calculation

### 3. **Storage Layer**
- **Database**: Supabase (PostgreSQL)
- **Connection**: Pooler for scalability
- **Schema**: Optimized for time-series data

### 4. **Presentation Layer**
- **Dashboard**: Streamlit web application
- **Analytics**: Jupyter notebooks
- **Visualization**: Altair and matplotlib charts

## 📦 Component Architecture

### Core Components

```
stockpulse-data-pipeline/
├── 📊 Data Layer
│   ├── Raw Data (CSV)
│   ├── Processed Data (CSV)
│   └── Database Tables
│
├── 🔧 Processing Layer
│   ├── Ingestion (fetch_stocks.py)
│   ├── Transformation (transform.py)
│   ├── Loading (load_to_db.py)
│   └── Orchestration (pipeline.py)
│
├── 📈 Presentation Layer
│   ├── Web Dashboard (app.py)
│   └── Analytics (analysis.ipynb)
│
└── ⚙️ Configuration Layer
    ├── Database Config (db_config.py)
    └── Environment (.env)
```

## 🗄️ Database Architecture

### Table Structure

Each stock has its own table with standardized schema:

```sql
-- Example: stock_reliance_ns
CREATE TABLE stock_reliance_ns (
    date                DATE PRIMARY KEY,
    close              DECIMAL(10, 2) NOT NULL,
    high               DECIMAL(10, 2) NOT NULL,
    low                DECIMAL(10, 2) NOT NULL,
    open               DECIMAL(10, 2) NOT NULL,
    volume             BIGINT NOT NULL,
    daily_return       DECIMAL(8, 6),
    sma_20            DECIMAL(10, 2),
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexing Strategy

```sql
-- Primary index on date for time-series queries
CREATE INDEX idx_stock_date ON stock_reliance_ns(date);

-- Composite index for range queries
CREATE INDEX idx_stock_date_close ON stock_reliance_ns(date, close);

-- Index for analytical queries
CREATE INDEX idx_stock_volume ON stock_reliance_ns(volume) 
WHERE volume > 1000000;
```

## 🔄 ETL Pipeline Design

### Extract Phase
```python
# Data Ingestion Flow
Yahoo Finance API → yfinance → Raw CSV Files
│
├── Error Handling: API rate limits, network issues
├── Data Validation: Schema verification, null checks
└── File Storage: Timestamped raw data files
```

### Transform Phase
```python
# Data Processing Flow
Raw CSV → pandas DataFrame → Feature Engineering → Validation
│
├── Data Cleaning: Remove duplicates, handle missing values
├── Feature Engineering: Daily returns, moving averages
├── Quality Checks: Data consistency, outlier detection
└── Format Standardization: Date parsing, decimal precision
```

### Load Phase
```python
# Database Loading Flow
Processed DataFrame → SQLAlchemy → Supabase PostgreSQL
│
├── Connection Management: Pooling, retry logic
├── Table Operations: CREATE, INSERT, UPDATE
├── Transaction Safety: Rollback on errors
└── Performance: Batch inserts, indexing
```

## 🌐 Web Application Architecture

### Streamlit Framework
```python
# Dashboard Architecture
Streamlit App → Database Connection → Data Loading → Visualization
│
├── Caching: @st.cache_data for performance
├── State Management: Session state for user interactions  
├── Reactive Updates: Auto-refresh on data changes
└── Responsive Design: Mobile-friendly layouts
```

### Frontend Components
- **Navigation**: Sidebar with stock/metric selection
- **Data Display**: Interactive tables and charts
- **Analysis**: Real-time calculations and indicators
- **Export**: Data download capabilities

## 🔧 Configuration Management

### Environment Configuration
```python
# Configuration Hierarchy
1. Environment Variables (.env file)
2. Default Values (fallbacks)
3. Runtime Parameters (command line)

# Security Layers
├── Credential Isolation: .env not in version control
├── Connection Encryption: SSL/TLS for database
└── Access Control: Supabase RLS policies
```

### Database Connection
```python
# Connection Pool Architecture
Application → SQLAlchemy Engine → Connection Pool → Supabase
│
├── Pool Size: Configurable connections (default: 5)
├── Timeout: Connection and query timeouts
├── Retry Logic: Automatic reconnection on failures
└── Health Checks: Regular connection validation
```

## 📊 Data Processing Architecture

### Real-time Processing
```python
# Processing Pipeline
Raw Data → Validation → Transformation → Enrichment → Storage
│
├── Parallel Processing: Multi-stock concurrent processing
├── Memory Management: Chunked processing for large datasets
├── Error Recovery: Graceful handling of failures
└── Monitoring: Logging and progress tracking
```

### Technical Indicators Engine
```python
# Indicator Calculation Flow
Price Data → Rolling Windows → Mathematical Operations → Signals
│
├── SMA: Simple Moving Average calculations
├── Returns: Daily percentage change calculations
├── Volatility: Rolling standard deviation
└── Signals: Buy/sell/hold recommendations
```

## 🚀 Scalability Considerations

### Horizontal Scaling
- **Multiple Stocks**: Easy addition of new tickers
- **Data Sources**: Pluggable data provider architecture
- **Geographic Distribution**: Multi-region deployment capability

### Vertical Scaling
- **Database**: Supabase auto-scaling
- **Compute**: Configurable processing resources
- **Storage**: Unlimited data retention

### Performance Optimization
- **Caching**: Multi-level caching strategy
- **Indexing**: Optimized database indexes
- **Compression**: Efficient data storage formats
- **CDN**: Static asset delivery optimization

## 🔐 Security Architecture

### Data Security
```python
# Security Layers
1. Transport Layer: HTTPS/TLS encryption
2. Authentication: Supabase authentication system
3. Authorization: Row-level security policies
4. Data Protection: Encrypted at rest
```

### Application Security
- **Environment Isolation**: Separate dev/prod environments
- **Credential Management**: Secure secret storage
- **Input Validation**: SQL injection prevention
- **Access Logging**: Audit trail for all operations

## 📈 Monitoring and Observability

### Application Monitoring
- **Error Tracking**: Exception logging and alerting
- **Performance Metrics**: Response time monitoring
- **Usage Analytics**: Dashboard interaction tracking
- **Health Checks**: System availability monitoring

### Data Quality Monitoring
- **Data Freshness**: Last update timestamps
- **Data Completeness**: Missing value detection
- **Data Accuracy**: Outlier and anomaly detection
- **Data Consistency**: Cross-validation checks

## 🔮 Future Architecture Enhancements

### Planned Improvements
1. **Real-time Streaming**: Apache Kafka for live data
2. **Machine Learning**: Predictive models integration
3. **API Layer**: REST API for external integrations
4. **Microservices**: Service decomposition for scalability
5. **Container Deployment**: Docker and Kubernetes
6. **Data Lake**: Raw data archival and analytics

### Technology Roadmap
- **Event-Driven Architecture**: Message queues and events
- **Serverless Functions**: Cloud functions for processing
- **Graph Database**: Relationship analysis capabilities
- **Time Series DB**: Specialized TSDB for performance

---

## 📚 Related Documentation

- **[Database Schema](database.md)** - Detailed table structures
- **[Configuration Guide](configuration.md)** - Setup and tuning
- **[Development Guide](development.md)** - Contributing guidelines
- **[Performance Guide](performance.md)** - Optimization tips

---

*This architecture supports the current needs while providing a foundation for future enhancements and scale.*