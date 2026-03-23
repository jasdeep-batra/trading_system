from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def generate_signal(self, df):
        """
        Must be implemented by every strategy.
        Returns:
            1  -> BUY
            0  -> HOLD
           -1 -> SELL
        """
        pass