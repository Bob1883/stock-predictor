import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import json
import time
from keras.models import Model
from keras.layers import Input, LSTM, concatenate, Dense
from sklearn.metrics import r2_score
from components.constants import *
from components.load_data import Load_data

# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)

# Load the data
data = Load_data(period=259, test_company="tesla", political=True)

historical = data.load_historical()    # evrey companys in an array, evrey array has 259 weeks
google_trends = data.load_google_trends() # evrey companys trend in an array, evrey array has 259 weeks
news = data.load_news()          # evrey companys news in an array, evrey array has 259 weeks
political = data.load_political()     # evrey companys political in an array, evrey array has 259 weeks
commodity = data.load_commodity()     # commodity data, for 259 weeks
world_economy = data.load_world_economy() # world economy data, for 259 weeks

print(historical)
print(google_trends)
print(news)
print(political)
print(commodity)
print(world_economy)

# repet the columns in commodity and world_economy to match the length of the other data
# add them all together
data = pd.concat([historical, google_trends, news, political, commodity, world_economy], axis=1)
data.reset_index(drop=True, inplace=True)
print(data)
# time.sleep(100)
# 20979 rows x 26 columns

# split the data into train and test
train = data.iloc[:int(data.shape[0]*0.8), :]
test = data.iloc[int(data.shape[0]*0.8):, :]

# split the data into X and y
X_train = train.iloc[:, :-1]
y_train = train.iloc[:, -1]
X_test = test.iloc[:, :-1]
y_test = test.iloc[:, -1]

# scale the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# reshape the data
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# build the model
input_layer = Input(shape=(X_train.shape[1], X_train.shape[2]))
lstm_layer = LSTM(50, activation="tanh")(input_layer)
dense_layer = Dense(1, activation="linear")(lstm_layer)

model = Model(inputs=input_layer, outputs=dense_layer)
model.compile(loss='mean_squared_error', optimizer='adam')

# train the model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=500, batch_size=32)

# plot the training loss and validation loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['train', 'validation'])
plt.show()

# save the model
model.save('model.h5')

# make predictions
data = Load_data(period=259, test_company="tesla", political=True)

data.load_historical()
data.load_google_trends()
data.load_news()
data.load_political()
data.load_commodity()
data.load_world_economy()

historical_test = data.historical_test
google_trends_test = data.google_trends_test
news_test = data.news_test
political_test = data.political_test
commodity_test = data.commodity_test
world_economy_test = data.world_economy_test

# print(historical_test)
# print(google_trends_test)
# print(news_test)
# print(political_test)
# print(commodity_test)

data = pd.concat([historical_test, google_trends_test, news_test, political_test, commodity_test, world_economy_test], axis=1)
data.reset_index(drop=True, inplace=True)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X = scaler.transform(X)
X = X.reshape((X.shape[0], 1, X.shape[1]))

y_pred = model.predict(X)
# y_pred = scaler.inverse_transform(y_pred)
y_pred = y_pred.reshape(y_pred.shape[0],)

# calculate the r2 score
r2 = r2_score(y, y_pred)
print(r2)

# plot the results
plt.plot(y, color='blue')
plt.plot(y_pred, color='red')
plt.legend(['real', 'prediction'])
plt.show()