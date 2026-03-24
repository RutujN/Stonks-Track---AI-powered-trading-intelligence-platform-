# 📊 Stonks Track – Fintech Quant Dashboard

A modular, interactive financial analytics platform built using **Python + Streamlit** that provides **technical analysis, sentiment insights, trading signals, and backtesting** in a single unified dashboard.

---

## 🚀 Overview

**Stonks Track** is a lightweight quantitative trading terminal designed to help users:

* Analyze stock price trends
* Generate trading signals using technical indicators
* Incorporate market sentiment (news-based)
* Perform risk-aware position sizing
* Backtest trading strategies

The project follows a **modular architecture**, making it scalable, maintainable, and easy to explain.

---

## 🧠 Key Features

### 📈 Market Analysis

* Candlestick charts
* EMA (50/200), VWAP overlays
* Supertrend indicator
* Support & Resistance levels

### 📊 Technical Indicators

* EMA (Trend)
* ATR (Volatility)
* ADX + DI+/DI− (Momentum)
* VWAP (Price bias)

### 📰 Sentiment Analysis

* News-based sentiment using **NLTK VADER**
* Optional integration with **Finnhub API**

### ⚡ Signal Engine

* Multi-factor decision system combining:

  * Trend
  * Momentum
  * Volatility
  * Sentiment
* Outputs: **BUY / SELL / NEUTRAL**

### 🧠 Verdict System

* Aggregates signals into:

  * Strong Buy / Buy / Neutral / Sell / Strong Sell

### 🧪 Backtesting Engine

* Simulates trades
* Metrics:

  * Return %
  * Win rate
  * Max drawdown
  * Sharpe ratio

### 💰 Risk Management

* Position sizing based on:

  * Capital
  * Risk %
  * Stop loss %

### 🧰 Tools

* ATR-based trade planning
* Breakout detection
* Trade logs export (CSV)

---

## 🏗️ Project Structure

```
fintech_app/
│
├── app.py                  # Main Streamlit application
│
├── config/
│   └── settings.py         # Trading mode presets
│
├── ui/
│   ├── theme.py            # UI themes (dark/light)
│   └── components.py       # Signal cards & UI elements
│
├── data/
│   ├── market_data.py      # Fetch stock data (yfinance)
│   └── sentiment.py        # News sentiment (VADER + Finnhub)
│
├── indicators/
│   └── core.py             # All technical indicators
│
├── strategy/
│   ├── signals.py          # Signal generation logic
│   └── verdict.py          # Final decision engine
│
├── backtest/
│   └── engine.py           # Backtesting logic
│
├── risk/
│   └── position.py         # Position sizing
│
└── utils/
    └── helpers.py          # Support/Resistance (pivot levels)
```

---

## ⚙️ Technologies Used

### 🐍 Core

* Python 3.x
* Streamlit (UI framework)

### 📊 Data & Analysis

* Pandas
* NumPy
* yFinance

### 📉 Visualization

* Plotly

### 🧠 NLP (Sentiment)

* NLTK (VADER Sentiment Analyzer)

### 🌐 APIs

* Finnhub (optional news data)

---

## 🔄 Workflow

1. User selects a stock ticker
2. Market data is fetched using **yFinance**
3. Indicators are applied (EMA, ATR, ADX, etc.)
4. Sentiment is calculated from news
5. Signal engine evaluates multiple factors
6. Verdict system generates final recommendation
7. Optional backtesting simulates performance

---

## ▶️ How to Run Locally

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the app

```
python -m streamlit run app.py
```

---

## ☁️ Deployment

The app can be deployed using:

* **Streamlit Cloud (recommended)**
* GitHub integration for CI/CD

---

## 🧠 Design Principles

* **Modularity** → Each component is isolated (data, indicators, strategy)
* **Scalability** → Easy to add ML models or new indicators
* **Separation of Concerns** → Clean architecture
* **Extensibility** → Supports future trading automation

---

## 📌 Future Improvements

* Machine Learning price prediction (LSTM)
* Real-time streaming data
* Portfolio optimization
* Broker API integration for live trading
* Advanced risk analytics

---

## 👨‍💻 Motivation to make this project

Developed as a fintech analytics project demonstrating:

* Quantitative finance concepts
* Algorithmic trading logic
* Full-stack data application using Streamlit

---


