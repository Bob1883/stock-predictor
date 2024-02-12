import os
import numpy as np
import tensorflow as tf
from keras import Model, regularizers
from keras.layers import LSTM, Dense, Dropout, Embedding, Concatenate, Layer, Bidirectional, BatchNormalization
from keras.losses import MeanSquaredError
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt
from components.constants import *
from components.load_data_for_test import Load_data

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

        # check if it's a good trade
        if company in top_5:
            money -= raw_data[company]['Adj Close'][date] * 1
            if company in stocks:
                stocks[company] += 1
            else:
                stocks[company] = 1

    # put the money we have in hand and the money we have invested in the stocks together, and add it to the money_data array
    money_data.append(money + sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))
    print("money in stocks: ", sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))
    print("money in hand: ", money)
    print("total money: ", money + sum([stocks[company] * raw_data[company]['Adj Close'][date] for company in stocks]))

class MultiHeadAttention(Layer):
    def __init__(self, num_heads=8):
        self.num_heads = num_heads
        super(MultiHeadAttention, self).__init__()

    def build(self, input_shape):
        self.d_model = input_shape[-1]
        assert self.d_model % self.num_heads == 0
        self.depth = self.d_model // self.num_heads
        self.wq = Dense(self.d_model)
        self.wk = Dense(self.d_model)
        self.wv = Dense(self.d_model)
        self.dense = Dense(self.d_model)

    def split_heads(self, x, batch_size):
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def scaled_dot_product_attention(self, q, k, v):
        matmul_qk = tf.matmul(q, k, transpose_b=True)
        dk = tf.cast(tf.shape(k)[-1], tf.float32)
        scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)
        attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)
        output = tf.matmul(attention_weights, v)
        return output, attention_weights

    def call(self, v, k, q):
        batch_size = tf.shape(q)[0]
        q = self.wq(q)
        k = self.wk(k)
        v = self.wv(v)
        q = self.split_heads(q, batch_size)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)
        scaled_attention, attention_weights = self.scaled_dot_product_attention(q, k, v)
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))
        output = self.dense(concat_attention)
        return output

class EnhancedLstmRNN(Model):
    def __init__(self, stock_count, lstm_size=128, num_layers=3, num_steps=30, input_size=3, embed_size=50, dropout_rate=0.2):
        super(EnhancedLstmRNN, self).__init__()

        self.stock_count = stock_count
        self.lstm_size = lstm_size
        self.num_layers = num_layers
        self.num_steps = num_steps
        self.input_size = input_size
        self.embed_size = embed_size

        self.embedding = Embedding(stock_count, embed_size, input_length=1)
        self.lstm_layers = [Bidirectional(LSTM(lstm_size, return_sequences=True)) for _ in range(num_layers)]
        self.attention = MultiHeadAttention(num_heads=8)
        self.dropout_layers = [Dropout(dropout_rate) for _ in range(num_layers)]
        self.dense_layers = [Dense(64, activation='relu'), Dense(32, activation='relu')]
        self.batch_norm_layers = [BatchNormalization() for _ in range(num_layers)]
        self.final_dense = Dense(1, kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4))

    def call(self, inputs):
        symbols, features = inputs
        x = self.embedding(symbols)
        x = tf.repeat(x, self.num_steps, axis=1)
        x = Concatenate()([x, features])
        for lstm, dropout, batch_norm in zip(self.lstm_layers, self.dropout_layers, self.batch_norm_layers):
            x = lstm(x)
            x = dropout(x)
            x = batch_norm(x)
        x = self.attention(x, x, x)
        for dense in self.dense_layers:
            x = dense(x)
        return self.final_dense(x)

    def train(self, data, raw_data, companies, config):
        symbols = np.array([[companies.index(company)] for company in companies])
        features = np.array([data[company] for company in companies]).astype(np.float32)
        prices = np.array([raw_data[company] for company in companies]).astype(np.float32)

        self.compile(optimizer=Adam(learning_rate=config['learning_rate']), loss=MeanSquaredError())
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.0001)
        self.fit([symbols, features], prices, epochs=config['epochs'], batch_size=config['batch_size'], callbacks=[reduce_lr])

        # predictions = self.predict([symbols, features])[2]
        # print(predictions)

        # plt.plot(prices, label='Actual')
        # plt.plot(predictions, label='Predicted')
        # plt.legend()
        # plt.show()

config = {
    'learning_rate': 0.001,
    'epochs': 100,
    'batch_size': 32
}

# Data Loading and Prediction Code
companies = []
for filename in os.listdir("data/data-week"):
    company_name = filename.split("-")[0]
    if os.path.isfile(f"data/data-google-trends/{company_name}-trend.json") and os.path.isfile(f"data/data-political/{company_name}-political.json"):
        companies.append(company_name)

data = {}
raw_data = {}
for company in companies:
    loader = Load_data(period=259, company=company.lower())
    data[company] = loader.get_all_data()
    raw_data[company] = loader.get_raw_data()

plt.figure()

model = EnhancedLstmRNN(stock_count=len(companies), lstm_size=128, num_layers=3, num_steps=259, input_size=3, embed_size=50)
model.train(data, raw_data, companies, config)

number_of_weeks = 52*5 - 20 
predictions = {}
n_future = 1
n_past = 10

for company in data:
    company_data = data[company]
    prediction_data = []

    for i in range(n_past, len(company_data) - n_future +1):
        prediction_data.append(company_data[i - n_past:i, 0:company_data.shape[1]])

    prediction_data = np.array(prediction_data)

    # Use the AI model to predict
    company_index = np.array([companies.index(company)] * len(prediction_data))
    company_index = company_index.reshape(prediction_data.shape[0], -1)
    prediction = model.predict([company_index, prediction_data])
    
    predictions[company] = prediction.flatten().tolist()

for i in range(number_of_weeks):
    date = len(data[company]) - (number_of_weeks - i)
    weeks_predictions = {}

    for company in predictions:
        weeks_predictions[company] = predictions[company][date - n_past][0]

    pick_stocks(weeks_predictions, date, raw_data, predictions)

    plt.plot(money_data)
    plt.legend(["Money"])
    plt.gca().lines[0].set_color("red")
    plt.draw()
    plt.pause(0.01)

plt.show()
