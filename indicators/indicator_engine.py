import pandas as pd
import ta


class IndicatorEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def add_ema(self, period: int):
        self.df[f'ema_{period}'] = ta.trend.ema_indicator(
            close=self.df['close'],
            window=period
        )
        return self

    def add_rsi(self, period: int = 14):
        self.df['rsi'] = ta.momentum.rsi(
            close=self.df['close'],
            window=period
        )
        return self

    def add_atr(self, period: int = 14):
        self.df['atr'] = ta.volatility.average_true_range(
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            window=period
        )
        return self

    def add_adx(self, period: int = 14):
        self.df['adx'] = ta.trend.adx(
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            window=period
        )
        return self

    def get_dataframe(self):
        return self.df
