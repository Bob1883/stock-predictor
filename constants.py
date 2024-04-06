from scipy.stats.mstats import winsorize
from alpaca_trade_api.rest import REST
from matplotlib import pyplot as plt
from tensorflow import keras
import statsmodels.api as sm
from typing import Tuple 
import pandas as pd
import numpy as np
import datetime
import time
import json
import os

import tensorflow as tf

from keras.models import Model, load_model
from keras.layers import Input, LSTM, concatenate, Dense, GRU, Dropout, Concatenate
from keras import layers
from keras_tuner import RandomSearch, Objective
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from kerastuner import HyperParameters

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# from lumibot.brokers import Alpaca
# from lumibot.backtesting import YahooDataBacktesting
# from lumibot.strategies.strategy import Strategy
# from lumibot.traders import Trader

# mute warnings
tf.get_logger().setLevel('INFO')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# use GPU
if tf.test.gpu_device_name(): 
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

############
# SETTINGS #
############
n_past = 20    # Number of past days we want to use to predict the future.
n_future = 3   # Number of days we want to predict into the future.

max_trials = 10
executions_per_trial = 3

use_freq = True

periode = 3  # years -> float
epochs = 250

data = {}
companies = []
indicators = []
test_stock = "apple" 

scaler = MinMaxScaler() 

####### 
# API #
#######  
# API_KEY = str(os.getenv("ALPACA_KEY"))
# API_SECRET = str(os.getenv("ALPACA_SECRET"))

# BASE_URL = "https://paper-api.alpaca.markets"

# ALPACA_CREDS = {
#     "API_KEY":API_KEY, 
#     "API_SECRET": API_SECRET, 
#     "PAPER": True
# }

# api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

##############
# INDICATORS #
##############
def calculate_rsi(prices, window=14):
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.convolve(gain, np.ones(window) / window, mode='valid')
    avg_loss = np.convolve(loss, np.ones(window) / window, mode='valid')
    avg_loss = np.where(avg_loss == 0, 1e-10, avg_loss)
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = pd.Series(prices).ewm(span=fast).mean().values
    ema_slow = pd.Series(prices).ewm(span=slow).mean().values
    macd = ema_fast - ema_slow
    signal_line = pd.Series(macd).ewm(span=signal).mean().values
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_ema(prices, window):
    return pd.Series(prices).ewm(span=window).mean().values

def calculate_bollinger_bands(prices, window=20, num_std=2):
    rolling_mean = pd.Series(prices).rolling(window=window).mean()
    rolling_std = pd.Series(prices).rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band.values, lower_band.values

def calculate_obv(prices, volume):
    obv = np.where(np.diff(prices) > 0, volume[1:], np.where(np.diff(prices) < 0, -volume[1:], 0)).cumsum()
    return np.concatenate(([0], obv))

###############
# FOR LOOGING #
###############
def printProgressBar(iteration, total, decimals = 1, length = 100, fill = '█', description = 'Progress: '):
    time.sleep(0.1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(description)
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\rProgress: |{bar}| {percent}%', end = "\r")
    if iteration == total: 
        print()

def clac_accuracy(y_test, y_pred):
    points = 0
    same_side = 0
    tot_dist = 0
    for i in range(len(y_test)):
        if y_pred[i] != 0:
            distence = y_test[i] / y_pred[i]
            distence = 1 - abs(1 - distence) 

            if distence > 0: 
                points += distence
                tot_dist += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
                same_side += 1
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
                same_side += 1
        else:
            distence = abs(y_test[i] - y_pred[i]) 
            distence = 1 - distence

            if distence > 0: 
                points += distence 
                tot_dist += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
                same_side += 1
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
                same_side += 1

    print("Same side: ", same_side/len(y_test))
    print("Total dist: ", (tot_dist/len(y_test))[0]*100, "%")
    points = points / len(y_test)
    print("Points: ", points[0]*100, "%")
    return points

# def custom_metric(y_true, y_pred):
#     points = 0

#     for i in range(len(y_true)):
#         if y_pred[i] != 0:
#             distence = y_true[i] / y_pred[i]
#             distence = 1 - abs(1 - distence) 

#             if distence > 0: 
#                 points += distence

#             if y_true[i] < 0 and y_pred[i] < 0:
#                 points += 0.5
            
#             if y_true[i] > 0 and y_pred[i] > 0:
#                 points += 0.5

#         else:
#             distence = abs(y_true[i] - y_pred[i]) 
#             distence = 1 - distence

#             if distence > 0: 
#                 points += distence 

#             if y_true[i] < 0 and y_pred[i] < 0:
#                 points += 0.5

#             if y_true[i] > 0 and y_pred[i] > 0:
#                 points += 0.5

#     points = points / len(y_true)
#     return tf.reduce_mean(points)

rounds = 0
class CustomCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        global rounds
        if epoch % epochs == 0 or epoch == 0:
            rounds += 1
            printProgressBar(rounds, max_trials*executions_per_trial, length=50, description="Training model...")

        if epoch % epochs-1 == 0:
            print("\n")
            print("Loss: ", logs['loss'])