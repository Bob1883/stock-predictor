import tensorflow as tf
from tensorflow import keras
from keras import layers
from kerastuner.tuners import RandomSearch

def build_model(hp):
    model = keras.Sequential()
    model.add(layers.Embedding(input_dim=1000, output_dim=50, input_length=100))
    model.add(layers.LSTM(units=hp.Int('units', min_value=32, max_value=512, step=32), return_sequences=True))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
        loss='binary_crossentropy',
        metrics=['accuracy'])
    return model

tuner = RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=5,
    executions_per_trial=3,
    directory='my_dir',
    project_name='helloworld')

tuner.search_space_summary()

# Assume you have some data X_train, y_train, X_val, y_val
# tuner.search(X_train, y_train,
#              epochs=5,
#              validation_data=(X_val, y_val))

tuner.results_summary()