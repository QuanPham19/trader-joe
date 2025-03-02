import backtesting
from backtesting import Backtest, Strategy


class BackTrader:
    def __init__(self, data, strategy, commission, params, grid_search, plot=False, print=False):
        self.data = data 
        self.train_data = self.data['train_data']
        self.test_data = self.data['test_data']

        self.strategy = strategy 
        self.params = params 

        self.commission = commission
        self.strategy.order_size = 0.1

        self.trades = dict()

        self.plot = plot
        self.print = print
        self.grid_search = grid_search

    def execute(self, mode='train', plot=False, print=False):
        if mode == 'test':
            plot = True
            data = self.test_data
        elif mode == 'train':
            plot = False 
            data = self.train_data 

        bt = Backtest(data=data, strategy=self.strategy, commission=self.commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
        stats = bt.run(**self.params)

        self.trades[mode] = stats._trades

        if self.print:
            print(f"Sharpe Ratio is {stats.loc['Sharpe Ratio']} compared to criteria of 1.2")
            print(f"Sortino Ratio is {stats.loc['Sortino Ratio']} compared to criteria of 1.2")
            print(f"Win Rate is {stats.loc['Win Rate [%]']} compared to criteria of 50")
            print(f"Max Drawdown is {stats.loc['Max. Drawdown [%]']} compared to criteria of -10")
            print(f"Max Drawdown duration is {stats.loc['Max. Drawdown Duration']} compared to criteria of 30")
            print(f"Kelly criterion is {stats.loc['Kelly Criterion']} use half-Kelly for order size")
        
        if plot:
            bt.plot()

        return stats
    
    def optimize(self):
        bt = Backtest(data=self.train_data, strategy=self.strategy, commission=self.commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
        stats, heatmap, result = bt.optimize(
            maximize='Equity Final [$]',
            method='sambo',
            max_tries=100,
            random_state=0,
            return_heatmap=True,
            return_optimization=True,
            **self.grid_search)
        
        return stats, heatmap, result