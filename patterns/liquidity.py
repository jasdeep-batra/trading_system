import pandas as pd
from .base_pattern import BasePattern


class BullishLiquiditySweep(BasePattern):

    def __init__(self):
        super().__init__("Bullish Liquidity Sweep")


    def detect(self, df):

        wick_condition = (
            df["lower_wick"] >
            df["body"] * 2
        )


        sweep = (
            (df["low"] < df["swing_low_10"])
            &
            (df["close"] > df["swing_low_10"])
            &
            wick_condition
        )


        return sweep



class BearishLiquiditySweep(BasePattern):

    def __init__(self):
        super().__init__("Bearish Liquidity Sweep")


    def detect(self, df):

        wick_condition = (
            df["upper_wick"] >
            df["body"] * 2
        )


        sweep = (
            (df["high"] > df["swing_high_10"])
            &
            (df["close"] < df["swing_high_10"])
            &
            wick_condition
        )


        return sweep