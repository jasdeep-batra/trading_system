import pandas as pd


class PerformanceMetrics:

    def __init__(self, trades, initial_capital, final_capital):

        self.trades = trades
        self.initial_capital = initial_capital
        self.final_capital = final_capital

    def calculate(self):

        closed_trades = [
            t for t in self.trades
            if t["status"] == "CLOSED"
        ]

        if len(closed_trades) == 0:

            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "total_pnl": 0,
                "return_percent": 0,
                "profit_factor": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "max_drawdown": 0,
                "final_capital": self.final_capital
            }

        pnl_list = [
            trade["pnl"]
            for trade in closed_trades
        ]

        wins = [
            pnl for pnl in pnl_list
            if pnl > 0
        ]

        losses = [
            pnl for pnl in pnl_list
            if pnl < 0
        ]

        total_pnl = sum(pnl_list)

        total_trades = len(closed_trades)

        win_rate = (
            len(wins) / total_trades
        ) * 100

        gross_profit = sum(wins)

        gross_loss = abs(sum(losses))

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss != 0
            else float("inf")
        )

        avg_win = (
            gross_profit / len(wins)
            if wins
            else 0
        )

        avg_loss = (
            gross_loss / len(losses)
            if losses
            else 0
        )

        return_percent = (
            (
                self.final_capital -
                self.initial_capital
            )
            / self.initial_capital
        ) * 100

        # -----------------------------
        # Equity Curve
        # -----------------------------

        equity = self.initial_capital

        equity_curve = []

        for trade in closed_trades:

            equity += trade["pnl"]

            equity_curve.append(equity)

        running_peak = equity_curve[0]

        max_drawdown = 0

        for value in equity_curve:

            running_peak = max(
                running_peak,
                value
            )

            drawdown = (
                running_peak - value
            )

            max_drawdown = max(
                max_drawdown,
                drawdown
            )

        # -----------------------------
        # Strategy-wise Performance
        # -----------------------------

        strategy_summary = {}

        for trade in closed_trades:

            for strategy in trade.get( "strategies", [] ):

                strategy_summary.setdefault(
                    strategy,
                    0
                )

                strategy_summary[strategy] += trade["pnl"]

        # -----------------------------
        # Regime-wise Performance
        # -----------------------------

        regime_summary = {}

        for trade in closed_trades:

            regime = trade["regime"]

            regime_summary.setdefault(
                regime,
                0
            )

            regime_summary[regime] += trade["pnl"]

        return {

            "total_trades": total_trades,

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": round(
                win_rate,
                2
            ),

            "total_pnl": round(
                total_pnl,
                2
            ),

            "return_percent": round(
                return_percent,
                2
            ),

            "profit_factor": round(
                profit_factor,
                2
            ),

            "avg_win": round(
                avg_win,
                2
            ),

            "avg_loss": round(
                avg_loss,
                2
            ),

            "max_drawdown": round(
                max_drawdown,
                2
            ),

            "final_capital": round(
                self.final_capital,
                2
            ),

            "strategy_summary": strategy_summary,

            "regime_summary": regime_summary
        }