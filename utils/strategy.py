import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy
from .signals import EMA

class EmaCross(Strategy):

    short_duration = 10  # Default values, can be overridden
    long_duration = 50

    id = 0
    take_profit_ratio = 1.1
    stop_loss_ratio = 0.9

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(EMA, price, self.short_duration)
        self.ma2 = self.I(EMA, price, self.long_duration)

    def next(self):
        entry_price = self.data.Close[-1]
        # if crossover(self.ma2, self.ma1) and not self.position:
        #     self.sell(size = self.order_size)

        # elif crossover(self.ma1, self.ma2):
        #     self.position.close()
        if crossover(self.ma1, self.ma2):
            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long {self.id}')
            self.id += 1

        # if len(self.trades) < 3:
        #     self.buy()
        # else:
        #     pass
        elif crossover(self.ma2, self.ma1):
            for trade in self.trades:
                if trade.tag ==f'Long {self.id-1}':
                    trade.close()

            
                

