import math
import backtrader as bt
from indicators.supertrend import SuperTrend

class SupertrendStrategy(bt.Strategy):
    params = (('period', 10), ('multiplier', 3))

    def __init__(self):
        # self.fast_moving_average = bt.indicators.SMA(
        #     self.data.close, period=self.params.fast, plotname="50 Day Moving Average"
        # )
        print("Supertrend Initialised")
        self.band = SuperTrend(
            self.data, period = self.params.period, multiplier = self.params.multiplier, plotname = "Supertrend 10 , 3"
        )

        # self.slow_moving_average = bt.indicators.SMA(
        #     self.data.close, period=self.params.slow, plotname="200 Day Moving Average"
        # )

        # self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        print("Supertrend")
        # if self.position.size == 0:
        #     print(self.band)
            # if self.crossover > 0:
            #     amount_to_invest = (self.params.order_percentage * self.broker.cash)
            #     self.size = math.floor(amount_to_invest / self.data.close)

            #     print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))

            #     self.buy(size=self.size)

        # if self.position.size > 0:
        #     print(self.band)
            # if self.crossover < 0:
            #     print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
            #     self.close()