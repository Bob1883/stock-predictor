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

def train_model(companies):
    for filename in os.listdir("./data/data-week"):
        company_name = filename.split("-")[0]
        if os.path.isfile(f"data/data-day/{company_name}.csv"):
            companies.append(company_name)

    # companies = companies[:1]
    companies.append(test_stock)

    # Assuming you have your preprocessed data
    X_prices_train, X_news_train, X_names_train, y_train, X_prices_test, X_news_test, X_name_test, y_test = preprocessing(companies, test_stock, periode, exclude=[])

    X_prices_train, X_prices_val, X_news_train, X_news_val, X_name_train, X_name_val, y_train, y_val = train_test_split(X_prices_train, X_news_train, X_names_train, y_train, test_size=0.2, random_state=42)

    def build_model(hp):
        input_prices = Input(shape=(X_prices_train.shape[1],))
        input_news = Input(shape=(1,))
        input_names = Input(shape=(1,))

        lstm_prices = Dense(hp.Int('units_prices', min_value=32, max_value=1024, step=64), activation='relu')(input_prices)
        lstm_news = Dense(hp.Int('units_news', min_value=32, max_value=1024, step=64), activation='relu')(input_news)
        lstm_names = Dense(hp.Int('units_names', min_value=32, max_value=1024, step=64), activation='relu')(input_names)    

        concatenated = concatenate([lstm_prices, lstm_news, lstm_names])
        output = Dense(1, activation='linear')(concatenated)

        model = Model(inputs=[input_prices, input_news, input_names], outputs=output)

        model.compile(
            optimizer=keras.optimizers.Adam(
                hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
            loss='mse',
            metrics=['mae'])

        return model

    # get the number of folders in the models folder
    num_tests = len([name for name in os.listdir('models') if os.path.isdir(f'models/{name}')])

    tuner = RandomSearch(
        build_model,                              # The model-building function
        objective='val_mae',                      # The metric that should be optimized
        max_trials=max_trials,                    # The numbers of rounds to test
        executions_per_trial=executions_per_trial,# The number of models that should be tested in each round
        directory='models',                       # The directory where the models should be saved
        project_name=f'stock-predictor-{num_tests}'
    )

    tuner.search(
        [X_prices_train, X_news_train, y_train], 
        y_train,
        epochs=50,
        batch_size=16,
        validation_data=([X_prices_val, X_news_val, y_val], y_val),
        verbose=0, # 0 = silent, 1 = progress bar, 2 = one line per epoch
        callbacks=[CustomCallback()],
    )

    # tuner.results_summary()

    model = tuner.get_best_models(num_models=1)[0]

    model.summary()

    ########
    # TEST #
    ########
    y_pred = model.predict([X_prices_test, X_news_test, y_test])

    # accuracy = clac_accuracy(y_test, y_pred)[0]
    # print(round(accuracy*100), "%")

    plt.plot(y_test, color = 'red', label = 'Real')
    plt.plot(y_pred, color = 'blue', label = 'Predicted')
    plt.title('Stock Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()