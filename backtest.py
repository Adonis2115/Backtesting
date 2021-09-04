import datetime
import backtrader as bt
import backtrader.feeds as btfeed
from strategies.dip import BuyDip
from strategies.sma import SmaCross
from strategies.goldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from indicators.supertrend import SuperTrend
# from indicators.supertrend import SuperTrendBand

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

cerebro.broker.set_cash(1000000)
print(cerebro.broker.getvalue())

# Create a data feed
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

data1 = bt.feeds.YahooFinanceCSVData(
    dataname = './Data/Yahoo/BTC-USD.csv',
    fromdate=datetime.datetime(2018, 1, 4),
    todate=datetime.datetime(2021, 9, 4),
    reverse = False
)

# use this if you want to change data to higher time frame
cerebro.resampledata(data1,
                         timeframe=bt.TimeFrame.Days,
                         compression=1)

# cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SuperTrend)
cerebro.run()
print(cerebro.broker.getvalue())
cerebro.plot()
