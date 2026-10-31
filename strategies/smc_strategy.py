import pandas as pd

from strategies.base_strategy import BaseStrategy

from patterns.fvg import (
    BullishFVGPattern,
    BearishFVGPattern
)

from patterns.liquidity import (
    BullishLiquiditySweep,
    BearishLiquiditySweep
)

from patterns.structure import (
    BullishMSSPattern,
    BearishMSSPattern
)

from patterns.displacement import (
    BullishDisplacementPattern,
    BearishDisplacementPattern
)


class SMCStructuralLiquidityStrategy(BaseStrategy):

    def __init__(self):

        super().__init__(
            "SMC Structural Liquidity Strategy"
        )

        self.bullish_fvg = BullishFVGPattern()
        self.bearish_fvg = BearishFVGPattern()

        self.buy_sweep = BullishLiquiditySweep()
        self.sell_sweep = BearishLiquiditySweep()

        self.buy_mss = BullishMSSPattern()
        self.sell_mss = BearishMSSPattern()

        self.buy_displacement = BullishDisplacementPattern()
        self.sell_displacement = BearishDisplacementPattern()
        self.bullish_sweep_active = False
        self.bearish_sweep_active = False

        self.sweep_candle_index = None

        self.confirmation_window = 5



    def generate_signal(self, df):

        """
        Returns:

        1  -> BUY
        0  -> HOLD
        -1 -> SELL

        """

        current_index = len(df) - 1
        latest = df.iloc[-1]


        # ==========================
        # HTF Trend Filter
        # ==========================

        bullish_htf = (
            latest["close"]
            >
            latest["sma_200"]
        )


        bearish_htf = (
            latest["close"]
            <
            latest["sma_200"]
        )


        # ==========================
        # Discount / Premium Zone
        # ==========================

        range_high = latest["high_20"]
        range_low = latest["low_20"]


        midpoint = (
            range_high +
            range_low
        ) / 2


        discount_zone = (
            latest["close"]
            <
            midpoint
        )


        premium_zone = (
            latest["close"]
            >
            midpoint
        )



        # ==========================
        # Detect patterns
        # ==========================

        bullish_sweep = (
            self.buy_sweep
            .detect(df)
            .iloc[-1]
        )


        bearish_sweep = (
            self.sell_sweep
            .detect(df)
            .iloc[-1]
        )


        bullish_mss = (
            self.buy_mss
            .detect(df)
            .iloc[-1]
        )


        bearish_mss = (
            self.sell_mss
            .detect(df)
            .iloc[-1]
        )


        bullish_fvg = (
            self.bullish_fvg
            .detect(df)
            .iloc[-1]
        )


        bearish_fvg = (
            self.bearish_fvg
            .detect(df)
            .iloc[-1]
        )


        bullish_displacement = (
            self.buy_displacement
            .detect(df)
            .iloc[-1]
        )


        bearish_displacement = (
            self.sell_displacement
            .detect(df)
            .iloc[-1]
        )

        # ==========================
        # BUY Logic
        # ==========================

        if bullish_htf and discount_zone and bullish_sweep:
            self.bullish_sweep_active = True
            self.sweep_candle_index = current_index


        if self.bullish_sweep_active:

            candles_after_sweep = current_index - self.sweep_candle_index

            if candles_after_sweep <= self.confirmation_window:

                if bullish_mss and bullish_displacement and bullish_fvg:
                    self.bullish_sweep_active = False
                    return 1

        else:
            self.bullish_sweep_active = False



        # ==========================
        # SELL Logic
        # ==========================

        if bearish_htf and premium_zone and bearish_sweep:
            self.bearish_sweep_active = True
            self.sweep_candle_index = current_index


        if self.bearish_sweep_active:

            candles_after_sweep = current_index - self.sweep_candle_index

            if candles_after_sweep <= self.confirmation_window:

                if bearish_mss and bearish_displacement and bearish_fvg:
                    self.bearish_sweep_active = False
                    return -1

            else:
                self.bearish_sweep_active = False



        return 0