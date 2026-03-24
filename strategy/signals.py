import pandas as pd
from config.settings import MODE_PRESETS
def generate_signals(df: pd.DataFrame, sentiment_score: float, mode: str):
    if df.empty or len(df) < 60:
        return []

    latest = df.iloc[-1]
    p = MODE_PRESETS.get(mode, MODE_PRESETS["Swing"])
    adx_th = p["adx_th"]

    sigs = []

    ema_sig = "BUY" if latest["EMA50"] > latest["EMA200"] else "SELL"
    sigs.append(("EMA 50/200 Trend Filter", "EMA50 vs EMA200", ema_sig))

    st_sig = "BUY" if latest["ST_Direction"] == 1 else "SELL"
    sigs.append(("Supertrend Direction", "Trend State", st_sig))

    if pd.isna(latest["VWAP"]):
        vwap_sig = "NEUTRAL"
        vwap_val = "VWAP N/A"
    else:
        vwap_sig = "BUY" if latest["Close"] > latest["VWAP"] else "SELL"
        vwap_val = "Price vs VWAP"
    sigs.append(("VWAP Bias", vwap_val, vwap_sig))

    if pd.isna(latest["ADX"]):
        adx_sig, adx_val = "NEUTRAL", "ADX N/A"
    else:
        adx_val = f"ADX {latest['ADX']:.2f}"
        if latest["ADX"] > adx_th:
            adx_sig = "BUY" if latest["DI_PLUS"] > latest["DI_MINUS"] else "SELL"
        else:
            adx_sig = "NEUTRAL"
    sigs.append(("ADX Strength + DI Direction", adx_val, adx_sig))

    sent_sig = "BUY" if sentiment_score > 0.05 else "SELL" if sentiment_score < -0.05 else "NEUTRAL"
    sigs.append(("News Sentiment", f"Score {sentiment_score:.2f}", sent_sig))

    return sigs