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