# import backtrader as bt

# class PivotPoint(bt.Indicator):
#     """
#     Alligator indicator
#     """
#     lines = ('p', 's1', 's2', 'r1', 'r2')
#     plotinfo = dict(subplot=False)

#     def __init__(self):
#         h = self.data.high  # current high
#         l = self.data.low  # current high
#         c = self.data.close  # current high

#         self.lines.p = p = (h + l + c) / 3.0

#         p2 = p * 2.0
#         self.lines.s1 = p2 - h  # (p x 2) - high
#         self.lines.r1 = p2 - l  # (p x 2) - low

#         hilo = h - l
#         self.lines.s2 = p - hilo  # p - (high - low)
#         self.lines.r2 = p + hilo  # p + (high - low)

import backtrader as bt

class PivotPoint(bt.Indicator):
    """
    Alligator indicator
    """
    lines = ("pivot", "s1", "r1", "s2", "r2", "s3", "r3")
    plotinfo = dict(subplot=False)

    def _init_(self):
        self.pivot = None
        self.prev_high = None
        self.prev_low = None

        self.current_high = -99999
        self.current_low = 99999
        self.current_close = -99999

        self.i = 0

    def next(self):
        if self.i > 0:
            if self.data.datetime.date(ago=0).day != self.data.datetime.date(ago=-1).day:
                self.pivot = (self.current_high + self.current_low + self.current_close) / 3
                self.prev_high = self.current_high
                self.prev_low = self.current_low
            else:
                if self.data.high[0] > self.current_high:
                    self.current_high = self.data.high[0]
                if self.data.low[0] < self.current_low:
                    self.current_low = self.data.low[0]
                self.current_close = self.data.close[0]

            if not self.pivot:
                return

            r1 = (2 * self.pivot) - self.prev_low
            s1 = (2 * self.pivot) - self.prev_high

            self.lines.pivot[0] = self.pivot
            self.lines.r1[0] = r1
            self.lines.s1[0] = s1

            r2 = (self.pivot - s1) + r1
            s2 = (self.pivot - r1) - s1
            self.lines.r2[0] = r2
            self.lines.s2[0] = s2

            r3 = (self.pivot - s2) + r2
            s3 = (self.pivot - r2) - s2
            self.lines.r3[0] = r3
            self.lines.s3[0] = s3

        self.i += 1