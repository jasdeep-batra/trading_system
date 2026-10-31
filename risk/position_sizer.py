class PositionSizer:

    def __init__(self, capital, risk_per_trade):
        self.capital = capital
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(self, entry_price, stop_loss):

        risk_amount = self.capital * self.risk_per_trade
        risk_per_share = abs(entry_price - stop_loss)

        if risk_per_share == 0:
            return 0

        quantity = risk_amount / risk_per_share

        return int(quantity)