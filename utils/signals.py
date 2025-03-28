import pandas as pd 
import numpy as np

def Change(data, period: int = 10):
    """
    Calculate the price change over a specific period.
    Returns a NumPy array of the same length as price.
    """
    price = data.Close
    change = np.full(len(price), 0)
    change[period:] = price[period:] - price[:-period]
    return change

def SMA(data, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    arr = data.Close
    return pd.Series(arr).rolling(n).mean()

def EMA(data, n: int) -> pd.Series:
    """
    Returns `n`-period exponential moving average of array `arr`.
    """
    arr = data.Close
    return pd.Series(arr).ewm(span=n, adjust=False).mean()

def MACD(data, short_n: int = 12, long_n: int = 26, signal_n: int = 9):
    """
    Returns MACD line and Signal line.
    MACD Line = EMA(short_n) - EMA(long_n)
    Signal Line = EMA(MACD Line, signal_n)
    """
    arr = data.Close
    short_ema = pd.Series(arr).ewm(span=short_n, adjust=False).mean()
    long_ema = pd.Series(arr).ewm(span=long_n, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = pd.Series(macd_line).ewm(span=signal_n, adjust=False).mean()
    return macd_line, signal_line

def RSI(data, n: int = 14, k: int = 14) -> pd.Series:
    """
    Returns `n`-period Relative Strength Index (RSI) of array `arr`.
    """
    arr = data.Close  # Ensure arr is a Pandas Series
    delta = np.diff(arr, prepend=arr[0])  # Compute differences manually

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(n).mean()
    avg_loss = pd.Series(loss).rolling(n).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    rsi_ma = rsi.rolling(k).mean()

    return rsi / 100, rsi_ma / 100

def BollingerBands(data, n: int = 20, k: float = 2.0) -> pd.DataFrame:
    """
    Returns the Bollinger Bands: upper, lower, and middle (SMA).
    - arr: input data series
    - n: number of periods for the SMA
    - k: number of standard deviations for the bands (default is 2)
    """
    # Calculate the middle band (SMA)
    arr = data.Close
    middle = pd.Series(arr).rolling(n).mean()
    
    # Calculate the rolling standard deviation
    rolling_std = pd.Series(arr).rolling(n).std()
    
    # Calculate the upper and lower bands
    upper = middle + (rolling_std * k)
    lower = middle - (rolling_std * k)
    
    return upper, middle, lower

def previous_low(data, n: int) -> pd.Series:
    """Return previous n period of time low"""
    arr = data.Close
    return pd.Series(arr).rolling(n).min()


def previous_high(data, n: int) -> pd.Series:
    """Return previous n period of time low"""
    arr = data.Close
    return pd.Series(arr).rolling(n).max()

def ATR(data, period: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR) for a given DataFrame of price data.


    Parameters:
        data (pd.DataFrame): DataFrame with columns 'High', 'Low', and 'Close'
        period (int): Number of periods to use for the ATR calculation (default is 14)


    Returns:
        pd.Series: The ATR values computed over the specified period.
    """
    # Convert the columns to pd.Series if they're not already
    high = pd.Series(data['High'])
    low = pd.Series(data['Low'])
    close = pd.Series(data['Close'])
   
    # Calculate the three components of the True Range
    high_low = high - low
    high_close = (high - close.shift(1)).abs()
    low_close = (low - close.shift(1)).abs()


    # True Range is the maximum of these three values
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)


    # ATR is computed as a simple moving average of the True Range over the specified period.
    atr_values = true_range.rolling(window=period, min_periods=period).mean()


    return atr_values

def OBV(data, volume: pd.Series) -> pd.Series:
    # Calculate the price difference
    arr = data.Close
    diff = np.diff(arr, prepend=diff[0])

    # Compute OBV changes: add volume if price increases, subtract if it decreases,
    # and 0 if there's no change
    obv_changes = np.where(diff > 0, volume[1:], np.where(diff < 0, -volume, 0))
    
    # Create a pandas Series with the same index as the price and calculate cumulative sum
    obv = pd.Series(obv_changes, index=arr.index).cumsum()
    
    return obv

def BBW(data, n: int = 10) -> pd.Series:
    """
    Returns Bollinger Band Width (BBW) of array `arr` over `n` periods.
    `k` is the smoothing period for signal generation.
    """
    arr = data.Close
    
    sma = arr.rolling(n).mean()  # Middle Band
    std = arr.rolling(n).std()   # Standard Deviation
    
    upper_band = sma + 2 * std
    lower_band = sma - 2 * std

    bbw = (upper_band - lower_band) / sma  # Normalize by SMA
        
    return bbw