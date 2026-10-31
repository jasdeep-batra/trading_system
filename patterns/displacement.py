from .base_pattern import BasePattern


class BullishDisplacementPattern(BasePattern):

    def __init__(self):
        super().__init__(
            "Bullish Displacement"
        )


    def detect(self, df):

        # Candle body size
        body = abs(
            df["close"] - df["open"]
        )


        # Average candle body
        avg_body = (
            body
            .rolling(20)
            .mean()
        )


        return (

            # Strong bullish candle
            (df["close"] > df["open"])

            &

            # Current body larger than recent average
            (body > avg_body * 1.5)

            &

            # Avoid tiny candles
            (body > df["atr"] * 0.5)

        )



class BearishDisplacementPattern(BasePattern):

    def __init__(self):
        super().__init__(
            "Bearish Displacement"
        )


    def detect(self, df):

        body = abs(
            df["close"] - df["open"]
        )


        avg_body = (
            body
            .rolling(20)
            .mean()
        )


        return (

            (df["close"] < df["open"])

            &

            (body > avg_body * 1.5)

            &

            (body > df["atr"] * 0.5)

        )