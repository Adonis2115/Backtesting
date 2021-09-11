import math
import backtrader as bt
from indicators.alligator import Alligator
from indicators.pivots import PivotPoint
from indicators.supertrend import SuperTrend

class ArjunBhatiaFutures(bt.Strategy):
    params = (('jaw_length', 13), ('teeth_length', 8), ('lips_length', 5), ('jaw_offset', 8), ('teeth_offset', 5), ('lips_offset', 3), ('order_percentage', 0.95), ('ticker', 'Banknifty'), ('period', 10), ('multiplier', 3))
    sl = target = None
    def __init__(self):
        self.alligator = Alligator(
            self.data, jaw_length = self.params.jaw_length, teeth_length = self.params.teeth_length, lips_length = self.params.lips_length, jaw_offset = self.params.jaw_offset, teeth_offset = self.params.teeth_offset, lips_offset = self.params.lips_offset, plotname = "Alligator"
        )
        self.supertrend = SuperTrend(
            self.data, period = self.params.period, multiplier = self.params.multiplier, plotname = "Supertrend 10 , 3"
        )
        self.pivotindicator = bt.ind.PivotPoint(self.data1)

    # Pivot is not working need to modify
    def next(self):
        if self.position.size == 0:
            isAlligator = self.data.close[-1] > self.alligator.jaw
            isSupertrend = self.data.close[-1] > self.supertrend
            isP = self.data.close[-1] > self.pivotindicator.lines.p[0] and self.data.open[-1] < self.pivotindicator.lines.p[0]
            isS1 = self.data.close[-1] > self.pivotindicator.s1[0] and self.data.open[-1] < self.pivotindicator.s1[0]
            isS2 = self.data.close[-1] > self.pivotindicator.s2[0] and self.data.open[-1] < self.pivotindicator.s2[0]
            isR1 = self.data.close[-1] > self.pivotindicator.r1[0] and self.data.open[-1] < self.pivotindicator.r1[0]
            isR2 = self.data.close[-1] > self.pivotindicator.r2[0] and self.data.open[-1] < self.pivotindicator.r2[0]
            if isAlligator and  isSupertrend and  (isP or isS1 or isS2 or isR1 or isR2) and self.data.high[0] >= self.data.high[-1] and self.datas[0].datetime.time().hour >= 9: #if new high is higher than previous high then buy would have been taken
                # amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = 2
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.high[-1]))
                if self.data.high[-1] - self.data.low[-1] > 200:
                    self.sl = self.data.high[-1] - 200
                    self.target = self.data.high[-1] + (2*200)
                else:
                    self.sl = self.data.low[-1]
                    self.target = self.data.high[-1] + 2*(self.data.high[-1] - self.data.low[-1])
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.data.low[0] <= self.sl:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.sl))
                self.close()
            if  self.data.high[0] >= self.target or self.datas[0].datetime.time().hour >= 15:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()