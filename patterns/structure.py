import pandas as pd
from .base_pattern import BasePattern


class BullishMSSPattern(BasePattern):

    def __init__(self):
        super().__init__("Bullish MSS")


    def detect(self, df):

        return (
            df["close"] >
            df["swing_high_10"]
        )



class BearishMSSPattern(BasePattern):

    def __init__(self):
        super().__init__("Bearish MSS")


    def detect(self, df):

        return (
            df["close"] <
            df["swing_low_10"]
        )