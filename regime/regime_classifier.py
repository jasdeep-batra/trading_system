class RegimeClassifier:
    def __init__(self, config):
        self.adx_threshold_trend = config.ADX_TREND_THRESHOLD   # e.g. 25
        self.adx_threshold_range = config.ADX_RANGE_THRESHOLD   # e.g. 20
        self.slope_lookback = config.EMA_SLOPE_LOOKBACK         # e.g. 5
        self.slope_threshold = config.EMA_SLOPE_THRESHOLD       # tune this

    def calculate_slope(self, series):
        return series.iloc[-1] - series.iloc[-self.slope_lookback]

    def is_trending(self, df):
        adx = df['adx'].iloc[-1]
        ema50 = df['ema_50']

        slope = self.calculate_slope(ema50)

        price = df['close'].iloc[-1]

        # Direction consistency check
        above = price > ema50.iloc[-1]

        if adx >= self.adx_threshold_trend and abs(slope) > self.slope_threshold:
            return True

        return False

    def is_ranging(self, df):
        adx = df['adx'].iloc[-1]

        if adx <= self.adx_threshold_range:
            return True

        return False

    def classify(self, df):
        if self.is_trending(df):
            return "TRENDING"

        if self.is_ranging(df):
            return "RANGING"

        return "NEUTRAL"