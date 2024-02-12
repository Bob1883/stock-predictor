from components.constants import *
from components.load_data import Load_data
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from keras.callbacks import EarlyStopping
import statsmodels.api as sm
from scipy.stats.mstats import winsorize

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

# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)

data = Load_data(period=259, test_company="apple", political=True)

historical = data.load_historical()    # evrey companys in an array, evrey array has 259 weeks
google_trends = data.load_google_trends() # evrey companys trend in an array, evrey array has 259 weeks
news = data.load_news()          # evrey companys news in an array, evrey array has 259 weeks
political = data.load_political()     # evrey companys political in an array, evrey array has 259 weeks
commodity = data.load_commodity()     # commodity data, for 259 weeks
world_economy = data.load_world_economy() # world economy data, for 259 weeks

historical_test = data.historical_test
google_trends_test = data.google_trends_test
news_test = data.news_test
political_test = data.political_test
commodity_test = data.commodity_test
world_economy_test = data.world_economy_test

data = pd.concat([historical, google_trends, news, political, commodity, world_economy], axis=1)
data.reset_index(drop=True, inplace=True)

# change adj close to the change in price
data['Adj Close'] = data['Adj Close'].pct_change()
data['Adj Close'] = data['Adj Close'].fillna(0)
print(data)

# smooth out the adj close a lot, so its not as speratic
lowess = sm.nonparametric.lowess
z = lowess(data['Adj Close'], range(len(data['Adj Close'])), frac=0.0009) 

data['Adj Close'] = z[:,1]

data['Adj Close'] = winsorize(data['Adj Close'], limits=[0.03, 0.03]) 

# int("crash")

#Variables for training
cols = list(data)[0:27]
#Date and volume columns are not used in training. 
print(cols) #['Open', 'High', 'Low', 'Close', 'Adj Close']

df_for_training = data[cols].astype(float)

scaler = StandardScaler()
scaler = scaler.fit(df_for_training)
df_for_training_scaled = scaler.transform(df_for_training)

trainX = []
trainY = []

n_future = 1   # Number of weeks we want to look into the future based on the past weeks.
n_past = 10  # Number of past weeks we want to use to predict the future.

for i in range(n_past, len(df_for_training_scaled) - n_future +1):
    trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
    trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])

trainX, trainY = np.array(trainX), np.array(trainY)

# define the Autoencoder model
model = Sequential()
model.add(LSTM(256, activation='selu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(128, activation='selu', return_sequences=False))
model.add(Dropout(0.5))
model.add(Dense(128, activation='selu'))
model.add(Dropout(0.5))
model.add(Dense(trainY.shape[1]))

# relu -> 0.77 
# tanh -> 0.96
# sigmoid -> 0.77
# softmax -> 0.63
# softplus -> 0.94
# softsign -> 0.82 but looks very good, can see in the future better 
# selu -> 0.93 but very consistent
# elu -> 0.72 but very, very good at predicting the future

# with change in price
# tanh -> -0.00017989142824759163
# softplus -> -0.0013818416335500405 
# softsign -> 0.0016387287292426445
# selu -> -0.0024990434861453803
# elu -> -0.0014186812734304777 But things happen

# with new preprocessing
# tanh -> 0.45
# softsign ->  0.467
# softplus -> 0.40
# selu -> 0.48
# elu -> 0.45

# relu -> 0.47 
# sigmoid -> 0.45
# softmax -> 0.46 but very consistent, and looks good



model.compile(optimizer='Adam', loss='huber_loss')
model.summary()

# difrent optimizers
# Nadam -> 0.48
# Adam -> 0.44
# SGD -> 0.5
# RMSprop -> 0.46
# Adadelta -> 0.39 very bad
# Adagrad -> 0.45 shit
# Adamax -> 0.46
# Ftrl -> 0.48 bretty good 

# difrent loss
# mse -> 0.5
# mae -> 0.49 
# mape -> nan 
# msle -> 0.46
# kld -> 0.32
# cosine_similarity -> 0.25
# huber_loss -> 0.51
# logcosh -> 0.5 

history = model.fit(trainX, trainY, epochs=100, batch_size=100, validation_split=0.1, verbose=1)

# try on test data
df_test = pd.concat([historical_test, google_trends_test, news_test, political_test, commodity_test, world_economy_test], axis=1)
df_test.reset_index(drop=True, inplace=True)

# change adj close to the change in price
df_test['Adj Close'] = df_test['Adj Close'].pct_change()
df_test['Adj Close'] = df_test['Adj Close'].fillna(0)

# smooth out the adj close a lot, so its not as speratic
lowess = sm.nonparametric.lowess
z = lowess(df_test['Adj Close'], range(len(df_test['Adj Close'])), frac=0.0009)

df_test['Adj Close'] = z[:,1]

df_test['Adj Close'] = winsorize(df_test['Adj Close'], limits=[0.03, 0.03])

df_for_test = df_test[cols].astype(float)

scaler = StandardScaler()
scaler = scaler.fit(df_for_test)
df_for_test_scaled = scaler.transform(df_for_test)

testX = []
testY = []

for i in range(n_past, len(df_for_test_scaled) - n_future +1): 
    testX.append(df_for_test_scaled[i - n_past:i, 0:df_for_test.shape[1]])
    testY.append(df_for_test_scaled[i + n_future - 1:i + n_future, 0])

testX, testY = np.array(testX), np.array(testY)

# make predictions
y_pred = model.predict(testX)

y_pred = y_pred.flatten()
y_test_t = testY.flatten()

# # move pred back by 3 weeks
# y_pred = np.roll(y_pred, -3)

# # remove last 3 weeks from y_test_t and y_pred
# y_pred = y_pred[:-3]
# y_test_t = y_test_t[:-3]

# show the results, predicted vs actual price
plt.plot(y_test_t)
plt.plot(y_pred)
plt.legend(["Actual Price", "Predicted Price"])
plt.show()

# calculate the accuracy
clac_accuracy(y_test_t, y_pred)

#  save the model
model.save("models/model_1.h5")