import pandas as pd
import numpy as np
from config.settings import MODE_PRESETS
def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    hl = df["High"] - df["Low"]
    hc = (df["High"] - df["Close"].shift()).abs()
    lc = (df["Low"] - df["Close"].shift()).abs()
    return pd.concat([hl, hc, lc], axis=1).max(axis=1)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    tr = true_range(df)
    return tr.rolling(period).mean()


def safe_vwap(df: pd.DataFrame) -> pd.Series:
    if "Volume" not in df.columns:
        return pd.Series(np.nan, index=df.index)
    vol = df["Volume"].fillna(0)
    if float(vol.sum()) == 0:
        return pd.Series(np.nan, index=df.index)
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    return (tp * vol).cumsum() / (vol.cumsum() + 1e-9)


def adx(df: pd.DataFrame, period: int = 14):
    up = df["High"].diff()
    down = -df["Low"].diff()

    plus_dm = np.where((up > down) & (up > 0), up, 0.0)
    minus_dm = np.where((down > up) & (down > 0), down, 0.0)

    tr = true_range(df)
    atr_n = tr.rolling(period).mean()

    plus_di = 100 * pd.Series(plus_dm, index=df.index).rolling(period).sum() / (atr_n + 1e-9)
    minus_di = 100 * pd.Series(minus_dm, index=df.index).rolling(period).sum() / (atr_n + 1e-9)

    dx = (np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-9)) * 100
    adx_val = dx.rolling(period).mean()

    return adx_val, plus_di, minus_di


def supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    out = df.copy()
    atr_val = atr(out, period)
    hl2 = (out["High"] + out["Low"]) / 2
    upper = hl2 + multiplier * atr_val
    lower = hl2 - multiplier * atr_val

    st_line = pd.Series(index=out.index, dtype=float)
    direction = pd.Series(index=out.index, dtype=float)

    direction.iloc[0] = 1
    st_line.iloc[0] = np.nan

    for i in range(1, len(out)):
        prev_dir = direction.iloc[i - 1]
        prev_upper = upper.iloc[i - 1]
        prev_lower = lower.iloc[i - 1]
        close = out["Close"].iloc[i]

        if close > prev_upper:
            curr_dir = 1
        elif close < prev_lower:
            curr_dir = -1
        else:
            curr_dir = prev_dir
            if curr_dir == 1:
                lower.iloc[i] = max(lower.iloc[i], prev_lower)
            else:
                upper.iloc[i] = min(upper.iloc[i], prev_upper)

        direction.iloc[i] = curr_dir
        st_line.iloc[i] = lower.iloc[i] if curr_dir == 1 else upper.iloc[i]

    out["Supertrend"] = st_line
    out["ST_Direction"] = direction
    return out


MODE_PRESETS = {
    "Intraday": {"st_period": 7, "st_mult": 2.0, "adx_th": 18},
    "Swing": {"st_period": 10, "st_mult": 3.0, "adx_th": 20},
    "Long-Term": {"st_period": 14, "st_mult": 4.0, "adx_th": 25},
}


def apply_indicators(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    if df.empty:
        return df

    p = MODE_PRESETS.get(mode, MODE_PRESETS["Swing"])

    out = df.copy()
    out["EMA50"] = ema(out["Close"], 50)
    out["EMA200"] = ema(out["Close"], 200)
    out["ATR14"] = atr(out, 14)
    out["VWAP"] = safe_vwap(out)

    adx_val, di_plus, di_minus = adx(out, 14)
    out["ADX"] = adx_val
    out["DI_PLUS"] = di_plus
    out["DI_MINUS"] = di_minus

    out = supertrend(out, period=p["st_period"], multiplier=p["st_mult"])
    out = out.replace([np.inf, -np.inf], np.nan)
    return out

