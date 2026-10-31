import pandas as pd
from .base_pattern import BasePattern


class BullishFVGPattern(BasePattern):

    def __init__(self):
        super().__init__("Bullish FVG")


    def detect(self, df):

        """
        Bullish FVG:

        Candle[i].low > Candle[i-2].high

        Example:

        Candle 1 High = 100
        Candle 3 Low  = 102

        Gap = 100-102

        """

        return (
            df["low"] >
            df["high"].shift(2)
        )



class BearishFVGPattern(BasePattern):

    def __init__(self):
        super().__init__("Bearish FVG")


    def detect(self, df):

        """
        Bearish FVG:

        Current High < Previous 2 candle Low
        """

        return (
            df["high"] <
            df["low"].shift(2)
        )