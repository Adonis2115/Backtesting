import math
import backtrader as bt
from indicators.alligator import Alligator

class AlligatorStrategy(bt.Strategy):
    params = (('jaw_length', 13), ('teeth_length', 8), ('lips_length', 5), ('jaw_offset', 8), ('teeth_offset', 5), ('lips_offset', 3), ('order_percentage', 0.95), ('ticker', 'Banknifty'))

    def __init__(self):
        print("Alligator Initialised")
        self.band = Alligator(
            self.data, jaw_length = self.params.jaw_length, teeth_length = self.params.teeth_length, lips_length = self.params.lips_length, jaw_offset = self.params.jaw_offset, teeth_offset = self.params.teeth_offset, lips_offset = self.params.lips_offset, plotname = "Alligator"
        )
        # self.band = Alligator(
        #     self.data, plotname = "Alligator"
        # )

    def next(self):
        print("Alligator")
        # if self.position.size == 0:
        #     if self.data.close > self.band:
        #         amount_to_invest = (self.params.order_percentage * self.broker.cash)
        #         self.size = math.floor(amount_to_invest / self.data.close)

        #         print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))

        #         self.buy(size=self.size)

        # if self.position.size > 0:
        #     if self.data.close < self.band:
        #         print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
        #         self.close()