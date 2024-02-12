from dependencies import *

# DONE                                               TODO                                                   DOING
#█ x █                                              Load in day data and use it when training, 20 days back █   █
#█ x █                                rewrite change, becuse now the price data is of, use day data instead █   █
#█ x █               Fix the scaler better so every parameter is scaled correctly, and not scal all at ones █   █
#█ x █ Get somthing that makes the model archetecture automaticly, its called hyperparameter tuning i think █   █
#█ x █          Make sure that the parameters are separated this time, so that the model knows what is what █   █
#█ x █      Find a way so that the model knows what company it is, so that it can predict the right company █   █
#█ x █                 Try to add the comodity data, its to much right know so i need to find a work around █   █
#█ x █          Make a program that checks what comoditeis are the closest to the change in the stock price █   █
#█ x █                              Add indicators to the model, like RSI, MACD, Bollinger Bands, and so on █   █    
#█ x █                                                                                 Fix data looding bug █   █    
#█ x █                                                                          Change get data to be a def █   █
#█ x █                                      Add stock fundamentals, i dont really know where but i will try █   █
#█ x █                                                                 Add the looding bar for the training █   █
#█   █                                                                                 Check the world data █ x █
#█   █                                                                               Add stock fundamentals █ x █
#█   █                               Add the other data and see if it improves the model, if not, remove it █   █
#█   █                                            Do some backtesting, find the best strategy for the model █   █
#█   █                                                      If total falure is achieved, pick a stock strat █   █
#█   █                                                            Check with companies the model is best at █   █
#█   █                               Add a algorithm to see what indicators are the best for AI backtesting █   █
#█   █                                             Dubble check price and commodity thing it might be wrong █   █

for filename in os.listdir("./data/data-week"):
    company_name = filename.split("-")[0]
    if os.path.isfile(f"data/data-day/{company_name}.csv"):
        companies.append(company_name)

print("\nLoading data...")
data, indicators = preprocessing(companies, test_stock, exclude=[])

print("\n\nFinding best commodities...")
best_commodities = loader.find_best_commodity(companies)

for company in data:
    name = encoder.fit_transform([[company]])
    for i in range(n_past, len(data[company]['prices'])):
        X_name.append(name)
        X_prices.append(data[company]['prices'][i])
        X_news.append(data[company]['news'][i])
        y_changes.append(data[company]['changes'][i])

    X_commodity.append(best_commodities[company])

X_prices = np.array(X_prices)
X_news = np.array(X_news)
X_commodity = np.array(X_commodity)
X_name = np.array(X_name)

y_changes = np.array(y_changes)

scaler_prices = MinMaxScaler()
X_prices_normalized = scaler_prices.fit_transform(X_prices.reshape(-1, X_prices.shape[-1])).reshape(X_prices.shape)

if len(X_news.shape) < 2:
    X_news = np.expand_dims(X_news, axis=1)

X_news_reshaped = X_news.reshape(X_news.shape[0], X_news.shape[1], 1)

if len(X_prices.shape) < 3:
    X_prices = np.expand_dims(X_prices, axis=2)

X_prices_train, X_prices_test, X_news_train, X_news_test, X_name_train, X_name_test, y_train, y_test = train_test_split(X_prices, X_news_reshaped, X_name, y_changes, test_size=0.2, random_state=42)

def build_model(hp):
    input_prices = Input(shape=(X_prices.shape[1], X_prices.shape[2]))
    input_news = Input(shape=(X_news.shape[1], 1))
    input_name = Input(shape=(1,))

    lstm_prices = LSTM(hp.Int('units_prices', min_value=32, max_value=1024, step=64))(input_prices)
    lstm_news = LSTM(hp.Int('units_news', min_value=32, max_value=1024, step=64))(input_news)
    lstm_name = layers.Flatten()(input_name)    

    concatenated = concatenate([lstm_prices, lstm_news, lstm_name])
    output = Dense(2, activation='linear')(concatenated)

    model = Model(inputs=[input_prices, input_news, input_name], outputs=output)

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
        loss='mse',
        metrics=['mae'])

    return model

tuner = RandomSearch(
    build_model,
    objective='val_mae',                      # The metric that should be optimized
    max_trials=max_trials,                    # The numbers of rounds to test
    executions_per_trial=executions_per_trial,# The number of models that should be tested in each round
    directory='models',                       # The directory where the models should be saved
    project_name=f'stock-predictor{len([name for name in os.listdir('models') if os.path.isdir(os.path.join('models', name))])}'
)

print("\n\nTraining model...")
tuner.search(
    [X_prices_train, X_news_train, X_name_train], 
    y_train,
    epochs=50,
    batch_size=16,
    validation_data=([X_prices_test, X_news_test, X_name_test], y_test),
    verbose=0, # 0 = silent, 1 = progress bar, 2 = one line per epoch
    callbacks=[CustomCallback()],
)

tuner.results_summary()

model = tuner.get_best_models(num_models=1)[0]

model.summary()

#
# TEST
#
