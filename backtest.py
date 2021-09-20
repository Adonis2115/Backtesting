import datetime
from indicators.alligator import Alligator
import backtrader as bt
import backtrader.feeds as btfeed
from strategies.dip import BuyDip
from strategies.sma import SmaCross
from strategies.goldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.supertrendStrategy import SupertrendStrategy
from strategies.alligatorStrategy import AlligatorStrategy
from indicators.pivots import PivotPoint
from strategies.pivotStrategy import PivotStrategy
from strategies.ArjunBhatiaFutures import ArjunBhatiaFutures

cerebro = bt.Cerebro()

cerebro.broker.set_cash(1000000)

data = btfeed.GenericCSVData(
    dataname='./Data/Custom/BANKNIFTY.csv',

    fromdate=datetime.datetime(2020, 1, 1),
    todate=datetime.datetime(2020, 12, 31),
    nullvalue=0.0,
    dtformat=('%Y/%m/%d'),
    tmformat=('%H:%M'),

    timeframe=bt.TimeFrame.Minutes, compression=1,
    sessionstart=datetime.time(9, 16), sessionend=datetime.time(15, 33),

    datetime=1,
    time=2,
    high=4,
    low=5,
    open=3,
    close=6,
    volume=-1,
    openinterest=-1
)

data2 = bt.feeds.YahooFinanceCSVData(
    dataname = './Data/Yahoo/BTC-USD.csv',
    fromdate=datetime.datetime(2018, 1, 4),
    todate=datetime.datetime(2021, 9, 4),
    reverse = False
)

cerebro.resampledata(data,
                         timeframe=bt.TimeFrame.Minutes,
                         compression=15)
cerebro.resampledata(data,
                         timeframe=bt.TimeFrame.Days,
                         compression=1).plotinfo.plot=False


cerebro.addstrategy(ArjunBhatiaFutures)
cerebro.run()
cerebro.plot(style='candle', barup='green')
