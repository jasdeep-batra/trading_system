from strategies.base_strategy import BaseStrategy


class TrendStrategy(BaseStrategy):

    def __init__(self):
        super().__init__("Trend Strategy")

    def generate_signal(self, df):

        latest = df.iloc[-1]

        if latest['ema_20'] > latest['ema_50'] and latest['adx'] > 20:
            return 1

        elif latest['ema_20'] < latest['ema_50'] and latest['adx'] > 20:
            return -1

        return 0