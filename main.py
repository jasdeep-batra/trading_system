from data.data_fetcher import DataFetcher
from indicators.indicator_engine import IndicatorEngine
from strategies.trend_strategy import TrendStrategy

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

    strategy = TrendStrategy()

    signal = strategy.generate_signal(df)

    print("Signal:", signal)