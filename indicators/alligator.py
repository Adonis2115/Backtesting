import backtrader as bt

class Alligator(bt.Indicator):
    """
    Alligator indicator
    """
    params = (
        ('jaw_length',13),
        ('teeth_length',8),
        ('lips_length',5),
        ('jaw_offset',8),
        ('teeth_offset',5),
        ('lips_offset',3),
    )
    lines = ('jaw','teeth','lips')
    plotinfo = dict(subplot=False)
    plotlines = dict(
        jaw=dict(_plotskip=False),
        teeth=dict(_plotskip=True),
        lips=dict(_plotskip=True),
    )

    def __init__(self):
        self.average = (self.data.high + self.data.low) / 2 
        _jaw = bt.indicators.SmoothedMovingAverage(self.average, period=self.params.jaw_length, plotname='Jaw')
        self.lines.jaw =_jaw(-1 * self.params.jaw_offset)
        _teeth = bt.indicators.SmoothedMovingAverage(self.average, period=self.params.teeth_length, plotname='Teeth')
        self.lines.teeth = _teeth(-1 * self.params.teeth_offset)
        _lips =  bt.indicators.SmoothedMovingAverage(self.average, period=self.params.lips_length, plotname='Lips')
        self.lines.lips = _lips(-1 * self.params.lips_offset)