import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Indicators:
    """
    This class is used to calculate the indicators for a given stock.
    """
    def calculate_obv(self, company, start_date, end_date):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df = df.dropna()
        price = df['Adj Close']
        volume = df['Volume']

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

    def calculate_ad_line(self, company, start_date, end_date):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df = df.dropna()
        data = df.copy()
        clv = ((data['Adj Close'] - data['Low']) - (data['High'] - data['Adj Close'])) / (data['High'] - data['Low'])
        ad_values = (clv * data['Volume']).cumsum()

        return ad_values

    def calculate_adx(self, company, start_date, end_date, window):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
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

    def calculate_aroon_oscillator(self, company, start_date, end_date, window):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df = df.dropna()
        data = df.copy()

        high = data['High']
        low = data['Low']

        aroon_up = ((window - high.rolling(window).apply(np.argmax)) / window) * 100
        aroon_down = ((window - low.rolling(window).apply(np.argmin)) / window) * 100

        aroon_oscillator = aroon_up - aroon_down

        return aroon_oscillator

    def calculate_stochastic_oscillator(self, company, start_date, end_date, window):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
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

    def calculate_rsi(self, data, window):
        delta = data.diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        average_gain = up.rolling(window).mean()
        average_loss = abs(down.rolling(window).mean())

        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_macd(self, company, start_date, end_date, short_window, long_window):
        df = pd.read_csv(f"data/data-week/{company}-week.csv")
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df = df.dropna()
        data = df.copy()

        data['Adj Close'] = pd.to_numeric(data['Adj Close'])  # Convert 'Adj Close' column to numeric type

        short_ema = data['Adj Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Adj Close'].ewm(span=long_window, adjust=False).mean()

        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=9, adjust=False).mean()

        return macd_line, signal_line
    
    def get_indicators(self, company, start_date, end_date): 
        """
        company: str - company name
        start_date: str - start date
        end_date: str - end date
        """

        obv = self.calculate_obv(company, start_date, end_date)
        ad_line = self.calculate_ad_line(company, start_date, end_date)
        adx = self.calculate_adx(company, start_date, end_date, 14)
        aroon_oscillator = self.calculate_aroon_oscillator(company, start_date, end_date, 25)
        k, d = self.calculate_stochastic_oscillator(company, start_date, end_date, 14)
        rsi = self.calculate_rsi(pd.read_csv(f"data/data-week/{company}-week.csv")['Adj Close'], 14)
        macd_line, signal_line = self.calculate_macd(company, start_date, end_date, 12, 26)

        obv = obv.fillna(0).tolist()
        ad_line = ad_line.fillna(0).tolist()
        adx = adx.fillna(0).tolist()
        aroon_oscillator = aroon_oscillator.fillna(0).tolist()
        k = k.fillna(0).tolist()
        d = d.fillna(0).tolist()
        rsi = rsi.fillna(0).tolist()
        macd_line = macd_line.fillna(0).tolist()
        signal_line = signal_line.fillna(0).tolist()

        return (obv, ad_line, adx, aroon_oscillator, k, d, rsi, macd_line, signal_line)
    
def test_get_indicators():
    indicators = Indicators()
    start_date = '2020-01-01'
    end_date = '2021-12-31'
    company = 'tesla'
    
    obv, ad_line, adx, aroon_oscillator, k, d, rsi, macd_line, signal_line = indicators.get_indicators(company, start_date, end_date)
    
    # Plotting the indicators
    plt.figure(figsize=(15,10))

    plt.subplot(3,3,1)
    plt.plot(obv)
    plt.title('OBV')

    plt.subplot(3,3,2)
    plt.plot(ad_line)
    plt.title('AD Line')

    plt.subplot(3,3,3)
    plt.plot(adx)
    plt.title('ADX')

    plt.subplot(3,3,4)
    plt.plot(aroon_oscillator)
    plt.title('Aroon Oscillator')

    plt.subplot(3,3,5)
    plt.plot(k)
    plt.title('Stochastic Oscillator K')

    plt.subplot(3,3,6)
    plt.plot(d)
    plt.title('Stochastic Oscillator D')

    plt.subplot(3,3,7)
    plt.plot(rsi)
    plt.title('RSI')

    plt.subplot(3,3,8)
    plt.plot(macd_line)
    plt.title('MACD Line')

    plt.subplot(3,3,9)
    plt.plot(signal_line)
    plt.title('Signal Line')

    plt.tight_layout()
    plt.show()

# test_get_indicators()