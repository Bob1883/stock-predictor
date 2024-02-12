import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import r2_score

data1 = []
names = []

for filename in os.listdir("data/data-week"):
    if filename == "tesla-week.csv": 
        continue
    if filename.endswith(".csv") and filename.split("-")[0] != "Tesla":
        if len(pd.read_csv(f"data/data-week/{filename}")) >= 260:
            df = pd.read_csv(f"data/data-week/{filename}")
            df['name'] = filename.split("-")[0]  
            data1.append(df)
            names.append(filename.split("-")[0])

for i in range(len(data1)):
    data1[i] = data1[i].iloc[:259, :]
    data1[i].reset_index(drop=True, inplace=True)

data1 = pd.concat(data1, axis=0)
data1.reset_index(drop=True, inplace=True)

scaler = MinMaxScaler()
data1['Close'] = data1['Close'].diff()  # calculate the price change
data1 = data1.dropna()  # remove the first row which is NaN
data1['Close'] = scaler.fit_transform(data1['Close'].values.reshape(-1, 1))

X = data1['Close'].values[:-1]  
y = data1['Close'].values[1:]   

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.reshape((X_train.shape[0], 1, 1))
X_test = X_test.reshape((X_test.shape[0], 1, 1))

model = Sequential()
model.add(LSTM(50, activation="tanh", input_shape=(1, 1)))
model.add(Dense(1, activation="linear"))

model.compile(loss='mean_squared_error', optimizer='adam')

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=500, batch_size=32)

loss = model.evaluate(X_test, y_test)
print('Test loss:', loss)

tesla_data = pd.read_csv('data/data-week/Tesla-week.csv')
tesla_data['Close'] = tesla_data['Close'].diff()  # calculate the price change
tesla_data = tesla_data.dropna()  # remove the first row which is NaN
tesla_data['Close'] = scaler.transform(tesla_data['Close'].values.reshape(-1, 1))  

X_tesla = tesla_data['Close'].values[:-1]  
y_tesla = tesla_data['Close'].values[1:]   

X_tesla = X_tesla.reshape((X_tesla.shape[0], 1, 1))

y_tesla_pred = model.predict(X_tesla)

r2 = r2_score(y_tesla, y_tesla_pred)
print('R^2 score:', r2)

plt.plot(y_tesla, label='Actual')
plt.plot(y_tesla_pred, label='Predicted')
plt.legend()
plt.show()