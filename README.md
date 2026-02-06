# 🤖 WealthBot: AI-Powered Tech Stock Manager

WealthBot is a real-time financial dashboard built with **Python** and **Streamlit**. It automates the "Buy the Dip" strategy by monitoring technical indicators, global market sentiment, and live news for top tech giants.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_DEPLOYED_APP_URL)

## 🚀 Key Features
- **Technical Strategy**: Automated "BUY" signals when price drops below the 50-Day SMA.
- **Sentiment Analysis**: Integration with the CNN Fear & Greed Index for macro-market context.
- **Portfolio Tracking**: Live P/L tracking and total value calculation for tech holdings.
- **Stable News Feed**: Reliable financial headlines powered by the **Finnhub API**.
- **Visual Alerts**: Dynamic UI background changes during significant market corrections (5%+ drops).

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Financial Data**: [yfinance](https://pypi.org/project/yfinance/) & [Finnhub API](https://finnhub.io/)
- **Visuals**: [Plotly](https://plotly.com/)
- **Language**: Python 3.10+

## 📦 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/WealthBot.git](https://github.com/yourusername/WealthBot.git)
   cd WealthBot
