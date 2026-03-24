
def pivot_levels(df: pd.DataFrame, lookback: int = 20):
    if df.empty or len(df) < lookback:
        return None

    recent = df.tail(lookback)
    support = float(recent["Low"].min())
    resistance = float(recent["High"].max())
    return support, resistance