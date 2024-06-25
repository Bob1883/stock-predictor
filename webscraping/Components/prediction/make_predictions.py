from keras.models import Model
from numpy import array as np_array

def make_predictions(data: dict, model: Model) -> dict:
    """
    Make predictions for the data.
    data: Data to make the predictions for.
    model: Model to make the predictions with.
    """
    predictions = {}

    for stocks in data:
        predictions[stocks] = {}

        # load the data
        commodity = data[stocks]["commodity"]
        prices = data[stocks]["prices"]
        news = data[stocks]["news"]
        names = data[stocks]["names"]
        rsi = data[stocks]["rsi"]
        macd = data[stocks]["macd"]
        obv = data[stocks]["obv"]

        prices = np_array(prices)
        news = np_array(news)
        commodity = np_array(commodity)
        names = np_array(names)
        rsi = np_array(rsi)
        macd = np_array(macd)
        obv = np_array(obv)

        # TODO: make the predictions, and how much money its going to go up or down. 

    return predictions