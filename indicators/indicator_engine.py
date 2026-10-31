import pandas as pd
import numpy as np
import ta


class IndicatorEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()


    # ==========================
    # Trend Indicators
    # ==========================

    def add_ema(self, period: int):

        self.df[f'ema_{period}'] = ta.trend.ema_indicator(
            close=self.df['close'],
            window=period
        )

        return self


    def add_sma(self, period: int):

        self.df[f'sma_{period}'] = (
            self.df['close']
            .rolling(window=period)
            .mean()
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


    # ==========================
    # Price Action Features
    # ==========================

    def add_candle_features(self):

        # Candle body size
        self.df['body'] = (
            abs(
                self.df['close'] -
                self.df['open']
            )
        )


        # Bullish candle
        self.df['bullish_candle'] = (
            self.df['close'] >
            self.df['open']
        )


        # Bearish candle
        self.df['bearish_candle'] = (
            self.df['close'] <
            self.df['open']
        )


        # Upper wick
        self.df['upper_wick'] = (
            self.df['high'] -
            self.df[['open', 'close']].max(axis=1)
        )


        # Lower wick
        self.df['lower_wick'] = (
            self.df[['open', 'close']].min(axis=1)
            -
            self.df['low']
        )


        # Full candle range
        self.df['candle_range'] = (
            self.df['high'] -
            self.df['low']
        )


        return self



    # ==========================
    # Liquidity / Structure Data
    # ==========================

    def add_market_structure_features(self):

        # Recent 20 candle range
        self.df['high_20'] = (
            self.df['high']
            .rolling(20)
            .max()
        )


        self.df['low_20'] = (
            self.df['low']
            .rolling(20)
            .min()
        )


        # Previous swing high
        # shift prevents look-ahead bias
        self.df['swing_high_10'] = (
            self.df['high']
            .shift(1)
            .rolling(10)
            .max()
        )


        # Previous swing low
        self.df['swing_low_10'] = (
            self.df['low']
            .shift(1)
            .rolling(10)
            .min()
        )


        return self



    # ==========================
    # Final DataFrame
    # ==========================

    def get_dataframe(self):

        return self.df