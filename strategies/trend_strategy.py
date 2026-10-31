from strategies.base_strategy import BaseStrategy
class TrendStrategy(BaseStrategy):

    def __init__(self):
        super().__init__("Trend Strategy")

    def generate_signal(self, df):

        if len(df) < 50:
            return 0

        latest = df.iloc[-1]

        if (
            latest['ema_20'] > latest['ema_50'] and
            latest['adx'] > 25 and
            latest['close'] > latest['ema_20']
        ):
            return 1

        return 0