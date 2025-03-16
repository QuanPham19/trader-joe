import pandas as pd
import numpy as np 

import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy

class DataLoader:
    def __init__(self, ticker, start, end, freq, test_size):
        self.ticker = ticker
        self.start = start 
        self.end = end
        self.freq = freq 
        self.test_size = test_size
        self.data = dict()
        
    def get_price_data(self):
        df = yf.download(
            self.ticker, 
            start=self.start, 
            end=self.end, 
            multi_level_index=False, 
            interval=self.freq,
            )
        df['Color'] = (df['Close'] > df['Open']) 
        self.data['price_data'] = df
        return df
    
    def get_option_data(self):

        tk = yf.Ticker(self.ticker)

        exps = tk.options 
        selected_exps = exps[0]

        option_chain = tk.option_chain(selected_exps)

        calls, puts = option_chain.calls, option_chain.puts 

        self.data['calls_data'] = calls 
        self.data['puts_data'] = puts

        return calls, puts
    
    def split(self, key):
        df = self.data[key].copy()
        split_idx = int(len(df) * (1-self.test_size))
        self.data['train_data'] = df.iloc[:split_idx]
        self.data['test_data'] = df.iloc[split_idx:]

    def plot_candlestick(self, data):
        class EmptyStrategy(SignalStrategy):
            def init(self):
                pass
            def next(self):
                pass

        bt = Backtest(data, EmptyStrategy, cash=10_000, commission=0.0)
        stats = bt.run()
        bt.plot()
    
    def run(self):
        self.get_price_data()
        self.split(key='price_data')
        self.plot_candlestick(self.data['test_data'])        