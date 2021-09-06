import math
import backtrader as bt
from indicators.pivots import PivotPoint

class PivotStrategy(bt.Strategy):
    def __init__(self):
        self.pp = PivotPoint(self.data1)