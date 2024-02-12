# settings
MONEY_TO_INVEST = 20 # % that can be invested per day
RISK = 10 # % how risky the investment is


date = "2020-05-10"
money = 2000 # Dollar 
stocks = [] # List of stocks
predictions = {} # Dict of predictions

def get_stock_data(stock, date):
    """Get the stock data for the given stock and date."""
    pass

#  def make prebs 
def make_predictions(stock, date):
    """Make predictions for the given stock and date."""
    pass

for stock in stocks:
    stock_data = get_stock_data(stock, date)
    stock_price = stock_data["price"]
    stock_volume = stock_data["volume"]
    stock_news = stock_data["news"]

    make_predictions(stock, date)

    # take the top 5 predictions, based on the percentage change. 
    top_predictions = sorted(predictions[stock][date], key=lambda x: x["percentage_change"])[:5]

    # for each prediction, calculate how much money we should invest in that stock
    for prediction in top_predictions:
        # get the price of the stock the next day
        prediction_date = prediction["date"]
        prediction_stock_data = get_stock_data(stock, prediction_date)
        prediction_stock_price = prediction_stock_data["price"]
        prediction_stock_volume = prediction_stock_data["volume"]
        prediction_stock_news = prediction_stock_data["news"]

        # calculate how much money we should invest in the stock
        prediction["investment"] = money * prediction["percentage_change"] / 100

        # calculate how many shares we should buy
        prediction["shares"] = prediction["investment"] // prediction_stock_price

        # calculate the profit
        prediction["profit"] = prediction["shares"] * (prediction_stock_price - stock_price)

        # calculate the risk
        prediction["risk"] = prediction["shares"] * prediction_stock_price * prediction_stock_volume

    # find the prediction with the highest profit
    best_prediction = max(top_predictions, key=lambda x: x["profit"])

    # invest in that prediction
    money -= best_prediction["investment"]
    print(f"invested {best_prediction['investment']} in {stock}")

    # update the stock price
    stock_price = prediction_stock_price

    # update the date
    date = prediction_date

    # update the predictions
    predictions = {stock: {prediction_date: []}}

    # update the money
    money += best_prediction["profit"]

    print(f"made {best_prediction['profit']} in {stock}")

    # update the stocks
    stocks.append(stock)

    # update the predictions
    make_predictions(stock, date)

    # take the top 5 predictions, based on the percentage change. 
    top_predictions = sorted(predictions[stock][date], key=lambda x: x["percentage_change"])[:5]

    # for each prediction, calculate how much money we should invest in that stock
    for prediction in top_predictions:
        # get the price of the stock the next day
        prediction_date = prediction["date"]
        prediction_stock_data = get_stock_data(stock, prediction_date)
        prediction_stock_price = prediction_stock_data["price"]
        prediction_stock_volume = prediction_stock_data["volume"]
        prediction_stock_news = prediction_stock_data["news"]

        # calculate how much money we should invest in the stock
        prediction["investment"] = money * prediction["percentage_change"] / 100

        # calculate how many shares we should buy
        prediction["shares"] = prediction["investment"] // prediction_stock_price

        # calculate the profit
        prediction["profit"] = prediction["shares"] * (prediction_stock_price - stock_price)

        # calculate the risk
        prediction["risk"] = prediction["shares"] * prediction_stock_price * prediction_stock_volume

    
