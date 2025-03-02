import backtesting
from backtesting import Backtest, Strategy


class BackTrader:
    def __init__(self, data, strategy, commission, plot=False, print=False):
        self.data = data 
        self.train_data = self.data['train_data']
        self.test_data = self.data['test_data']

        self.strategy = strategy 

        self.commission = commission
        self.strategy.order_size = 0.1

        self.trades = dict()

        self.plot = plot
        self.print = print
        # self.grid_search = grid_search

    def execute(self, params, data, plot=False, print=False):
        bt = Backtest(data=data, strategy=self.strategy, commission=self.commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
        stats = bt.run(**params)

        self.trades = stats._trades

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
    
    def cross_val(self, grid, train_size, test_size, step_size, metrics='Equity Final [$]'):
        n = len(self.train_data)

        total = 0
        count = 0

        for start in range(0, n - train_size - test_size + 1, step_size):
            df_train = self.train_data[start : (start + train_size)]
            df_test = self.train_data[(start + train_size) : (start + train_size + test_size)]

            bt = Backtest(data=df_train, strategy=self.strategy, commission=self.commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
            stats, result = bt.optimize(maximize=metrics, method='sambo', max_tries=100, random_state=0, return_heatmap=False, return_optimization=True, **grid)
            params = {'short_duration': result['x'][0], 'long_duration': result['x'][1]}
            print(params) 

            stats = self.execute(params=params, data=df_test)
            score = stats.loc[metrics]
            print(score)

            total += score
            count += 1
        
        return total / count