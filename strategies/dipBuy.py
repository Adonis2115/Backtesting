import backtrader as bt

class DipBuy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.slow = bt.indicators.SMA(
            self.data.close, period=200, plotname="200 Day Moving Average"
        )
        self.rsi = bt.indicators.RSI(self.data.close, period=10)
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi[-1] <= 50 and self.rsi[0] > 50:
                self.buyPrice = self.datas[0].close
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:
            if self.datas[0].close[0] < self.buyPrice * 0.995 or self.rsi[0] < 45 or self.datas[0].close > self.buyPrice * 1.005:
                self.log('SELL CREATED {}'. format(self.dataclose[0]))
                self.order = self.sell()
