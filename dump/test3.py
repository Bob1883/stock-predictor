import numpy as np
import tensorflow as tf
from keras import Model, regularizers
from keras.layers import LSTM, Dense, Dropout, Embedding, Concatenate, Layer, Bidirectional
from keras.losses import MeanSquaredError
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import os
from components.load_data_for_test import Load_data

class Attention(Layer):
    def __init__(self, return_sequences=True):
        self.return_sequences = return_sequences
        super(Attention,self).__init__()
        
    def build(self, input_shape):
        self.W=self.add_weight(name="att_weight", shape=(input_shape[-1],1), initializer="normal")
        self.b=self.add_weight(name="att_bias", shape=(input_shape[1],1), initializer="zeros")        
        super(Attention,self).build(input_shape)
        
    def call(self, x):
        e = tf.nn.tanh(tf.tensordot(x,self.W,axes=1) + self.b)
        a = tf.nn.softmax(e, axis=1)
        output = x*a
        if self.return_sequences:
            return output
        return tf.reduce_sum(output, axis=1)

class EnhancedLstmRNN(Model):
    def __init__(self, stock_count, lstm_size=128, num_layers=2, num_steps=30, input_size=3, embed_size=50, dropout_rate=0.2):
        super(EnhancedLstmRNN, self).__init__()

        self.stock_count = stock_count
        self.lstm_size = lstm_size
        self.num_layers = num_layers
        self.num_steps = num_steps
        self.input_size = input_size
        self.embed_size = embed_size

        self.embedding = Embedding(stock_count, embed_size, input_length=1)
        self.lstm_layers = [Bidirectional(LSTM(lstm_size, return_sequences=True)) for _ in range(num_layers)]
        self.attention = Attention(return_sequences=False)
        self.dropout_layers = [Dropout(dropout_rate) for _ in range(num_layers)]
        self.dense = Dense(1, kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4))

    def call(self, inputs):
        symbols, features = inputs
        x = self.embedding(symbols)
        x = tf.repeat(x, self.num_steps, axis=1)
        x = tf.reshape(x, [-1, self.num_steps, self.embed_size])  # Adjust this line
        x = Concatenate()([x, features])
        for lstm, dropout in zip(self.lstm_layers, self.dropout_layers):
            x = lstm(x)
            x = dropout(x)
        x = self.attention(x)
        return self.dense(x)

    def train(self, config):
        # get the company names
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

        # Here, you need to process the data to match the format expected by your model
        # This will depend on how your model expects the data to be formatted
        # For example, if your model expects the data to be in the form of (samples, time_steps, features), you need to reshape the data accordingly
        # Let's assume that your model expects the data in the form of (samples, time_steps, features)
        symbols = np.array([i for i in range(len(companies))])
        features = np.array([data[company] for company in companies])
        prices = np.array([raw_data[company]['Adj Close'] for company in companies])

        self.compile(optimizer=Adam(learning_rate=config['learning_rate']), loss=MeanSquaredError())
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.0001)
        self.fit([symbols, features], prices, epochs=config['epochs'], batch_size=config['batch_size'], callbacks=[reduce_lr])

        predictions = self.predict([symbols, features])

        plt.plot(prices, label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.legend()
        plt.show()

model = EnhancedLstmRNN(stock_count=10, lstm_size=128, num_layers=2, num_steps=30, input_size=3, embed_size=50)

config = {
    'learning_rate': 0.001,
    'epochs': 100,
    'batch_size': 32
}

model.train(config=config)