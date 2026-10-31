from config import (
    SYMBOLS,
    INITIAL_CAPITAL,
    RISK_PER_TRADE,
    MAX_OPEN_TRADES
)

import config


from data.data_fetcher import DataFetcher

from indicators.indicator_engine import IndicatorEngine

from strategies.strategy_registry import StrategyRegistry
from strategies.strategy_selector import StrategySelector
from strategies.strategy_manager import StrategyManager

from risk.position_sizer import PositionSizer
from risk.risk_manager import RiskManager

from regime.regime_classifier import RegimeClassifier

from backtester.engine import BacktestEngine
from backtester.metrics import PerformanceMetrics



for symbol in SYMBOLS:


    print("\n==============================")
    print(f"Running for: {symbol}")
    print("==============================")


    # ===================================
    # Fetch Market Data
    # ===================================

    fetcher = DataFetcher(
    symbol,
    interval="1h",
    period="2y"
)
    data = fetcher.fetch()



    # ===================================
    # Indicator Pipeline
    # ===================================

    df = (
        IndicatorEngine(data)

        .add_ema(20)

        .add_ema(50)

        .add_sma(200)

        .add_rsi()

        .add_atr()

        .add_adx()

        .add_candle_features()

        .add_market_structure_features()

        .get_dataframe()
    )



    # ===================================
    # Strategy Architecture
    # ===================================

    registry = StrategyRegistry()


    selector = StrategySelector(
        registry
    )


    strategy_manager = StrategyManager(
        selector
    )



    # ===================================
    # Risk Management
    # ===================================

    risk_manager = RiskManager(
        MAX_OPEN_TRADES
    )


    position_sizer = PositionSizer(
        INITIAL_CAPITAL,
        RISK_PER_TRADE
    )



    # ===================================
    # Market Regime
    # ===================================

    regime_classifier = RegimeClassifier(
        config
    )



    # ===================================
    # Backtesting
    # ===================================

    backtester = BacktestEngine(

        df=df,

        strategy_manager=strategy_manager,

        position_sizer=position_sizer,

        risk_manager=risk_manager,

        regime_classifier=regime_classifier
    )


    trades = backtester.run()



    # ===================================
    # Performance Metrics
    # ===================================

    metrics = PerformanceMetrics(
    trades,
    INITIAL_CAPITAL,
    backtester.capital
)

    result = metrics.calculate()

    print("\n===== PERFORMANCE =====")

    for key, value in result.items():

        if key in [
            "strategy_summary",
            "regime_summary"
        ]:
            continue

        print(f"{key}: {value}")

    print("\n===== Strategy Performance =====")

    for strategy, pnl in result[
        "strategy_summary"
    ].items():

        print(
            f"{strategy}: {round(pnl,2)}"
        )

    print("\n===== Regime Performance =====")

    for regime, pnl in result[
        "regime_summary"
    ].items():

        print(
            f"{regime}: {round(pnl,2)}"
        )