def verdict_from_signals(sigs):
    score = 0
    for _, _, a in sigs:
        if a == "BUY":
            score += 1
        elif a == "SELL":
            score -= 1

    if score >= 3:
        return "STRONG BUY", score
    if score == 2:
        return "BUY", score
    if score == 1:
        return "MILD BUY", score
    if score == 0:
        return "NEUTRAL", score
    if score == -1:
        return "MILD SELL", score
    if score == -2:
        return "SELL", score
    return "STRONG SELL", score


def to_command(sentiment_score, mode):
    from strategy.signals import generate_signals

    def cmd(df):
        sigs = generate_signals(df, sentiment_score, mode)
        if not sigs:
            return "HOLD"

        buys = sum(1 for _, _, a in sigs if a == "BUY")
        sells = sum(1 for _, _, a in sigs if a == "SELL")

        if buys > sells:
            return "BUY"
        if sells > buys:
            return "SELL"
        return "HOLD"

    return cmd


