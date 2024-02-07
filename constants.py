from typing import Tuple 
from alpaca_trade_api.rest import REST
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import json
import time

from sklearn.preprocessing import MinMaxScaler

API_KEY = "PK9618UB7TK7LDWHY5SE" 
API_SECRET = "OaXaMZnLfur2mKLII3K3ktKbaoO3RG2zPfTI1Xco" 
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

def clac_accuracy(y_test, y_pred):
    # get the tops and see how far appart they are. If they both are negative or positive, then give it extra points
    points = 0
    for i in range(len(y_test)):
        # see how far apart they are
        if y_pred[i] != 0:
            distence = y_test[i] / y_pred[i]

            # the closer it is to 1, the more points it gets
            distence = 1 - abs(1 - distence) 

            if distence > 0: 
                points += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
        else:
            distence = abs(y_test[i] - y_pred[i]) 
            # the closer it is to 0, the more points it gets
            distence = 1 - distence

            if distence > 0: 
                points += distence 

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5

    points = points / len(y_test)

    print(points)

def find_best_commodity(companies): 
    commodity_data = {}
    best_commodies = {}

    for commodity in os.listdir("data/commodity"):
        # open json file
        with open(f"data/commodity/{commodity}") as f:
            data = json.load(f)

        commodity_data[commodity] = []

        for i in range(len(data["series"][0]["data"])): 
            commodity_data[commodity].append(data["series"][0]["data"][i]["y"])

    for company in companies:
        df = pd.read_csv(f"data/data-day/{company}.csv")
        df = df.dropna()
        data = df.copy()

        prices = data['Adj Close'].values   

        prices = [np.mean(prices[i:i+30]) for i in range(0, len(prices), 30)]

        best_commodies[company] = {}
        diffs = {}

        for commodity in commodity_data:    
            for commodity in commodity_data:
                commodity_prices = commodity_data[commodity]

                # make sure the price data is the same length
                if len(prices) > len(commodity_prices):
                    prices = prices[:len(commodity_prices)]
                else:
                    commodity_prices = commodity_prices[:len(prices)]

                # scale the prices
                scaler = MinMaxScaler()
                prices_scaled = scaler.fit_transform(np.array(prices).reshape(-1, 1)).flatten()
                commodity_prices_scaled = scaler.transform(np.array(commodity_prices).reshape(-1, 1)).flatten()

                # scale the prices
                scaler = MinMaxScaler()
                prices_scaled = scaler.fit_transform(np.array(prices).reshape(-1, 1)).flatten()
                commodity_prices_scaled = scaler.transform(np.array(commodity_prices).reshape(-1, 1)).flatten()

                # calculate the diff
                diff = 0
                for i in range(len(prices_scaled)):
                    diff += abs(prices_scaled[i] - commodity_prices_scaled[i])

                diffs[commodity] = diff
            
        best_commodies[company] = sorted(diffs, key=diffs.get)[:3]

        print(best_commodies)   
        for commodity in range(len(best_commodies[company])):
            best_commodies[company][commodity] = commodity_data[best_commodies[company][commodity]]

    return best_commodies


def printProgressBar(iteration, total, decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '―' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}%', end = "\r")
    if iteration == total: 
        print()