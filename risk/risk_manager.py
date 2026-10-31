class RiskManager:

    def __init__(self, max_open_trades):
        self.max_open_trades = max_open_trades
        self.current_open_trades = 0

    def can_take_trade(self):
        return self.current_open_trades < self.max_open_trades

    def register_trade(self):
        self.current_open_trades += 1

    def close_trade(self):
        if self.current_open_trades > 0:
            self.current_open_trades -= 1

    def validate_stop_loss(self, entry, stop_loss):
        return entry != stop_loss