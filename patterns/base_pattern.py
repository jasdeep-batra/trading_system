from abc import ABC, abstractmethod
import pandas as pd


class BasePattern(ABC):

    def __init__(self, name):
        self.name = name


    @abstractmethod
    def detect(self, df: pd.DataFrame) -> pd.Series:
        """
        Must return boolean pandas Series.

        Example:

        True  -> Pattern detected
        False -> No pattern

        """

        pass