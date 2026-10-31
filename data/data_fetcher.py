import yfinance as yf
import pandas as pd


class DataFetcher:
    def __init__(self, symbol, interval="15m", period="60d"):
        self.symbol = symbol
        self.interval = interval
        self.period = period

    def fetch(self):
        ticker = yf.Ticker(self.symbol)
        df = ticker.history(interval=self.interval, period=self.period)

        if df.empty:
            raise ValueError("No data fetched")

        # ✅ Keep datetime as index (DO NOT reset)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None)

        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })


        return df
