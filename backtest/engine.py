import pandas as pd
import numpy as np
class Backtester:
    def __init__(self, initial_capital=10000, commission=0.001, slippage=0.0005):
        self.initial_capital = float(initial_capital)
        self.commission = float(commission)
        self.slippage = float(slippage)
        self.reset()

    def reset(self):
        self.trades = []
        self.equity_curve = []
        self.final_equity = self.initial_capital
        self.total_return_pct = 0.0
        self.win_rate = 0.0
        self.max_drawdown_pct = 0.0
        self.sharpe = 0.0

    def run(self, df: pd.DataFrame, cmd_func, stop_loss_pct=0.05, take_profit_pct=0.10):
        self.reset()
        if df.empty or len(df) < 10:
            return []

        cash = self.initial_capital
        pos = 0.0
        entry = 0.0

        for i in range(2, len(df)):
            price = float(df["Close"].iloc[i])
            cmd = cmd_func(df.iloc[: i + 1])

            if cmd == "BUY" and cash > 0:
                exec_price = price * (1 + self.slippage)
                pos = (cash * (1 - self.commission)) / exec_price
                entry = exec_price
                cash = 0.0
                self.trades.append({"entry_date": df.index[i], "entry_p": entry})

            elif pos > 0:
                chg = (price - entry) / entry
                stop_hit = chg <= -stop_loss_pct
                tp_hit = chg >= take_profit_pct
                sell_sig = cmd == "SELL"

                if stop_hit or tp_hit or sell_sig:
                    exec_price = price * (1 - self.slippage)
                    exit_val = (pos * exec_price) * (1 - self.commission)
                    pnl = exit_val - (pos * entry)

                    self.trades[-1].update(
                        {"exit_date": df.index[i], "exit_p": exec_price, "pnl": pnl}
                    )
                    cash = exit_val
                    pos = 0.0

            self.equity_curve.append(cash + pos * price)

        self.final_equity = self.equity_curve[-1] if self.equity_curve else self.initial_capital
        self.total_return_pct = ((self.final_equity - self.initial_capital) / self.initial_capital) * 100

        eq = np.array(self.equity_curve, dtype=float)
        if len(eq) > 5:
            peak = np.maximum.accumulate(eq)
            dd = (eq - peak) / peak
            self.max_drawdown_pct = float(dd.min() * 100)
            rets = pd.Series(eq).pct_change().dropna()
            if rets.std() > 0:
                self.sharpe = float((rets.mean() / rets.std()) * np.sqrt(252))

        trades = self.get_trades_df()
        if not trades.empty:
            self.win_rate = float((trades["pnl"] > 0).mean() * 100)

        return self.equity_curve

    def get_trades_df(self):
        return pd.DataFrame([t for t in self.trades if "exit_date" in t])


def to_command(sentiment_score, mode):
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