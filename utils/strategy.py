import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy
from .signals import *

class EmaCross(Strategy):

    short_duration = 10  # Default values, can be overridden
    long_duration = 50

    id = 0
    take_profit_ratio = 1.02
    stop_loss_ratio = 0.95

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


class Modified_EMACross(Strategy):
    #Is used for trending market
    #Use trailing stop loss based on ATR indicator
   
    short_duration = 5 # Default values, can be overridden
    long_duration = 10
    stop_loss_duration = 5
    take_profit_ratio = 0.3
    atr_multiplier = 1
    
   
    def init(self):
        df_data = self.data
       
        self.ema_short_duration = self.I(EMA, df_data.Close, self.short_duration)
        self.ema_long_duration = self.I(EMA, df_data.Close, self.long_duration)
        self.atr = self.I(ATR, df_data)
        self.previous_low = self.I(previous_low, df_data.Low, self.stop_loss_duration)
        self.previous_high = self.I(previous_high, df_data.High, self.stop_loss_duration)
   
    def next(self):
        self.stop_loss_duration = min(self.stop_loss_duration, len(self.data.Low), len(self.data.High))
        current_price = self.data.Close[-1]
        #stop loss using data  
        long_stop_loss = min(self.previous_low[-1], current_price - self.atr_multiplier*self.atr[-1])
        short_stop_loss = max(self.previous_high[-1], current_price + self.atr_multiplier*self.atr[-1])
       
        # long_stop_loss = current_price - self.atr[-1]
        # short_stop_loss = current_price + self.atr[-1]
       
        #update stop loss for previous trades
        for trade in self.trades:
            if trade.tag == "Long":
                trade.sl = long_stop_loss
            elif trade.tag == "Short":
                trade.sl = short_stop_loss
       
        if crossover(self.ema_short_duration, self.ema_long_duration):
            #close all short trade:
            for trade in self.trades:
                if trade.tag == "Short":
                    trade.close()


            self.buy(size = self.order_size, sl = long_stop_loss, tp = current_price*(1+self.take_profit_ratio), tag = "Long")
           
        if crossover(self.ema_long_duration, self.ema_short_duration):
            #close all long trade:
            for trade in self.trades:
                if trade.tag == "Long":
                    trade.close()
           
            self.sell(size = self.order_size, sl = short_stop_loss, tp = current_price*(1-self.take_profit_ratio), tag = "Short")

class MacdCross(Strategy):

    id = 0
    take_profit_ratio = 1.02
    stop_loss_ratio = 0.95

    def init(self):
        price = self.data.Close
        self.macd_line = self.I(MACD, price)[0]
        self.signal_line = self.I(MACD, price)[1]

    def next(self):
        entry_price = self.data.Close[-1]

        if crossover(self.macd_line, self.signal_line):
            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long {self.id}')
            self.id += 1

        elif crossover(self.signal_line, self.macd_line):
            for trade in self.trades:
                if trade.tag ==f'Long {self.id-1}':
                    trade.close()

class BollingerCross(Strategy):

    id = 0
    take_profit_ratio = 1.02
    stop_loss_ratio = 0.95

    def init(self):
        price = self.data.Close
        self.upper_band = self.I(BollingerBands, price)[0]
        self.middle_band = self.I(BollingerBands, price)[1]
        self.lower_band = self.I(BollingerBands, price)[2]

    def next(self):
        entry_price = self.data.Close[-1]
        if crossover(self.data.Close, self.middle_band):
            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long {self.id}')
            self.id += 1

        elif crossover(self.middle_band, self.data.Close):
            for trade in self.trades:
                if trade.tag ==f'Long {self.id-1}':
                    trade.close()

class BollingerBound(Strategy):

    id = 0
    take_profit_ratio = 1.02
    stop_loss_ratio = 0.95

    def init(self):
        price = self.data.Close
        self.upper_band = self.I(BollingerBands, price)[0]
        self.middle_band = self.I(BollingerBands, price)[1]
        self.lower_band = self.I(BollingerBands, price)[2]

    def next(self):
        entry_price = self.data.Close[-1]
        # if crossover(self.lower_band, self.data.Close):
        #     self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag=f'Long {self.id}')
        #     self.id += 1

        # elif crossover(self.data.Close, self.upper_band):
        #     for trade in self.trades:
        #         if trade.tag ==f'Long {self.id-1}':
        #             trade.close()

        if crossover(self.lower_band, self.data.Close):
            #close all short trade:
            for trade in self.trades:
                if trade.tag == "Short":
                    trade.close()


            self.buy(size = self.order_size, tp=entry_price*self.take_profit_ratio, sl=entry_price*self.stop_loss_ratio, tag = "Long")
           
        if crossover(self.data.Close, self.upper_band):
            #close all long trade:
            for trade in self.trades:
                if trade.tag == "Long":
                    trade.close()
           
            self.sell(size = self.order_size, tp=entry_price*self.stop_loss_ratio, sl=entry_price*self.take_profit_ratio, tag = "Short")

class testRSI(Strategy):
    short_duration = 5 # Default values, can be overridden
    long_duration = 10
    stop_loss_duration = 5
    take_profit_ratio = 0.3
    atr_multiplier = 1
    
   
    def init(self):
        df_data = self.data
       
        self.ema_short_duration = self.I(EMA, df_data.Close, self.short_duration)
        self.ema_long_duration = self.I(EMA, df_data.Close, self.long_duration)
        self.atr = self.I(ATR, df_data)
        self.previous_low = self.I(previous_low, df_data.Low, self.stop_loss_duration)
        self.previous_high = self.I(previous_high, df_data.High, self.stop_loss_duration)
        self.RSI = self.I(RSI, df_data.Close)
   
    def next(self):
        self.stop_loss_duration = min(self.stop_loss_duration, len(self.data.Low), len(self.data.High))
        current_price = self.data.Close[-1]
        #stop loss using data  
        long_stop_loss = min(self.previous_low[-1], current_price - self.atr_multiplier*self.atr[-1])
        short_stop_loss = max(self.previous_high[-1], current_price + self.atr_multiplier*self.atr[-1])
       
        # long_stop_loss = current_price - self.atr[-1]
        # short_stop_loss = current_price + self.atr[-1]
       
        #update stop loss for previous trades
        for trade in self.trades:
            if trade.tag == "Long":
                trade.sl = long_stop_loss
            elif trade.tag == "Short":
                trade.sl = short_stop_loss
       
        if crossover(self.ema_short_duration, self.ema_long_duration) and self.RSI[-1] >= 30:
            #close all short trade:
            for trade in self.trades:
                if trade.tag == "Short":
                    trade.close()

        # if crossover(self.ema_short_duration, self.ema_long_duration) and :

            self.buy(size = self.order_size, sl = long_stop_loss, tp = current_price*(1+self.take_profit_ratio), tag = "Long")
           
        if crossover(self.ema_long_duration, self.ema_short_duration) and self.RSI[-1] <= 70:
            #close all long trade:
            for trade in self.trades:
                if trade.tag == "Long":
                    trade.close()
           
            self.sell(size = self.order_size, sl = short_stop_loss, tp = current_price*(1-self.take_profit_ratio), tag = "Short")

