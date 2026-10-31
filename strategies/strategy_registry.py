from strategies.trend_strategy import TrendStrategy
from strategies.breakout_strategy import BreakoutStrategy
from strategies.pullback_strategy import PullbackStrategy
from strategies.smc_strategy import SMCStructuralLiquidityStrategy


class StrategyRegistry:


    def __init__(self):

        self.strategies = {

            "trend": TrendStrategy(),

            "breakout": BreakoutStrategy(),

            "pullback": PullbackStrategy(),

            "smc": SMCStructuralLiquidityStrategy()

        }


    def get(self, name):

        return self.strategies.get(name)


    def get_all(self):

        return self.strategies