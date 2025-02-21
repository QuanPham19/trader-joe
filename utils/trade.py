import backtesting
from backtesting import Backtest, Strategy


class BackTrader:
    def __init__(self, data, strategy, commission, exclusive_orders, plot=False, print=False):
        self.data = data 
        self.train_data = self.data['train_data']
        self.test_data = self.data['test_data']

        self.strategy = strategy 
        self.commission = commission
        self.exclusive_orders = exclusive_orders
        self.strategy.order_size = 0.9999
        self.plot = plot
        self.print = print

    def hypothesis(self):
        bt = Backtest(data=self.train_data, strategy=self.strategy, commission=self.commission, exclusive_orders=self.exclusive_orders, trade_on_close=True)
        stats = bt.run()

        if self.print:
            print(f"Sharpe Ratio is {stats.loc['Sharpe Ratio']} compared to criteria of 1.2")
            print(f"Sortino Ratio is {stats.loc['Sortino Ratio']} compared to criteria of 1.2")
            print(f"Win Rate is {stats.loc['Win Rate [%]']} compared to criteria of 50")
            print(f"Max Drawdown is {stats.loc['Max. Drawdown [%]']} compared to criteria of -10")
            print(f"Max Drawdown duration is {stats.loc['Max. Drawdown Duration']} compared to criteria of 30")
            print(f"Kelly criterion is {stats.loc['Kelly Criterion']} use half-Kelly for order size")

        # self.strategy.order_size = stats.loc['Kelly Criterion']/2

        self.train_trades = stats._trades
        if self.plot:
            bt.plot()
        return stats


    def execute(self):
        bt = Backtest(data=self.test_data, strategy=self.strategy, commission=self.commission, exclusive_orders=self.exclusive_orders, trade_on_close=True)
        stats = bt.run()

        self.test_trades = stats._trades
        bt.plot()
        return stats