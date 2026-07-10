from statistics import mean


class GoldStrategy:


    def __init__(
        self,
        fast_period=5,
        slow_period=20
    ):

        self.fast_period = fast_period
        self.slow_period = slow_period



    def analyze(
        self,
        prices
    ):

        if len(prices) < self.slow_period:

            return {
                "signal":"HOLD",
                "reason":"not enough data"
            }



        fast_ma = mean(
            prices[-self.fast_period:]
        )


        slow_ma = mean(
            prices[-self.slow_period:]
        )



        if fast_ma > slow_ma:

            return {

                "signal":"BUY",

                "fast_ma":fast_ma,

                "slow_ma":slow_ma

            }



        elif fast_ma < slow_ma:

            return {

                "signal":"SELL",

                "fast_ma":fast_ma,

                "slow_ma":slow_ma

            }



        return {

            "signal":"HOLD",

            "fast_ma":fast_ma,

            "slow_ma":slow_ma

        }