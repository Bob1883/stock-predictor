import pandas as pd
import numpy as np

def calculate_obv(price, volume):
    changes = price.diff()

    obv_values = [0]
    for change, volume in zip(changes[1:], volume[1:]):
        if change > 0:
            obv_values.append(obv_values[-1] + volume)
        elif change < 0:
            obv_values.append(obv_values[-1] - volume)
        else:
            obv_values.append(obv_values[-1])

    return pd.Series(obv_values, index=price.index)

def calculate_ad_line(company):
    df = pd.read_csv(f"data/data-week/{company}-week.csv")
    df = df.dropna()
    data = df.copy()
    clv = ((data['Adj Close'] - data['Low']) - (data['High'] - data['Adj Close'])) / (data['High'] - data['Low'])
    ad_values = (clv * data['Volume']).cumsum()

    return ad_values

def calculate_adx(company, window):
    df = pd.read_csv(f"data/data-week/{company}-week.csv")
    df = df.dropna()
    data = df.copy()

    high = data['High']
    low = data['Low']
    close = data['Adj Close']

    up_move = high.diff()
    down_move = low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    tr = high.combine(close.shift(), max) - low.combine(close.shift(), min)

    plus_di = 100 * pd.Series(plus_dm).rolling(window).sum() / pd.Series(tr).rolling(window).sum()
    minus_di = 100 * pd.Series(minus_dm).rolling(window).sum() / pd.Series(tr).rolling(window).sum()

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window).mean()

    return adx

def calculate_aroon_oscillator(company, window):
    df = pd.read_csv(f"data/data-week/{company}-week.csv")
    df = df.dropna()
    data = df.copy()

    high = data['High']
    low = data['Low']

    aroon_up = ((window - high.rolling(window).apply(np.argmax)) / window) * 100
    aroon_down = ((window - low.rolling(window).apply(np.argmin)) / window) * 100

    aroon_oscillator = aroon_up - aroon_down

    return aroon_oscillator

def calculate_stochastic_oscillator(company, window):
    df = pd.read_csv(f"data/data-week/{company}-week.csv")
    df = df.dropna()
    data = df.copy()

    high = data['High']
    low = data['Low']
    close = data['Adj Close']

    highest_high = high.rolling(window).max()
    lowest_low = low.rolling(window).min()

    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(3).mean()

    return k, d

def calculate_rsi(data, window):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    average_gain = up.rolling(window).mean()
    average_loss = abs(down.rolling(window).mean())

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_macd(data, short_window, long_window):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    return macd_line, signal_line
