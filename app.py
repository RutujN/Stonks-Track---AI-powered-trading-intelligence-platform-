import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from ui.theme import apply_theme
from ui.components import render_signal_cards
from data.market_data import fetch_market_data
from data.sentiment import fetch_sentiment
from indicators.core import apply_indicators
from strategy.signals import generate_signals
from strategy.verdict import verdict_from_signals, to_command
from backtest.engine import Backtester
from risk.position import position_size
from utils.helpers import pivot_levels

st.markdown(
    """
<div class="card">
    <h2 style="margin:0;">Stonks Track</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.85;">
        Premium Quant Terminal • Signals • Risk • Backtest • S/R Levels
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ========================= SIDEBAR =========================
with st.sidebar:
    st.header("Control Panel")
    theme = st.radio("Theme", ["Dark", "Light"], index=0, horizontal=True)
    apply_theme(theme)

    plotly_template = "plotly_dark" if theme == "Dark" else "plotly_white"

    mode = st.selectbox("Trading Mode", ["Intraday", "Swing", "Long-Term"], index=1)

    tickers_raw = st.text_area("Watchlist (1 ticker per line)", value="AAPL\nMSFT\nTSLA")
    tickers = [t.strip().upper() for t in tickers_raw.splitlines() if t.strip()]

    period = st.selectbox("History", ["1y", "2y", "5y"], index=0)

    st.subheader("Sentiment")
    api_key = st.text_input("Finnhub API Key (optional)", type="password")
    news_weight = st.slider("News Weight", 0, 100, 50) / 100

    st.divider()
    st.subheader("Risk Controls")
    capital = st.number_input("Capital", 1000, 1000000, 10000, 1000)
    risk_pct = st.slider("Risk per Trade (%)", 1, 5, 2) / 100
    sl_pct = st.slider("Stop Loss %", 1, 15, 5) / 100
    tp_pct = st.slider("Take Profit %", 5, 30, 12) / 100

# Main ticker selection
selected = st.selectbox("Select Ticker", tickers, index=0 if tickers else None)
if not selected:
    st.error("Add at least 1 ticker to watchlist.")
    st.stop()

df = fetch_market_data(selected, period)
if df.empty:
    st.error("No market data. Try another ticker.")
    st.stop()

df = apply_indicators(df, mode)
sent_score, sent_df = fetch_sentiment(selected, api_key)
sent_score = sent_score * news_weight

support_res = pivot_levels(df, lookback=20)

tabs = st.tabs(["📊 Market", "📈 Indicators", "📰 Mood", "🧠 Verdict", "🧪 Backtest", "🧾 Tools"])

# ========================= TAB: MARKET =========================
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"{selected} — Market")

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Price"
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], name="EMA50", mode="lines"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA200"], name="EMA200", mode="lines"))
    fig.add_trace(go.Scatter(x=df.index, y=df["VWAP"], name="VWAP", mode="lines", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Supertrend"], name="Supertrend", mode="lines"))

    if support_res:
        support, resistance = support_res
        fig.add_hline(y=support, line_dash="dot", annotation_text="Support", annotation_position="bottom left")
        fig.add_hline(y=resistance, line_dash="dot", annotation_text="Resistance", annotation_position="top left")

    fig.update_layout(template=plotly_template, height=650, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= TAB: INDICATORS =========================
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Indicators (ADX / DI + ATR)")

    ind_fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
    ind_fig.add_trace(go.Scatter(x=df.index, y=df["ADX"], name="ADX"), row=1, col=1)
    ind_fig.add_trace(go.Scatter(x=df.index, y=df["DI_PLUS"], name="DI+"), row=2, col=1)
    ind_fig.add_trace(go.Scatter(x=df.index, y=df["DI_MINUS"], name="DI-"), row=2, col=1)

    ind_fig.update_layout(template=plotly_template, height=600)
    st.plotly_chart(ind_fig, use_container_width=True)

    st.write("ATR14 (Volatility)")
    st.line_chart(df["ATR14"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= TAB: MOOD =========================
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Mood (VADER News Sentiment)")
    st.metric("Sentiment Score (Weighted)", f"{sent_score:.2f}")
    st.dataframe(sent_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========================= TAB: VERDICT =========================
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Verdict Engine")

    sigs = generate_signals(df, sent_score, mode)
    if not sigs:
        st.warning("Not enough data for verdict.")
    else:
        verdict, score = verdict_from_signals(sigs)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Verdict", verdict)
        c2.metric("Score", score)
        c3.metric("Mode", mode)
        c4.metric("Sentiment Weight", f"{news_weight:.2f}")

        st.divider()
        render_signal_cards(sigs)

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= TAB: BACKTEST =========================
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Backtest")

    if st.button("Run Backtest"):
        bt = Backtester(initial_capital=capital)
        cmd = to_command(sent_score, mode)
        curve = bt.run(df, cmd, stop_loss_pct=sl_pct, take_profit_pct=tp_pct)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Return %", f"{bt.total_return_pct:.2f}")
        c2.metric("Win Rate %", f"{bt.win_rate:.1f}")
        c3.metric("Max DD %", f"{bt.max_drawdown_pct:.2f}")
        c4.metric("Sharpe", f"{bt.sharpe:.2f}")

        st.line_chart(curve, use_container_width=True)

        trades = bt.get_trades_df()
        st.dataframe(trades, use_container_width=True)

        if not trades.empty:
            csv = trades.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Trade Log CSV", csv, file_name=f"{selected}_trades.csv", mime="text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= TAB: TOOLS =========================
with tabs[5]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Tools (Risk + Trade Plan)")

    latest_price = float(df["Close"].iloc[-1])
    latest_atr = float(df["ATR14"].iloc[-1]) if not pd.isna(df["ATR14"].iloc[-1]) else 0.0

    st.write("### Position Sizing")
    qty, cost = position_size(capital, latest_price, sl_pct, risk_pct)
    st.write(f"**Entry Price:** {latest_price:.2f}")
    st.write(f"**Risk Per Trade:** {risk_pct*100:.2f}% of capital")
    st.write(f"**Suggested Quantity:** {qty}")
    st.write(f"**Approx Cost:** {cost:.2f}")

    st.divider()
    st.write("### Trade Plan (ATR Based)")
    if latest_atr > 0:
        entry = latest_price
        stop = entry - (1.5 * latest_atr)
        target = entry + (2.5 * latest_atr)
        st.success(f"Entry: {entry:.2f} | SL: {stop:.2f} | TP: {target:.2f}")
    else:
        st.info("ATR not available yet for this ticker.")

    st.divider()
    st.write("### Breakout Detector")
    if support_res:
        support, resistance = support_res
        dist_to_res = (resistance - latest_price) / resistance
        if dist_to_res < 0.01 and df["ADX"].iloc[-1] > MODE_PRESETS[mode]["adx_th"]:
            st.success("⚡ Price is near resistance with strong trend strength → breakout watch!")
        else:
            st.write("No breakout conditions detected right now.")
    else:
        st.write("Not enough data for support/resistance detection.")

    st.markdown("</div>", unsafe_allow_html=True)