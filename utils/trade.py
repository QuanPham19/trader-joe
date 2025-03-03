import backtesting
from backtesting import Backtest, Strategy


class BackTrader:
    def __init__(self, data):
        self.data = data 
        self.train_data = self.data['train_data']
        self.test_data = self.data['test_data']

        self.trades = dict()

    def evaluate(self, data, strategy, params, order_size=0.1, commission=0.002, plot=False, print=False):
        strategy.order_size = order_size

        bt = Backtest(data=data, strategy=strategy, commission=commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
        stats = bt.run(**params)

        self.trades = stats._trades

        if print:
            print(f"Sharpe Ratio is {stats.loc['Sharpe Ratio']} compared to criteria of 1.2")
            print(f"Sortino Ratio is {stats.loc['Sortino Ratio']} compared to criteria of 1.2")
            print(f"Win Rate is {stats.loc['Win Rate [%]']} compared to criteria of 50")
            print(f"Max Drawdown is {stats.loc['Max. Drawdown [%]']} compared to criteria of -10")
            print(f"Max Drawdown duration is {stats.loc['Max. Drawdown Duration']} compared to criteria of 30")
            print(f"Kelly criterion is {stats.loc['Kelly Criterion']} use half-Kelly for order size")
        
        if plot:
            bt.plot()

        return stats
    
    def cross_val(self, strategy, grid, train_size, test_size, step_size, order_size=0.1, commission=0.002, metrics='Equity Final [$]'):
        n = len(self.train_data)
        strategy.order_size = order_size

        total = 0
        count = 0

        for start in range(0, n - train_size - test_size + 1, step_size):
            df_train = self.train_data[start : (start + train_size)]
            df_test = self.train_data[(start + train_size) : (start + train_size + test_size)]

            bt = Backtest(data=df_train, strategy=strategy, commission=commission, finalize_trades=True, exclusive_orders=False, trade_on_close=True)
            stats, result = bt.optimize(maximize=metrics, method='sambo', max_tries=100, random_state=0, return_heatmap=False, return_optimization=True, **grid)

            # To be upgraded
            # params = {'short_duration': result['x'][0], 'long_duration': result['x'][1]}
            best_params = {key: result.x[i] for i, key in enumerate(grid.keys())}
            print(best_params) 

            stats = self.evaluate(data=df_test, strategy=strategy, params=best_params, order_size=order_size, commission=commission)
            score = stats.loc[metrics]
            print(score)

            total += score
            count += 1
        
        return total / count