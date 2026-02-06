import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import finnhub
from fear_and_greed import get as get_fg
from datetime import datetime, timedelta

# --- 1. CONFIG & API ---
st.set_page_config(page_title="WealthBot", layout="wide")
FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

# --- 2. DATA ENGINE ---
def get_analysis(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty or len(df) < 50:
            return None 

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        close_prices = df['Close'].dropna()
        df['SMA50'] = close_prices.rolling(window=50).mean()
        
        price = float(close_prices.iloc[-1])
        yday = float(close_prices.iloc[-2])
        sma = float(df['SMA50'].iloc[-1])
        pct_change = ((price - yday) / yday) * 100
        
        today = datetime.now().strftime('%Y-%m-%d')
        last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        news = finnhub_client.company_news(ticker, _from=last_week, to=today)[:3]
            
        signal = "🟢 BUY" if price < sma else "⚪ HOLD"
        return df, price, yday, sma, signal, news, pct_change
    except:
        return None

# --- 3. SIDEBAR & CALCULATOR ---
st.sidebar.header("💼 Your Holdings")
CALC_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
holdings = {s: st.sidebar.number_input(f"{s} Shares", min_value=0, value=0) for s in CALC_STOCKS}

# --- 4. MAIN INTERFACE ---
st.title("🤖 AI Tech Wealth Manager")
TECH_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'GLD', 'PLUG', 'BBAI', 'AMC', 'RR', 'POET', 'GRRR', 'XTKG', 'INBS', 'ANIX', 'TNXP', 'BTAI']

total_val = 0.0
total_pnl = 0.0

# --- 5. DISPLAY LOOP ---
for stock in TECH_STOCKS:
    result = get_analysis(stock)
    if result is None:
        continue
    
    df, price, yday, sma, signal, news, pct = result
    
    # Calculate Portfolio Totals
    if stock in holdings and holdings[stock] > 0:
        total_val += (price * holdings[stock])
        total_pnl += ((price - yday) * holdings[stock])

    # UI Section
    alert_marker = " ⚠️" if pct <= -5.0 else ""
    with st.expander(f"{stock}{alert_marker} - Signal: {signal}", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric(label=f"Price {alert_marker}", value=f"${price:.2f}", delta=f"{pct:.2f}%")
            if pct <= -5.0:
                st.error(f"High Volatility: Down {pct:.2f}%")
            st.write(f"**Signal:** {signal}")
            st.write(f"**50-Day SMA:** ${sma:.2f}")
        with col2:
            fig = go.Figure()
            # Fixed String Literals below
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Price", line=dict(color='#00d1ff')))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name="50-Day SMA", line=dict(color='#ff9900', dash='dot')))
            fig.update_layout(template="plotly_dark", height=200, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        if news:
            st.write("---")
            for article in news:
                st.markdown(f"- [{article['headline']}]({article['url']})")

# Update Sidebar Totals at the end
st.sidebar.divider()
st.sidebar.metric("Total Portfolio Value", f"${total_val:,.2f}")

st.sidebar.metric("Today's Profit/Loss", f"${total_pnl:,.2f}", delta=f"${total_pnl:,.2f}")
