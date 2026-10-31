from strategies.base_strategy import BaseStrategy
class BreakoutStrategy(BaseStrategy):

    def __init__(self):
        super().__init__("Breakout Strategy")

    def generate_signal(self, df):

        if len(df) < 50:
            return 0

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        if (
            latest['close'] > prev['high'] and
            latest['volume'] > df['volume'].rolling(20).mean().iloc[-1]
        ):
            return 1

        return 0