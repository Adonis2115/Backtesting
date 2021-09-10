# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
import math
# from . import Indicator, CmpEx
import backtrader as bt

class PivotStrategy(bt.Strategy):
    def __init__(self):
        pivotindicator = bt.ind.PivotPoint(self.data1)