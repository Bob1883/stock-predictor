# from lumibot.brokers import Alpaca
# from lumibot.backtesting import YahooDataBacktesting
# from lumibot.strategies.strategy import Strategy
# from lumibot.traders import Trader
# from datetime import datetime 
# from alpaca_trade_api import REST 
# from timedelta import Timedelta 

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 
from alpaca_trade_api.rest import REST

API_KEY = "PK9618UB7TK7LDWHY5SE" 
API_SECRET = "OaXaMZnLfur2mKLII3K3ktKbaoO3RG2zPfTI1Xco" 
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

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
