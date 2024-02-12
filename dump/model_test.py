import pandas as pd
from keras.models import load_model
from components.load_data import Load_data
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm
from scipy.stats.mstats import winsorize
from components.load_data_for_test import Load_data
import time
import os
import numpy as np
import matplotlib.pyplot as plt

# Load the model
model = load_model("models/model_1.h5")
money_data = []
money = 2000 # the amount of money you have to invest
stocks = {} # the stocks you have

def calculate_obv(company):
    df = pd.read_csv(f"data/data-week/{company}-week.csv")
    df = df.dropna()
    data = df.copy()
    volumes = data['Volume']
    changes = data['Adj Close'].diff()

    obv_values = [0]
    for change, volume in zip(changes[1:], volumes[1:]):
        if change > 0:
            obv_values.append(obv_values[-1] + volume)
        elif change < 0:
            obv_values.append(obv_values[-1] - volume)
        else:
            obv_values.append(obv_values[-1])

    return pd.Series(obv_values, index=data.index)

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

# def is_good_trade(data, date):
#     # Check if RSI is less than 70 (not overbought)
#     if data['RSI'][date] > 100:
#         return False

#     # Check if MACD line is above the Signal line or has recently crossed above it
#     if data['MACD Line'][date] < data['Signal Line'][date] and data['MACD Line'][date - 1] < data['Signal Line'][date - 1]:
#         return False

#     return True

def pick_stocks(predictions, date, raw_data, all_predictions):
    global money
    global stocks
    global money_data

    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_predictions[:5]
    money_to_spend = money / 2 # the amount of money that i can spend 

    top_5 = dict(top_5)
    new_stock = {}

    promesing_companies = []

    # sell all companies
    for company in stocks:
        money += stocks[company] * raw_data[company]['Adj Close'][date]

    stocks = {}


    # get all the companies that had gone down in price, but know the AI predicts that it will go up and last prediction was negative
    for company in predictions:
        if predictions[company] > 1 and raw_data[company]['Adj Close'][date] < raw_data[company]['Adj Close'][date - 1] and all_predictions[company][date - 1][0] < 0:
            promesing_companies.append(company)

    # buy companies that are promesing
    for company in promesing_companies:
        # calculate RSI and MACD
        raw_data[company]['RSI'] = calculate_rsi(raw_data[company]['Adj Close'], 14)
        raw_data[company]['MACD Line'], raw_data[company]['Signal Line'] = calculate_macd(raw_data[company]['Adj Close'], 12, 26)
        stochastic_oscillator = calculate_stochastic_oscillator(company, 14)
        adx = calculate_adx(company, 14)
        aroon_oscillator = calculate_aroon_oscillator(company, 14)
        # ad_line = calculate_ad_line(company)
        # obv = calculate_obv(company)

        # print(company, "stats: ")
        # print("RSI: ", raw_data[company]['RSI'][date])
        # print("MACD: ", raw_data[company]['MACD Line'][date])
        # print("Signal: ", raw_data[company]['Signal Line'][date])
        # print("Stochastic Oscillator: ", stochastic_oscillator[0][date])
        # print("ADX: ", adx[date])
        # print("Aroon Oscillator: ", aroon_oscillator[date])
        # # print("AD Line: ", ad_line[date])
        # # print("OBV: ", obv[date])
        # print("AI prediction: ", predictions[company])

        # check if it's a good trade
        if company in top_5:
            money -= raw_data[company]['Adj Close'][date] * 1
            if company in stocks:
                stocks[company] += 1
            else:
                stocks[company] = 1

    # # sell companies that are not in the top 5
    # for company in stocks:
    #     if company not in top_5:
    #         money += stocks[company] * raw_data[company]['Adj Close'][date]
    #     else:
    #         new_stock[company] = top_5[company]

    # stocks = new_stock

    # # calculate total prediction score of top 5 companies
    # total_prediction_score = sum(top_5.values())

    # # invest in the top 5 companies, if have money to invest. 
    # for company in top_5:
    #     if top_5[company] > 0.5:
    #         # calculate proportion of money to invest in this company
    #         proportion_to_invest = top_5[company] / total_prediction_score

    #         # calculate how much money to invest in this company
    #         money_to_invest = money_to_spend * proportion_to_invest

    #         # calculate how many stocks to buy, of the company
    #         company_to_buy = int(money_to_invest / raw_data[company]['Adj Close'][date])

    #         # calculate RSI and MACD
    #         raw_data[company]['RSI'] = calculate_rsi(raw_data[company]['Adj Close'], 14)
    #         raw_data[company]['MACD Line'], raw_data[company]['Signal Line'] = calculate_macd(raw_data[company]['Adj Close'], 12, 26)
    #         stochastic_oscillator = calculate_stochastic_oscillator(company, 14)
    #         adx = calculate_adx(company, 14)
    #         aroon_oscillator = calculate_aroon_oscillator(company, 14)
    #         # ad_line = calculate_ad_line(company)
    #         # obv = calculate_obv(company)

    #         print(company, "stats: ")
    #         print("RSI: ", raw_data[company]['RSI'][date])
    #         print("MACD: ", raw_data[company]['MACD Line'][date])
    #         print("Signal: ", raw_data[company]['Signal Line'][date])
    #         print("Stochastic Oscillator: ", stochastic_oscillator[0][date])
    #         print("ADX: ", adx[date])
    #         print("Aroon Oscillator: ", aroon_oscillator[date])
    #         # print("AD Line: ", ad_line[date])
    #         # print("OBV: ", obv[date])
    #         print("AI prediction: ", top_5[company])

    #         # check if it's a good trade
    #         if raw_data[company]['Adj Close'][date] * company_to_buy <= money and raw_data[company]['RSI'][date] < 70 and raw_data[company]['MACD Line'][date] > raw_data[company]['Signal Line'][date] and stochastic_oscillator[0][date] > stochastic_oscillator[1][date] and adx[date] > 25 and aroon_oscillator[date] > 0:
    #             money -= raw_data[company]['Adj Close'][date] * company_to_buy
    #             if company in stocks:
    #                 stocks[company] += company_to_buy
    #             else:
    #                 stocks[company] = company_to_buy
            
    # put the money we have in hand and the money we have invested in the stocks together, and add it to the money_data array
    money_data.append(money + sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))
    print("money in stocks: ", sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))
    print("money in hand: ", money)
    print("total money: ", money + sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))

# get the company names that are both in data/data-week and data/data-google-trends and data/data-political
companies = []
for filename in os.listdir("data/data-week"):
    company_name = filename.split("-")[0]
    if os.path.isfile(f"data/data-google-trends/{company_name}-trend.json") and os.path.isfile(f"data/data-political/{company_name}-political.json"):
        companies.append(company_name)

# get the data for the companies
data = {}
raw_data = {}
for company in companies:
    loader = Load_data(period=259, company=company.lower())
    data[company] = loader.get_all_data()
    raw_data[company] = loader.get_raw_data()

plt.figure()  # Create a new figure

# predict from 2021-01-01 to now. 
number_of_weeks = 52*5 - 20 
predictions = {}
n_future = 1   # Number of weeks we want to look into the future based on the past weeks.
n_past = 10  # Number of past weeks we want to use to predict the future.

for company in data:
    company_data = None
    # get the data for the company
    company_data = data[company]

    prediction_data = []
    
    for i in range(n_past, len(company_data) - n_future +1):
        prediction_data.append(company_data[i - n_past:i, 0:company_data.shape[1]])

    prediction_data = np.array(prediction_data)

    # predict the stock price
    prediction = model.predict(prediction_data)

    predictions[company] = prediction.tolist()

for i in range(number_of_weeks):
    # date is = to the the number of weeks the data contains 
    date = len(data[company]) - (number_of_weeks - i)

    weeks_predictions = {}
    # get the predictions for the week
    for company in predictions:
        weeks_predictions[company] = predictions[company][date - n_past][0]

    pick_stocks(weeks_predictions, date, raw_data, predictions)

    plt.plot(money_data)
    plt.legend(["Money"])
    # change color to red
    plt.gca().lines[0].set_color("red")
    plt.draw()  # Draw the current figure
    plt.pause(0.01)  # Pause for a short period

plt.show()  # Show the final figure