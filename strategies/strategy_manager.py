class StrategyManager:


    def __init__(self, selector):

        self.selector = selector



    def generate_signals(self, df, regime):


        active_strategies = (
            self.selector.select(regime)
        )


        signals = []


        for strategy in active_strategies:

            signal = strategy.generate_signal(df)

            signals.append({

                "strategy": strategy.name,

                "signal": signal

            })
        return signals


