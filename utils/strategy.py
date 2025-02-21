import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy
from .signals import EMA

class EmaCross(Strategy):

    # short_duration = 10  # Default values, can be overridden
    # long_duration = 50

    def __init__(self, short_duration, long_duration):
        self.short_duration = short_duration
        self.long_duration = long_duration

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(EMA, price, self.short_duration)
        self.ma2 = self.I(EMA, price, self.long_duration)

    def next(self):
        if crossover(self.ma1, self.ma2) and not self.position:
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.position.close()

# class SmaCross(Strategy):
#     params = (('short_duration', 5), ('long_duration', 10))

#     def __init__(self):
#         # Initialize your indicators based on the parameters
#         self.ma1 = self.I(EMA, self.data.Close, self.params.short_duration)
#         self.ma2 = self.I(EMA, self.data.Close, self.params.long_duration)

#     def next(self):
#         if crossover(self.ma1, self.ma2):
#             self.buy()
#         elif crossover(self.ma2, self.ma1):
#             self.position.close()