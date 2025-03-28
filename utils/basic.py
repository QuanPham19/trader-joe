from backtesting import Backtest, Strategy
from backtesting.lib import crossover, TrailingStrategy
from .signals import *
import pandas as pd

def get_trailing_price(self):
    self.atr = self.I(ATR, self.data, plot=True)
    self.previous_low = self.I(previous_low, self.data, self.stop_loss_duration)
    self.previous_high = self.I(previous_high, self.data, self.stop_loss_duration)

    return self.atr, self.previous_low, self.previous_high

def update_sl(self):
    long_sl = min(self.previous_low[-1], self.data.Close[-1] - self.atr_multiplier*self.atr[-1])

    for trade in self.trades:
        trade.sl = long_sl
        print('Hello')

class MomentumStrategy(Strategy):
    period = 10               # Lookback period for momentum calculation
    take_profit_ratio = 1.02  # Take profit level (e.g., 2% gain)
    stop_loss_ratio = 0.98    # Stop loss level (e.g., 2% loss)
    id = 0                    # Identifier for tagging trades

    def init(self):
        # Calculate the momentum indicator (price change over 'period')
        self.momentum = self.I(Change, self.data, self.period)

    def next(self):
        # Ensure we have enough data points (first 'period' values will be NaN)
        if np.isnan(self.momentum[-1]) or np.isnan(self.momentum[-2]):
            return

        entry_price = self.data.Close[-1]
        current_change = self.momentum[-1]
        previous_change = self.momentum[-2]

        # No open position: evaluate entry conditions
        if not self.position:
            # Long entry: momentum is positive and increasing
            if current_change > 0 and current_change > previous_change:
                self.buy(
                    size=self.order_size,
                    tp=entry_price * self.take_profit_ratio,
                    sl=entry_price * self.stop_loss_ratio,
                    tag=f'Long {self.id}'
                )
                self.id += 1

        # Optional: exit position if momentum reverses

        if self.position.is_short and (current_change >= previous_change or current_change > 0):
            self.position.close()

class BarUpDnStrategy(Strategy):
    max_intraday_loss = 1  # Max intraday loss percentage
    take_profit_ratio = 1.1
    stop_loss_ratio = 0.95
    stop_loss_duration = 5
    atr_multiplier = 1

    def init(self):
        # self.atr = self.I(ATR, self.data, plot=False)
        # self.previous_low = self.I(previous_low, self.data.Low, self.stop_loss_duration)
        # self.previous_high = self.I(previous_high, self.data.High, self.stop_loss_duration)
        pass
    
    def next(self):
        # self.atr = self.I(ATR, self.data, plot=False)
        entry_price = self.data.Close[-1]
        # long_stop_loss = min(self.previous_low[-1], entry_price - self.atr_multiplier*self.atr[-1])

        # for trade in self.trades:
        #     trade.sl = long_stop_loss
        update_sl(self)

        if self.data.Close[-1] > self.data.Open[-1] and self.data.Open[-1] > self.data.Close[-2]:
            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long')

        # elif self.data.Close[-1] < self.data.Open[-1] and self.data.Open[-1] < self.data.Close[-2]:
        #     self.sell()
        
        # Implement max intraday loss condition
        # for trade in self.trades:
        #     # if trade.pl < -self.max_intraday_loss / 100 * self.equity:
        #     if (self.data.Close[-1] < self.data.Open[-1] and self.data.Open[-1] < self.data.Close[-2]):
        #         trade.close()


class BollingerBandsStrategy(Strategy):
    '''
    Indicators: Bollinger Band
    Idea: Long when current price crossover lower band 
    Filter:
    TP and SL: 10% and 5% and trailing
    Recommendation: 
    '''
    take_profit_ratio = 1.1
    stop_loss_ratio = 0.95
    stop_loss_duration = 5
    atr_multiplier = 1
    
    def init(self):
        self.upper_band = self.I(BollingerBands, self.data, plot=True)[0]
        self.middle_band = self.I(BollingerBands, self.data, plot=False)[1]
        self.lower_band = self.I(BollingerBands, self.data, plot=False)[2]
        self.atr, self.previous_low, self.previous_high = get_trailing_price(self)

    def next(self):
        entry_price = self.data.Close[-1]

        update_sl(self)
        
        # Long entry condition
        if crossover(entry_price, self.lower_band):
            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long')
        # else:
        #     self.position.close()
        