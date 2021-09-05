import backtrader as bt

class Alligator(bt.Indicator):
    """
    Alligator indicator
    """
    params = (('jaw_length',13),('teeth_length',8), ('lips_length',5),('jaw_offset',8), ('teeth_offset',5),('lips_offset',3))
    lines = ('jaw','teeth','lips')
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.average = (self.data.high + self.data.low) / 2

    def next(self):
        self.jaw = bt.indicators.SmoothedMovingAverage(self.average, period=self.params.jaw_length, plotname='Jaw')(self.params.jaw_offset)
        self.teeth = bt.indicators.SmoothedMovingAverage(self.average, period=self.params.teeth_length, plotname='Teeth')(self.params.teeth_offset)
        self.lips = bt.indicators.SmoothedMovingAverage(self.average, period=self.params.lips_length, plotname='Lips')(self.params.lips_offset)