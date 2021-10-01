import backtrader as bt
from indicators.alligator import Alligator
from indicators.supertrend import SuperTrend

# Create a Stratey
class StopOrderSubmit(bt.Strategy):
    params = (('jaw_length', 13), ('teeth_length', 8), ('lips_length', 5), ('jaw_offset', 8), ('teeth_offset', 5), ('lips_offset', 3), ('order_percentage', 0.95), ('ticker', 'Banknifty'), ('period', 10), ('multiplier', 3))
    plotinfo = dict(subplot=True)
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    # Order Notification System
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))
        self.order = None

    def __init__(self):
        self.alligator = Alligator(
            self.data, jaw_length = self.params.jaw_length, teeth_length = self.params.teeth_length, lips_length = self.params.lips_length, jaw_offset = self.params.jaw_offset, teeth_offset = self.params.teeth_offset, lips_offset = self.params.lips_offset, plotname = "Alligator",
        )
        self.alligator.plotinfo.plotskip = dict(
            jaw=dict(plotskip=False),
            teeth=dict(plotskip=True),
            lips=dict(plotskip=True),
        )
        self.supertrend = SuperTrend(
            self.data, period = self.params.period, multiplier = self.params.multiplier, plotname = "Supertrend 10 , 3"
        )
        self.pivotindicator = bt.ind.PivotPoint(self.data1)
        self.order = self.stopLoss = self.targetOrder = None

    def next(self):
        # Update Stop Loss (Trailing) Traget Order was also getting cancelled so made new target Orders as well
        if self.position.size < 0:
            if self.data.low[0] < self.lastLow:
                trailedAmount = (self.lastLow - self.data.low[0])/2
                self.tsl = self.tsl - trailedAmount
                self.lastLow = self.data.low[0]
                self.cancel(self.stopLoss)
                self.stopLoss = self.buy(exectype=bt.Order.Stop, size=self.size, price=self.tsl)
                self.targetOrder = self.buy(exectype=bt.Order.Limit, size=self.size, price=self.target, oco=self.stopLoss)
        # LONG Trade Trailing Update
        if(self.position.size > 0 and self.data.high[0] > self.lastHigh):
            trailedAmount = (self.data.high[0] - self.lastHigh)/2
            self.tsl = self.tsl + trailedAmount
            self.lastHigh = self.data.high[0]
            self.cancel(self.stopLoss)
            self.stopLoss = self.sell(exectype=bt.Order.Stop, size=self.size, price=self.tsl)
            self.targetOrder = self.sell(exectype=bt.Order.Limit, size=self.size, price=self.target, oco=self.stopLoss)
        isAlligator = self.data.close[0] > self.alligator.jaw
        isSupertrend = self.data.close[0] > self.supertrend
        if not self.position and self.order is None:
            # SHORT Trade
            if not isAlligator and not isSupertrend and self.datas[0].datetime.time().hour < 15:
                isP = self.data.close[0] < self.pivotindicator.lines.p[0] and self.data.open[0] > self.pivotindicator.lines.p[0]
                isS1 = self.data.close[0] < self.pivotindicator.s1[0] and self.data.open[0] > self.pivotindicator.s1[0]
                isS1 = self.data.close[0] < self.pivotindicator.s1[0] and self.data.open[0] > self.pivotindicator.s1[0]
                isS2 = self.data.close[0] < self.pivotindicator.s2[0] and self.data.open[0] > self.pivotindicator.s2[0]
                isR1 = self.data.close[0] < self.pivotindicator.r1[0] and self.data.open[0] > self.pivotindicator.r1[0]
                isR2 = self.data.close[0] < self.pivotindicator.r2[0] and self.data.open[0] > self.pivotindicator.r2[0]
                if  isP or isS1 or isS2 or isR1 or isR2:
                    if isP:
                        self.pivotLevel = self.pivotindicator.lines.p[0]
                    elif isS1:
                        self.pivotLevel = self.pivotindicator.lines.s1[0]
                    elif isS2:
                        self.pivotLevel = self.pivotindicator.lines.s2[0]
                    elif isR1:
                        self.pivotLevel = self.pivotindicator.lines.r1[0]
                    elif isR2:
                        self.pivotLevel = self.pivotindicator.lines.r2[0]
                    self.sellPrice = self.data.low[0]
                    self.lastLow = self.data.low[0]
                    self.isValid = True
                    self.size = -25
                    self.log('SELL CREATE, %.2f' % self.data.low[0])
                    if self.data.high[0] - self.data.low[0] > 200:
                        self.sl = self.tsl = self.data.low[0] + 200
                        self.target = self.data.low[0] - (2*200)
                    else:
                        self.sl = self.tsl = self.data.high[0]
                        self.target = self.data.low[0] - 2*(self.data.high[0] - self.data.low[0])
                    self.order = self.sell(exectype=bt.Order.Stop, size=self.size, price=self.data.low[0], transmit=False)
                    self.log('STOP LOSS is, %.2f' % self.tsl)
                    self.log('TARGET is, %.2f' % self.target)
                    self.stopLoss = self.buy(exectype=bt.Order.Stop, size=self.size, price=self.tsl, parent=self.order)
                    self.targetOrder = self.buy(exectype=bt.Order.Limit, size=self.size, price=self.target, parent=self.order, oco=self.stopLoss)
            
            #LONG Trade
            if isAlligator and isSupertrend and self.datas[0].datetime.time().hour < 15:
                isP = self.data.close[0] > self.pivotindicator.lines.p[0] and self.data.open[0] < self.pivotindicator.lines.p[0]
                isS1 = self.data.close[0] > self.pivotindicator.s1[0] and self.data.open[0] < self.pivotindicator.s1[0]
                isS2 = self.data.close[0] > self.pivotindicator.s2[0] and self.data.open[0] < self.pivotindicator.s2[0]
                isR1 = self.data.close[0] > self.pivotindicator.r1[0] and self.data.open[0] < self.pivotindicator.r1[0]
                isR2 = self.data.close[0] > self.pivotindicator.r2[0] and self.data.open[0] < self.pivotindicator.r2[0]
                if isP or isS1 or isS2 or isR1 or isR2:
                    if isP:
                        self.pivotLevel = self.pivotindicator.lines.p[0]
                    elif isS1:
                        self.pivotLevel = self.pivotindicator.lines.s1[0]
                    elif isS2:
                        self.pivotLevel = self.pivotindicator.lines.s2[0]
                    elif isR1:
                        self.pivotLevel = self.pivotindicator.lines.r1[0]
                    elif isR2:
                        self.pivotLevel = self.pivotindicator.lines.r2[0]
                    self.buyPrice = self.data.high[0]
                    self.lastHigh = self.data.high[0]
                    self.isValid = True
                    self.size = 25
                    self.log('BUY CREATE, %.2f' % self.data.high[0])
                    if self.data.high[0] - self.data.low[0] > 200:
                        self.sl = self.tsl = self.data.high[0] - 200
                        self.target = self.data.high[0] + (2*200)
                    else:
                        self.sl = self.tsl = self.data.low[0]
                        self.target = self.data.high[0] + 2*(self.data.high[0] - self.data.low[0])
                    self.order = self.buy(exectype=bt.Order.Stop, size=self.size, price=self.data.high[0], transmit=False)
                    self.log('STOP LOSS is, %.2f' % self.tsl)
                    self.log('TARGET is, %.2f' % self.target)
                    self.stopLoss = self.sell(exectype=bt.Order.Stop, size=self.size, price=self.tsl, parent=self.order)
                    self.targetOrder = self.sell(exectype=bt.Order.Limit, size=self.size, price=self.target, parent=self.order, oco=self.stopLoss)

        if self.order:
            # SHORT Trade Order Cancel if conditions nullifies
            if self.order.size < 0:
                if isAlligator or isSupertrend or self.datas[0].datetime.time().hour >= 15 or self.data.close[0] > self.pivotLevel:
                    self.isValid = False
                    self.log('SELL CANCELLED')
                    self.cancel(self.order)
            # LONG Trade Order Cancel
            if self.order.size > 0:
                if not isAlligator or  not isSupertrend or self.datas[0].datetime.time().hour >= 15 or self.data.close[0] < self.pivotLevel:
                    self.isValid = False
                    self.log('BUY CANCELLED')
                    self.cancel(self.order)

        # Trade Closing and Order cancelling after 3 PM
        if self.position.size > 0 or self.position.size < 0 and self.datas[0].datetime.time().hour >= 15:
            self.log('TRADING TIME OVER, %.2f' % self.datas[0].datetime.time().hour)
            self.close(self.order)
            self.cancel(self.stopLoss)
            self.cancel(self.targetOrder)