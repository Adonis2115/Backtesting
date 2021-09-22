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
                self.size = 50
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.data.close < self.band:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()