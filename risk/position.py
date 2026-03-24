def position_size(capital: float, entry: float, stop_loss_pct: float, risk_pct: float):
    """
    risk_pct = % of capital you want to risk (e.g., 0.01 = 1%)
    """
    if entry <= 0:
        return 0, 0

    risk_amount = capital * risk_pct
    sl_price = entry * (1 - stop_loss_pct)
    risk_per_share = entry - sl_price
    if risk_per_share <= 0:
        return 0, 0

    qty = int(risk_amount / risk_per_share)
    cost = qty * entry
    return qty, cost