import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy
from .signals import EMA

class EmaCross(Strategy):

    short_duration = 10  # Default values, can be overridden
    long_duration = 50

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(EMA, price, self.short_duration)
        self.ma2 = self.I(EMA, price, self.long_duration)

    def next(self):
        # if crossover(self.ma2, self.ma1) and not self.position:
        #     self.sell(size = self.order_size)

        # elif crossover(self.ma1, self.ma2):
        #     self.position.close()

        # if crossover(self.ma1, self.ma2) and not self.position:
        #     self.buy(size = self.order_size)
        # elif crossover(self.ma2, self.ma1):
        #     self.position.close()

        
        if crossover(self.ma1, self.ma2):
            if self.position.is_short:
                self.position.close()
            
            self.buy(size = self.order_size)

                
        
        elif crossover(self.ma2, self.ma1):
            if self.position.is_long:
                self.position.close()
            
            self.sell(size = self.order_size)
            
                

