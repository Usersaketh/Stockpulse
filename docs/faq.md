# ❓ Frequently Asked Questions

Common questions about StockPulse Data Pipeline.

## 🚀 Getting Started

### Q: What is StockPulse?
**A:** StockPulse is an end-to-end ETL (Extract, Transform, Load) pipeline for Indian stock market data. It automatically fetches stock data from Yahoo Finance, processes it, stores it in a database, and provides interactive visualizations through a web dashboard.

### Q: Which stocks are supported?
**A:** Currently supports:
- **RELIANCE.NS** (Reliance Industries)
- **TCS.NS** (Tata Consultancy Services)
- **INFY.NS** (Infosys Limited)

You can easily add more NSE/BSE stocks by modifying the ticker list in `scripts/pipeline.py`.

### Q: Is this free to use?
**A:** Yes! StockPulse is open-source and free. The only costs might be:
- Supabase database (free tier available)
- Cloud hosting if you deploy it (optional)

## 🛠️ Technical Questions

### Q: What programming language is used?
**A:** Python is the primary language, with these key libraries:
- **pandas** for data manipulation
- **streamlit** for the web dashboard
- **yfinance** for stock data
- **sqlalchemy** for database operations

### Q: Do I need a database?
**A:** Yes, but it's easy to set up:
- **Recommended**: Supabase (free PostgreSQL database)
- **Alternative**: Local PostgreSQL or MySQL
- **Fallback**: CSV files (limited functionality)

### Q: How often is data updated?
**A:** Data updates are manual by default. Run this command to refresh:
```bash
python scripts/pipeline.py
```

Future versions may include automated scheduling.

## 📊 Data Questions

### Q: How much historical data is included?
**A:** By default, 60 days of historical data. You can modify this in `scripts/fetch_stocks.py`:
```python
def fetch_stock_data(ticker="RELIANCE.NS", days=60):  # Change this
```

### Q: What data points are collected?
**A:** For each trading day:
- **OHLCV**: Open, High, Low, Close, Volume
- **Daily Returns**: Percentage change from previous day
- **SMA_20**: 20-day Simple Moving Average
- **Date**: Trading date

### Q: Is real-time data available?
**A:** Currently uses end-of-day data from Yahoo Finance. Real-time data would require:
- Paid data feeds
- Different architecture (streaming)
- More complex infrastructure

## 💻 Setup Questions

### Q: I'm getting database connection errors. What should I do?
**A:** Check these common issues:
1. **Username format**: Use `postgres.your_project_ref` not just `postgres`
2. **Password**: Verify in Supabase Dashboard → Settings → Database
3. **Host**: Use pooler host `aws-region.pooler.supabase.com`
4. **Port**: Use `6543` for pooler connection

See [troubleshooting.md](troubleshooting.md) for detailed solutions.

### Q: Can I run this without Supabase?
**A:** Yes, but with limitations:
- Dashboard will use CSV files instead of database
- Slower performance
- No real-time updates
- Limited scalability

### Q: What if I don't have Python experience?
**A:** StockPulse is designed to be beginner-friendly:
1. Follow the [Quick Start Guide](quickstart.md) step-by-step
2. All commands are provided
3. Pre-configured settings work out-of-the-box
4. Extensive documentation and troubleshooting guides

## 📈 Dashboard Questions

### Q: How do I interpret the trading signals?
**A:** Trading signals are educational indicators:
- 🟢 **Buy**: Price above moving average + positive momentum
- 🟡 **Hold**: Price near moving average or mixed signals  
- 🔴 **Sell**: Price below moving average + negative momentum

**Important**: These are for learning only, not financial advice!

### Q: What do the technical indicators mean?
**A:** Key indicators explained:
- **SMA_20**: 20-day average price, shows trend direction
- **Daily Return**: Day-to-day percentage change
- **Volatility**: How much the price fluctuates
- **Volume Ratio**: Current trading volume vs average

### Q: Can I add more technical indicators?
**A:** Yes! Modify `scripts/transform.py` to add indicators like:
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- EMA (Exponential Moving Average)

## 🔧 Customization Questions

### Q: How do I add more stocks?
**A:** Edit `scripts/pipeline.py`:
```python
def run_pipeline(load_to_database=True):
    tickers = [
        "RELIANCE.NS", 
        "TCS.NS", 
        "INFY.NS",
        "HDFCBANK.NS",  # Add new stocks here
        "ICICIBANK.NS"
    ]
```

### Q: Can I change the data source?
**A:** Currently uses Yahoo Finance, but you can modify `scripts/fetch_stocks.py` to use:
- Alpha Vantage API
- IEX Cloud
- Quandl
- NSE/BSE direct APIs (if available)

### Q: How do I modify the dashboard?
**A:** Edit `dashboard/app.py` to:
- Add new chart types
- Include more metrics
- Change the layout
- Add export features
- Customize colors/themes

## 🚀 Deployment Questions

### Q: Can I deploy this to the cloud?
**A:** Yes! Deployment options:
- **Streamlit Cloud**: Free hosting for Streamlit apps
- **Heroku**: Easy app deployment
- **AWS/Azure/GCP**: Full cloud platforms
- **Docker**: Containerized deployment

### Q: How do I share this with others?
**A:** Several options:
1. **GitHub**: Share the code repository
2. **Streamlit Cloud**: Deploy and share the URL
3. **Local Network**: Run locally and share IP address
4. **Docker**: Package everything in a container

### Q: Is this suitable for production use?
**A:** Current version is designed for:
- Learning and education
- Personal analysis
- Portfolio projects
- Proof of concepts

For production, consider adding:
- Authentication system
- Error monitoring
- Automated backups
- Load balancing
- Security hardening

## 💡 Learning Questions

### Q: What can I learn from this project?
**A:** Key skills demonstrated:
- **Data Engineering**: ETL pipeline design
- **Database Management**: SQL, PostgreSQL operations
- **Web Development**: Interactive dashboard creation
- **Data Analysis**: Financial metrics and visualization
- **Python Programming**: Modern libraries and best practices
- **Cloud Integration**: Database-as-a-service usage

### Q: How is this useful for job interviews?
**A:** This project shows:
- **End-to-end thinking**: Complete system design
- **Modern tech stack**: Industry-relevant tools
- **Data pipeline experience**: Core data engineering skill
- **Web development**: Full-stack capabilities
- **Financial domain**: Specialized knowledge
- **Documentation**: Professional communication skills

### Q: What should I build next?
**A:** Potential enhancements:
1. **Machine Learning**: Price prediction models
2. **Real-time Processing**: Streaming data pipeline
3. **Mobile App**: React Native or Flutter frontend
4. **API Development**: REST API for data access
5. **Alert System**: Email/SMS notifications
6. **Portfolio Tracking**: Investment portfolio analysis

## 🔐 Security Questions

### Q: Is my data secure?
**A:** Security measures in place:
- **Encrypted connections**: HTTPS/SSL for all communications
- **Credential isolation**: Sensitive data in `.env` files
- **Database security**: Supabase built-in security features
- **No sensitive data**: Only public market data stored

### Q: What about my Supabase credentials?
**A:** Best practices:
- Never commit `.env` files to version control
- Use environment variables in production
- Regularly rotate database passwords
- Monitor access logs in Supabase dashboard

## 📞 Support Questions

### Q: Where can I get help?
**A:** Support resources:
- **Documentation**: Comprehensive guides in `/docs` folder
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community Q&A
- **Troubleshooting Guide**: Common problems and solutions

### Q: How do I report bugs?
**A:** To report issues:
1. Check [troubleshooting.md](troubleshooting.md) first
2. Search existing GitHub issues
3. Create new issue with:
   - Error messages
   - Steps to reproduce
   - System information
   - Configuration (without sensitive data)

### Q: Can I contribute to the project?
**A:** Absolutely! Contributions welcome:
- **Bug fixes**: Submit pull requests
- **New features**: Propose and implement
- **Documentation**: Improve guides and examples
- **Testing**: Add test cases and validation
- **Feedback**: Share usage experiences

## 🎯 Next Steps

### Q: I've got it working. What's next?
**A:** Suggested progression:
1. **Explore**: Try different stocks and time periods
2. **Analyze**: Use Jupyter notebooks for deeper analysis
3. **Customize**: Add your own indicators and features
4. **Share**: Deploy and show others
5. **Extend**: Build additional functionality
6. **Learn**: Study financial markets and data science

### Q: How do I stay updated?
**A:** Keep current:
- **Watch the repository**: Get notified of updates
- **Follow releases**: New features and bug fixes
- **Join discussions**: Community updates and tips
- **Read changelog**: Track project evolution

---

**Still have questions?** 

- 📖 Check the [full documentation](README.md)
- 🐛 Report issues on [GitHub](https://github.com/username/stockpulse-data-pipeline/issues)
- 💬 Join [GitHub Discussions](https://github.com/username/stockpulse-data-pipeline/discussions)

*Last updated: September 20, 2025*