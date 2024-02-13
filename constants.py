from typing import Tuple 
from alpaca_trade_api.rest import REST
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import json
import time
import datetime

import tensorflow as tf
from tensorflow import keras

from keras.models import Model
from keras.layers import Input, LSTM, concatenate, Dense
from keras import layers
from keras_tuner import RandomSearch

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader



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

periode = 259 # weeks, so 5 years 

data = {}
companies = []
indicators = []
test_stock = "Tesla" 

scaler = MinMaxScaler() 

####### 
# API #
#######  
API_KEY = str(os.getenv("ALPACA_KEY"))
API_SECRET = str(os.getenv("ALPACA_SECRET"))

BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

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
    return points

rounds = 0
class CustomCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        global rounds
        if epoch % 50 == 0:
            rounds += 1
        printProgressBar(rounds, max_trials*executions_per_trial, length=50, description="Training model...")
