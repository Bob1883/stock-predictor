from keras.models import Model
from keras.layers import Input, LSTM, concatenate, Dense
import tensorflow as tf
from tensorflow import keras
from keras import layers
from kerastuner.tuners import RandomSearch

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import pandas as pd
import os
import time

from constants import *
from load_data import Load_data

# TODO
# 1.x                                             Load in day data and use it when training, 20 days back
# 2.x                               rewrite change, becuse now the price data is of, use day data instead
# 3.x              Fix the scaler better so every parameter is scaled correctly, and not scal all at ones 
# 4. Get somthing that makes the model archetecture automaticly, its called hyperparameter tuning i think
# 5.x         Make sure that the parameters are separated this time, so that the model knows what is what
# 6.      Find a way so that the model knows what company it is, so that it can predict the right company
# 7.                              Add indicators to the model, like RSI, MACD, Bollinger Bands, and so on
# 8.                               Add the other data and see if it improves the model, if not, remove it
# 9.                 Try to add the comodity data, its to much right know so i need to find a work around
# 10.                                           Do some backtesting, find the best strategy for the model
# 11.         Make a program that checks what comoditeis are the closest to the change in the stock price

companies = []

n_past = 20    # Number of past days we want to use to predict the future.
n_future = 1   # Number of days we want to predict into the future.

for filename in os.listdir("./data/data-week"):
    company_name = filename.split("-")[0]
    if os.path.isfile(f"data/data-day/{company_name}.csv"):
        companies.append(company_name)

data = {}
test_stock = "tesla"   

def build_model(hp):
    input_prices = Input(shape=(X_prices.shape[1], X_prices.shape[2]))
    input_news = Input(shape=(X_news.shape[1], 1))

    lstm_prices = LSTM(hp.Int('units_prices', min_value=32, max_value=512, step=32))(input_prices)
    lstm_news = LSTM(hp.Int('units_news', min_value=32, max_value=512, step=32))(input_news)

    concatenated = concatenate([lstm_prices, lstm_news])
    output = Dense(1, activation='linear')(concatenated)

    model = Model(inputs=[input_prices, input_news], outputs=output)

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
        loss='mse',
        metrics=['mae'])

    return model

for company in companies:
    if company != test_stock:
        # print out a looding bar, that moves to show how many percent are done
        percent = round((companies.index(company) / len(companies)) * 100)
        print(f"Loading data: {percent}% done", end="\r")

        loader = Load_data(period=259, company=company.lower())

        company_data = loader.get_raw_data()
        day_data = loader.load_day_data()

        data[company] = {}

        average_change_down = []
        average_change_up = []

        prices = []
        changes = []

        for date in range(len(company_data['Date'])):

            price = []

            current_date = pd.to_datetime(company_data['Date'][date])
            # print(current_date)

            for index in range(n_past):
                try:
                    past_date = current_date - pd.DateOffset(days=n_past - index)
                    price.append(day_data[day_data['Date'] == past_date]['Adj Close'].values[0].round(2))
                except Exception as e:
                    if len(price) > 0:
                        price.append(price[-1])
                    else:
                        if len(prices) > 0:
                            price.append(prices[-1][-1])
                        else:
                            price.append(0)
            
            prices.append(price)

        # print(prices)

        for date in range(len(prices)):
            current_date = pd.to_datetime(company_data['Date'][date])
            future_date = current_date + pd.DateOffset(days=n_future)

            dates = [str(date).split("T")[0] for date in day_data['Date'].values]
            
            if str(future_date).split(" ")[0] in dates:
                future_price = day_data[day_data['Date'] == future_date]['Adj Close'].values[0]
                change = ((future_price / prices[date][-1]) - 1)
                if change < 0:
                    changes.append(-1)
                else:
                    changes.append(1)
            else:
                current_date = pd.to_datetime(company_data['Date'][date])
                future_date = current_date + pd.DateOffset(days=n_future+2)

                dates = [str(date).split("T")[0] for date in day_data['Date'].values]
                
                if str(future_date).split(" ")[0] in dates:
                    future_price = day_data[day_data['Date'] == future_date]['Adj Close'].values[0]
                    change = ((future_price / prices[date][-1]) - 1)
                    if change < 0:
                        changes.append(-1)
                    else:
                        changes.append(1)
                else:
                    changes.append(0)
                

        print(changes)

        data[company]['prices'] = prices
        data[company]['changes'] = changes
        data[company]['news'] = company_data['score'].values.tolist()

        # print(data)

X_prices = []
X_news = []
y_changes = []

for company in data:
    for i in range(n_past, len(data[company]['prices'])):
        X_prices.append(data[company]['prices'][i])
        X_news.append(data[company]['news'][i])
        y_changes.append(data[company]['changes'][i])

X_prices = np.array(X_prices)
X_news = np.array(X_news)
y_changes = np.array(y_changes)

# Normalize the price data
scaler_prices = MinMaxScaler()
X_prices_normalized = scaler_prices.fit_transform(X_prices.reshape(-1, X_prices.shape[-1])).reshape(X_prices.shape)

# Check the shape of X_news
if len(X_news.shape) < 2:
    X_news = np.expand_dims(X_news, axis=1)

# Reshape the news data
X_news_reshaped = X_news.reshape(X_news.shape[0], X_news.shape[1], 1)

# Check the shape of X_prices
if len(X_prices.shape) < 3:
    X_prices = np.expand_dims(X_prices, axis=2)

# Split the data into training and testing sets
X_prices_train, X_prices_test, X_news_train, X_news_test, y_train, y_test = train_test_split(
    X_prices, X_news_reshaped, y_changes, test_size=0.2, random_state=42
)


tuner = RandomSearch(
    build_model,
    objective='val_mae',           # The metric that should be optimized
    max_trials=5,                  # The numbers of rounds to test
    executions_per_trial=3,        # The number of models that should be tested in each round
    directory='models',            # The directory where the models should be saved
    project_name='stock-predictor' # The name of the project, used in the directory to separate different projects
    )

tuner.search_space_summary()

tuner.search([X_prices_train, X_news_train], y_train,
             epochs=50,
             batch_size=16,
             validation_data=([X_prices_test, X_news_test], y_test),
             verbose=2)

tuner.results_summary()

model = tuner.get_best_models(num_models=1)[0]

model.summary()

#
# TEST
#
tesla_loader = Load_data(period=259, company=test_stock)
tesla_data = tesla_loader.get_raw_data()
tesla_day_data = tesla_loader.load_day_data()

tesla_prices = []
tesla_changes = []
tesla_news = tesla_data['score'].values.tolist()

for date in range(len(tesla_data['Date'])):
    price = []
    current_date = pd.to_datetime(tesla_data['Date'][date])
    for index in range(n_past):
        try:
            past_date = current_date - pd.DateOffset(days=n_past - index)
            price.append(tesla_day_data[tesla_day_data['Date'] == past_date]['Adj Close'].values[0].round(2))
        except Exception as e:
            if len(price) > 0:
                price.append(price[-1])
            else:
                if len(tesla_prices) > 0:
                    price.append(tesla_prices[-1][-1])
                else:
                    price.append(0)
    tesla_prices.append(price)

for date in range(len(tesla_prices)):
    current_date = pd.to_datetime(tesla_data['Date'][date])
    future_date = current_date + pd.DateOffset(days=n_future)

    dates = [str(date).split("T")[0] for date in tesla_day_data['Date'].values]
    
    if str(future_date).split(" ")[0] in dates:
        future_price = tesla_day_data[tesla_day_data['Date'] == future_date]['Adj Close'].values[0]
        change = ((future_price / tesla_prices[date][-1]) - 1)
        if change < 0:
            tesla_changes.append(-1)
        else:
            tesla_changes.append(1)
    else:
        current_date = pd.to_datetime(tesla_data['Date'][date])
        future_date = current_date + pd.DateOffset(days=n_future+2)

        dates = [str(date).split("T")[0] for date in tesla_day_data['Date'].values]
        
        if str(future_date).split(" ")[0] in dates:
            future_price = tesla_day_data[tesla_day_data['Date'] == future_date]['Adj Close'].values[0]
            change = ((future_price / tesla_prices[date][-1]) - 1)
            if change < 0:
                tesla_changes.append(-1)
            else:
                tesla_changes.append(1)
        else:
            tesla_changes.append(0)

tesla_prices = np.array(tesla_prices)
tesla_news = np.array(tesla_news)

tesla_prices_normalized = scaler_prices.transform(tesla_prices.reshape(-1, tesla_prices.shape[-1])).reshape(tesla_prices.shape)

if len(tesla_news.shape) < 2:
    tesla_news = np.expand_dims(tesla_news, axis=1)

tesla_news_reshaped = tesla_news.reshape(tesla_news.shape[0], tesla_news.shape[1], 1)

if len(tesla_prices.shape) < 3:
    tesla_prices = np.expand_dims(tesla_prices, axis=2)

tesla_predictions = model.predict([tesla_prices, tesla_news_reshaped])

plt.plot(tesla_changes, label='Actual Changes')
plt.plot(tesla_predictions, label='Predicted Changes')
plt.legend()
plt.show()
