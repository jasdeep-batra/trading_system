    def __init__(self, df, strategy_manager, position_sizer, risk_manager):
        self.df = df
        self.strategy_manager = strategy_manager
        self.position_sizer = position_sizer
        self.risk_manager = risk_manager

        self.trades = []
        self.capital = position_sizer.capital
        self.last_trade_candle_index = -10