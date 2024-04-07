from preprocessing import *

# DONE                                          TODO                                                   DOING
#█ x █ Load in day data and use it when training, 20 days back                                         █   █
#█ x █ Rewrite change, becuse now the price data is of, use day data instead                           █   █
#█ x █ Fix the scaler better so every parameter is scaled correctly, and not scal all at ones          █   █
#█ x █ Implemrnt hyperparameter tuning                                                                 █   █
#█ x █ Make sure that the parameters are separated this time, so that the model knows what is what     █   █
#█ x █ Find a way so that the model knows what company it is, so that it can predict the right company █   █
#█ x █ Try to add the comodity data, its to much right know so i need to find a work around            █   █
#█ x █ Make a program that checks what comoditeis are the closest to the change in the stock price     █   █
#█ x █ Add indicators to the model, like RSI, MACD, Bollinger Bands, and so on                         █   █    
#█ x █ Fix data looding bug                                                                            █   █    
#█ x █ Change get data to be a def                                                                     █   █
#█ x █ Add stock fundamentals, i dont really know where but i will try                                 █   █
#█ x █ Add the looding bar for the training                                                            █   █
#█ x █ Check the world data                                                                            █   █
#█ x █ Fix changes                                                                                     █   █
#█ x █ Fix news                                                                                        █   █
#█ x █ Fix price                                                                                       █   █
#█ x █ Add the other data and see if it improves the model, if not, remove it                          █   █
#█ x █ Commodity data looding is wrong                                                                 █   █
#█   █ To much data from indicastors                                                                   █ x █	
#█   █ indicators needs work                                                                           █ x █
#█   █ Add a algorithm to see what indicators are the best for AI backtesting                          █   █
#█   █ Test witch commodity normelizer is best                                                         █   █

#█   █ Do some backtesting, find the best strategy for the model                                       █   █
#█   █ If total falure is achieved, pick a stock strat                                                 █   █
#█   █ Check with companies the model is best at                                                       █   █
#█   █ Fundementals data is to incomplete, find a better source (future problem)                       █   █

def build_model(hp):
    input_prices = Input(shape=(n_past, 1))
    input_news = Input(shape=(1,))
    input_commoditie1 = Input(shape=(1,))
    input_commoditie2 = Input(shape=(1,))
    input_commoditie3 = Input(shape=(1,))
    input_names = Input(shape=(1,))
    input_rsi = Input(shape=(1,))
    input_macd = Input(shape=(1,))
    input_ema_20 = Input(shape=(1,))
    input_ema_50 = Input(shape=(1,))
    input_ema_200 = Input(shape=(1,))
    input_bb_low = Input(shape=(1,))
    input_bb_high = Input(shape=(1,))
    input_obv = Input(shape=(1,))
    input_debt = Input(shape=(1,))
    input_gdp = Input(shape=(1,))
    input_inflation = Input(shape=(1,))
    input_unemployement = Input(shape=(1,))
    
    # Prices branch
    lstm_prices = LSTM(units=hp.Int('lstm_units_prices', min_value=32, max_value=512, step=32), return_sequences=True)(input_prices)
    lstm_prices = Dropout(hp.Float('dropout_prices', min_value=0.1, max_value=0.5, step=0.1))(lstm_prices)
    lstm_prices = LSTM(units=hp.Int('lstm_units_prices_2', min_value=32, max_value=512, step=32))(lstm_prices)
    
    # News branch
    dense_news = Dense(units=hp.Int('dense_units_news', min_value=32, max_value=512, step=32), activation='relu')(input_news)
    dense_news = Dropout(hp.Float('dropout_news', min_value=0.1, max_value=0.5, step=0.1))(dense_news)
    
    # Commodities branch
    dense_commoditie1 = Dense(units=hp.Int('dense_units_commoditie1', min_value=32, max_value=512, step=32), activation='relu')(input_commoditie1)
    dense_commoditie1 = Dropout(hp.Float('dropout_commoditie1', min_value=0.1, max_value=0.5, step=0.1))(dense_commoditie1)
    dense_commoditie2 = Dense(units=hp.Int('dense_units_commoditie2', min_value=32, max_value=512, step=32), activation='relu')(input_commoditie2)
    dense_commoditie2 = Dropout(hp.Float('dropout_commoditie2', min_value=0.1, max_value=0.5, step=0.1))(dense_commoditie2)
    dense_commoditie3 = Dense(units=hp.Int('dense_units_commoditie3', min_value=32, max_value=512, step=32), activation='relu')(input_commoditie3)
    dense_commoditie3 = Dropout(hp.Float('dropout_commoditie3', min_value=0.1, max_value=0.5, step=0.1))(dense_commoditie3)
    
    # Names branch
    dense_names = Dense(units=hp.Int('dense_units_names', min_value=32, max_value=512, step=32), activation='relu')(input_names)
    dense_names = Dropout(hp.Float('dropout_names', min_value=0.1, max_value=0.5, step=0.1))(dense_names)
    
    # RSI branch
    dense_rsi = Dense(units=hp.Int('dense_units_rsi', min_value=32, max_value=512, step=32), activation='relu')(input_rsi)
    dense_rsi = Dropout(hp.Float('dropout_rsi', min_value=0.1, max_value=0.5, step=0.1))(dense_rsi)
    
    # MACD branch
    dense_macd = Dense(units=hp.Int('dense_units_macd', min_value=32, max_value=512, step=32), activation='relu')(input_macd)
    dense_macd = Dropout(hp.Float('dropout_macd', min_value=0.1, max_value=0.5, step=0.1))(dense_macd)
    
    # EMA branches
    dense_ema_20 = Dense(units=hp.Int('dense_units_ema_20', min_value=32, max_value=512, step=32), activation='relu')(input_ema_20)
    dense_ema_20 = Dropout(hp.Float('dropout_ema_20', min_value=0.1, max_value=0.5, step=0.1))(dense_ema_20)
    dense_ema_50 = Dense(units=hp.Int('dense_units_ema_50', min_value=32, max_value=512, step=32), activation='relu')(input_ema_50)
    dense_ema_50 = Dropout(hp.Float('dropout_ema_50', min_value=0.1, max_value=0.5, step=0.1))(dense_ema_50)
    dense_ema_200 = Dense(units=hp.Int('dense_units_ema_200', min_value=32, max_value=512, step=32), activation='relu')(input_ema_200)
    dense_ema_200 = Dropout(hp.Float('dropout_ema_200', min_value=0.1, max_value=0.5, step=0.1))(dense_ema_200)
    
    # Bollinger Bands branches
    dense_bb_low = Dense(units=hp.Int('dense_units_bb_low', min_value=32, max_value=512, step=32), activation='relu')(input_bb_low)
    dense_bb_low = Dropout(hp.Float('dropout_bb_low', min_value=0.1, max_value=0.5, step=0.1))(dense_bb_low)
    dense_bb_high = Dense(units=hp.Int('dense_units_bb_high', min_value=32, max_value=512, step=32), activation='relu')(input_bb_high)
    dense_bb_high = Dropout(hp.Float('dropout_bb_high', min_value=0.1, max_value=0.5, step=0.1))(dense_bb_high)
    
    # OBV branch
    dense_obv = Dense(units=hp.Int('dense_units_obv', min_value=32, max_value=512, step=32), activation='relu')(input_obv)
    dense_obv = Dropout(hp.Float('dropout_obv', min_value=0.1, max_value=0.5, step=0.1))(dense_obv)
    
    # Debt branch
    dense_debt = Dense(units=hp.Int('dense_units_debt', min_value=32, max_value=512, step=32), activation='relu')(input_debt)
    dense_debt = Dropout(hp.Float('dropout_debt', min_value=0.1, max_value=0.5, step=0.1))(dense_debt)
    
    # GDP branch
    dense_gdp = Dense(units=hp.Int('dense_units_gdp', min_value=32, max_value=512, step=32), activation='relu')(input_gdp)
    dense_gdp = Dropout(hp.Float('dropout_gdp', min_value=0.1, max_value=0.5, step=0.1))(dense_gdp)
    
    # Inflation branch
    dense_inflation = Dense(units=hp.Int('dense_units_inflation', min_value=32, max_value=512, step=32), activation='relu')(input_inflation)
    dense_inflation = Dropout(hp.Float('dropout_inflation', min_value=0.1, max_value=0.5, step=0.1))(dense_inflation)
    
    # Unemployment branch
    dense_unemployement = Dense(units=hp.Int('dense_units_unemployement', min_value=32, max_value=512, step=32), activation='relu')(input_unemployement)
    dense_unemployement = Dropout(hp.Float('dropout_unemployement', min_value=0.1, max_value=0.5, step=0.1))(dense_unemployement)
    
    # Concatenate all branches
    concatenated = Concatenate()([lstm_prices, dense_news, dense_commoditie1, dense_commoditie2, dense_commoditie3, dense_names,
                                  dense_rsi, dense_macd, dense_ema_20, dense_ema_50, dense_ema_200, dense_bb_low, dense_bb_high,
                                  dense_obv, dense_debt, dense_gdp, dense_inflation, dense_unemployement])
    
    # Output layer
    output = Dense(1, activation='linear')(concatenated)
    
    model = Model(inputs=[input_prices, input_news, input_commoditie1, input_commoditie2, input_commoditie3, input_names,
                          input_rsi, input_macd, input_ema_20, input_ema_50, input_ema_200, input_bb_low, input_bb_high,
                          input_obv, input_debt, input_gdp, input_inflation, input_unemployement], outputs=output)
    
    model.compile(optimizer=Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                  loss='mse',
                  metrics=['mae'])
    
    return model

def train_model(companies, test_stock, periode, max_trials=50, executions_per_trial=3):
    # Preprocessing
    commodties, google_trends, changes, prices, political, news, names, rsi, macd, ema_20, ema_50, ema_200, bb_low, bb_high, obv, debt, gdp, inflation, unemployement = preprocessing(companies, test_stock, periode)
   
    # Split commodities into three different variables
    commodity1, commodity2, commodity3 = [], [], []
    # so its an array of a few hundred lists, the first list should go in commodity1, the second in commodity2, and the third in commodity3, then the fourth in commodity1 and so on
    for i, commodity in enumerate(commodties):
        if i % 3 == 0:
            for n in range(len(commodity)):
                commodity1.append(commodity[n])
        elif i % 3 == 1:
            for n in range(len(commodity)):
                commodity2.append(commodity[n])
        else:
            for n in range(len(commodity)):
                commodity3.append(commodity[n])
    
    # Convert to numpy arrays
    prices = np.array(prices)
    news = np.array(news)
    commodity1 = np.array(commodity1)
    commodity2 = np.array(commodity2)
    commodity3 = np.array(commodity3)
    names = np.array(names)
    rsi = np.array(rsi)
    macd = np.array(macd)
    ema_20 = np.array(ema_20)
    ema_50 = np.array(ema_50)
    ema_200 = np.array(ema_200)
    bb_low = np.array(bb_low)
    bb_high = np.array(bb_high)
    obv = np.array(obv)
    debt = np.array(debt)
    gdp = np.array(gdp)
    inflation = np.array(inflation)
    unemployement = np.array(unemployement)
    changes = np.array(changes)
   
    # Split data into train, validation, and test sets
    X_prices_train, X_prices_test, X_news_train, X_news_test, X_commodity1_train, X_commodity1_test, X_commodity2_train, X_commodity2_test, X_commodity3_train, X_commodity3_test, X_names_train, X_names_test, X_rsi_train, X_rsi_test, X_macd_train, X_macd_test, X_ema_20_train, X_ema_20_test, X_ema_50_train, X_ema_50_test, X_ema_200_train, X_ema_200_test, X_bb_low_train, X_bb_low_test, X_bb_high_train, X_bb_high_test, X_obv_train, X_obv_test, X_debt_train, X_debt_test, X_gdp_train, X_gdp_test, X_inflation_train, X_inflation_test, X_unemployement_train, X_unemployement_test, y_train, y_test = train_test_split(prices, news, commodity1, commodity2, commodity3, names, rsi, macd, ema_20, ema_50, ema_200, bb_low, bb_high, obv, debt, gdp, inflation, unemployement, changes, test_size=0.2, random_state=42)
    
    X_prices_train, X_prices_val, X_news_train, X_news_val, X_commodity1_train, X_commodity1_val, X_commodity2_train, X_commodity2_val, X_commodity3_train, X_commodity3_val, X_names_train, X_names_val, X_rsi_train, X_rsi_val, X_macd_train, X_macd_val, X_ema_20_train, X_ema_20_val, X_ema_50_train, X_ema_50_val, X_ema_200_train, X_ema_200_val, X_bb_low_train, X_bb_low_val, X_bb_high_train, X_bb_high_val, X_obv_train, X_obv_val, X_debt_train, X_debt_val, X_gdp_train, X_gdp_val, X_inflation_train, X_inflation_val, X_unemployement_train, X_unemployement_val, y_train, y_val = train_test_split(X_prices_train, X_news_train, X_commodity1_train, X_commodity2_train, X_commodity3_train, X_names_train, X_rsi_train, X_macd_train, X_ema_20_train, X_ema_50_train, X_ema_200_train, X_bb_low_train, X_bb_high_train, X_obv_train, X_debt_train, X_gdp_train, X_inflation_train, X_unemployement_train, y_train, test_size=0.2, random_state=42)
   
    # Reshape input data
    X_prices_train = np.reshape(X_prices_train, (X_prices_train.shape[0], X_prices_train.shape[1], 1))
    X_prices_val = np.reshape(X_prices_val, (X_prices_val.shape[0], X_prices_val.shape[1], 1))
    X_prices_test = np.reshape(X_prices_test, (X_prices_test.shape[0], X_prices_test.shape[1], 1))
   

    num_tests = len([name for name in os.listdir('models') if os.path.isdir(f'models/{name}')])
    model_dir = f'models/stock-predictor-1'
    os.makedirs(model_dir, exist_ok=True)

    tuner = RandomSearch(
        build_model,
        objective='val_mae',
        max_trials=max_trials,
        executions_per_trial=executions_per_trial,
        directory=model_dir,
        project_name='stock-predictor'
    )

    # Early stopping and model checkpointing
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint(f'{model_dir}/best_model.h5', save_best_only=True, monitor='val_loss', mode='min')

    # Perform the search
    tuner.search(
        [X_prices_train, X_news_train, X_commodity1_train, X_commodity2_train, X_commodity3_train, X_names_train,
        X_rsi_train, X_macd_train, X_ema_20_train, X_ema_50_train, X_ema_200_train, X_bb_low_train, X_bb_high_train,
        X_obv_train, X_debt_train, X_gdp_train, X_inflation_train, X_unemployement_train],
        y_train,
        epochs=100,
        batch_size=32,
        validation_data=([X_prices_val, X_news_val, X_commodity1_val, X_commodity2_val, X_commodity3_val, X_names_val,
                        X_rsi_val, X_macd_val, X_ema_20_val, X_ema_50_val, X_ema_200_val, X_bb_low_val, X_bb_high_val,
                        X_obv_val, X_debt_val, X_gdp_val, X_inflation_val, X_unemployement_val], y_val),
        callbacks=[early_stopping, model_checkpoint],
        verbose=1
    )

    # Get the best model
    best_model = tuner.get_best_models(num_models=1)[0]
    best_model.summary()

    # Save the best model
    best_model.save(f'{model_dir}/best_model.h5')

    # Evaluate the model on the test set
    y_pred = best_model.predict([X_prices_test, X_news_test, X_commodity1_test, X_commodity2_test, X_commodity3_test, X_names_test,
                                X_rsi_test, X_macd_test, X_ema_20_test, X_ema_50_test, X_ema_200_test, X_bb_low_test, X_bb_high_test,
                                X_obv_test, X_debt_test, X_gdp_test, X_inflation_test, X_unemployement_test])

    y_t = [val - 0.5 for val in y_test]
    y_p = [val - 0.5 for val in y_pred]
    clac_accuracy(y_t, y_p)

    # Plot the real vs predicted stock prices
    plt.figure(figsize=(12, 6))
    plt.plot(y_test, color='red', label='Real Stock Price')
    plt.plot(y_pred, color='blue', label='Predicted Stock Price')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

companies = []
for filename in os.listdir('data/data-day'):
    if filename.endswith('.csv'):
        companies.append(filename.split('.')[0].lower())

train_model(companies, test_stock, periode, max_trials=10, executions_per_trial=3)