from strategies.base_strategy import BaseStrategy


class PullbackStrategy(BaseStrategy):

    def __init__(self):
        super().__init__("Pullback Strategy")

    def generate_signal(self, df):

        if len(df) < 50:
            return 0

        latest = df.iloc[-1]

        # Trend condition
        trend_up = latest['ema_20'] > latest['ema_50']

        # Pullback condition
        pullback = latest['close'] <= latest['ema_20'] * 1.01   # allow slight above EMA

        rsi_ok = 35 < latest['rsi'] < 65   # widen band

        # Trend strength
        strong_trend = latest['adx'] > 20

        if trend_up and pullback and rsi_ok and strong_trend:
            return 1

        return 0