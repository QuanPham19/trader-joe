import backtesting
from backtesting import Backtest, Strategy


class BackTrader:
    def __init__(self, data, strategy, commission, exclusive_orders):
        self.data = data 
        self.strategy = strategy 
        self.commission = commission
        self.exclusive_orders = exclusive_orders

    def execute(self):
        bt = Backtest(data=self.data, strategy=self.strategy, commission=self.commission, exclusive_orders=self.exclusive_orders)
        stats = bt.run()

        self.trades = stats._trades
        bt.plot()
        return stats