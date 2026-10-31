class BacktestEngine:

    def __init__(
        self,
        df,
        strategy_manager,
        position_sizer,
        risk_manager,
        regime_classifier
    ):

        self.df = df

        self.strategy_manager = strategy_manager

        self.position_sizer = position_sizer

        self.risk_manager = risk_manager

        self.regime_classifier = regime_classifier


        self.trades = []

        self.capital = position_sizer.capital

        self.last_trade_candle_index = -10


        self.daily_loss_limit = (
            0.02 * self.capital
        )

        self.daily_loss = 0

        self.current_day = None

    
    def _handle_buy(self, current_index, row, signals, regime):

        if self.capital <= 0:
            return

        if (current_index - self.last_trade_candle_index) < 4:
            return

        open_trades = [
            t for t in self.trades
            if t["status"] == "OPEN"
        ]

        if len(open_trades) >= 2:
            return

        if not self.risk_manager.can_take_trade():
            return


        price = row["close"]

        stop_loss = price - (2 * row["atr"])

        risk_per_share = price - stop_loss

        if risk_per_share <= 0:
            return


        target = price + (2 * risk_per_share)


        quantity = self.position_sizer.calculate_position_size(
            price,
            stop_loss
        )


        if quantity == 0:
            return


        # ============================
        # Identify actual strategies
        # ============================

        active_strategies = [
            s["strategy"]
            for s in signals
            if s["signal"] == 1
        ]


        trade = {

            "entry_price": price,

            "stop_loss": stop_loss,

            "target": target,

            "quantity": quantity,

            "status": "OPEN",

            "regime": regime,

            "strategies": [
                s["strategy"]
                for s in signals
                if s["signal"] == 1
            ]
        }


        self.trades.append(trade)


        self.risk_manager.register_trade()


        self.last_trade_candle_index = current_index
        
    def _update_trades(self, row):

        for trade in self.trades:

            if trade["status"] != "OPEN":
                continue

            exit_price = None

            # Stop Loss Hit
            if row["low"] <= trade["stop_loss"]:

                exit_price = trade["stop_loss"]

            # Target Hit
            elif row["high"] >= trade["target"]:

                exit_price = trade["target"]

            else:
                continue

            trade["exit_time"] = row.name

            trade["exit_price"] = exit_price

            trade["status"] = "CLOSED"

            pnl = (
                exit_price -
                trade["entry_price"]
            ) * trade["quantity"]

            trade["pnl"] = pnl

            self.capital += pnl

            # Update daily loss
            if pnl < 0:
                self.daily_loss += abs(pnl)

            self.risk_manager.close_trade()
            
    def run(self):

        for i in range(50, len(self.df)):


            # =========================
            # Capital Protection
            # =========================

            if self.capital <= 0:
                break



            current_df = self.df.iloc[:i]

            latest = current_df.iloc[-1]



            # =========================
            # Daily Loss Reset
            # =========================

            current_day = latest.name.date()


            if self.current_day != current_day:

                self.current_day = current_day

                self.daily_loss = 0



            # =========================
            # Daily Loss Protection
            # =========================

            if self.daily_loss >= self.daily_loss_limit:

                continue



            # =========================
            # Update Existing Trades
            # =========================

            self._update_trades(latest)



            # =========================
            # Market Regime Detection
            # =========================

            regime = (
                self.regime_classifier
                .classify(current_df)
            )



            # No trade in unclear market
            if regime == "NEUTRAL":

                continue



            # =========================
            # Strategy Execution
            # =========================

            signals = (
                self.strategy_manager
                .generate_signals(
                    current_df,
                    regime
                )
            )



            # =========================
            # Consensus Logic
            # =========================

            buy_signals = [

                s for s in signals

                if s["signal"] == 1

            ]



            if len(buy_signals) >= 2:

                self._handle_buy(
                    i,
                    latest,
                    signals,
                    regime
                )



        return self.trades