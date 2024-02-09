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
    points = 0
    for i in range(len(y_test)):
        if y_pred[i] != 0:
            distence = y_test[i] / y_pred[i]
            distence = 1 - abs(1 - distence) 

            if distence > 0: 
                points += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
        else:
            distence = abs(y_test[i] - y_pred[i]) 
            distence = 1 - distence

            if distence > 0: 
                points += distence 

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5

    points = points / len(y_test)
    print(points)


def printProgressBar(iteration, total, decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}%', end = "\r")
    if iteration == total: 
        print()