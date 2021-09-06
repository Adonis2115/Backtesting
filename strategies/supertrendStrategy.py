import math
import backtrader as bt
from indicators.supertrend import SuperTrend

class SupertrendStrategy(bt.Strategy):
    params = (('period', 10), ('multiplier', 3), ('order_percentage', 0.95), ('ticker', 'Banknifty'))

    def __init__(self):
        self.band = SuperTrend(
            self.data, period = self.params.period, multiplier = self.params.multiplier, plotname = "Supertrend 10 , 3"
        )

    def next(self):
        if self.position.size == 0:
            if self.data.close > self.band:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.data.close < self.band:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()