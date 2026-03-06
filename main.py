from data.data_fetcher import DataFetcher
from indicators.indicator_engine import IndicatorEngine


if __name__ == "__main__":

    fetcher = DataFetcher("RELIANCE.NS", interval="15m")
    data = fetcher.fetch()

    engine = IndicatorEngine(data)

    df = (
        engine
        .add_ema(20)
        .add_ema(50)
        .add_rsi()
        .add_atr()
        .add_adx()
        .get_dataframe()
    )

    print(df.tail())
