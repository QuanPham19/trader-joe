import pandas as pd 
import numpy as np

def SMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    return pd.Series(arr).rolling(n).mean()

def EMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period exponential moving average of array `arr`.
    """
    return pd.Series(arr).ewm(span=n, adjust=False).mean()

def MACD(arr: pd.Series, short_n: int = 12, long_n: int = 26, signal_n: int = 9):
    """
    Returns MACD line and Signal line.
    MACD Line = EMA(short_n) - EMA(long_n)
    Signal Line = EMA(MACD Line, signal_n)
    """
    short_ema = EMA(arr, short_n)
    long_ema = EMA(arr, long_n)
    macd_line = short_ema - long_ema
    signal_line = EMA(macd_line, signal_n)
    return macd_line, signal_line

def RSI(arr, n: int = 14) -> pd.Series:
    """
    Returns `n`-period Relative Strength Index (RSI) of array `arr`.
    """
    arr = pd.Series(arr)  # Ensure arr is a Pandas Series
    delta = np.diff(arr, prepend=arr[0])  # Compute differences manually

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(n).mean()
    avg_loss = pd.Series(loss).rolling(n).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def BollingerBands(arr: pd.Series, n: int = 20, k: float = 2.0) -> pd.DataFrame:
    """
    Returns the Bollinger Bands: upper, lower, and middle (SMA).
    - arr: input data series
    - n: number of periods for the SMA
    - k: number of standard deviations for the bands (default is 2)
    """
    # Calculate the middle band (SMA)
    middle = SMA(arr, n)
    
    # Calculate the rolling standard deviation
    rolling_std = pd.Series(arr).rolling(n).std()
    
    # Calculate the upper and lower bands
    upper = middle + (rolling_std * k)
    lower = middle - (rolling_std * k)
    
    return upper, middle, lower

def previous_low(arr: pd.Series, n: int) -> pd.Series:
    """Return previous n period of time low"""
    return pd.Series(arr).rolling(n).min()


def previous_high(arr: pd.Series, n: int) -> pd.Series:
    """Return previous n period of time low"""
    return pd.Series(arr).rolling(n).max()

def ATR(data: pd.DataFrame, period: int = 14) -> pd.Series:
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
