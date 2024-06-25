# alpaca imports 
from alpaca.trading.client import TradingClient
from alpaca_trade_api import REST
from keras.models import load_model

# for loading env
from os import getenv
from dotenv import load_dotenv

# extract data
from pandas import read_csv

# webscraping 
from Components.webscraping.historical_data import get_historical_data

################
### Settings ###
################

STOP_LOSS = 0.05      # Stop loss percentage
TAKE_PROFIT = 0.10     # Take profit percentage
DIVERSIFICATION = 5     # Number of stocks to invest in each day
RISK_TOLERANCE = 0.05    # Maximum acceptable risk level
MONEY_TO_INVEST = 0.20    # % that can be invested per day
TRAILING_STOP_LOSS = 0.03  # Trailing stop loss percentage
REBALANCE_THRESHOLD = 0.10  # Portfolio rebalance threshold
CONFIDENCE_THRESHOLD = 0.75  # Minimum confidence level required for investment

####################
### Enitializing ###
####################

# load env vars 
load_dotenv()

ALPACA_KEY = getenv('ALPACA_KEY')
ALPACA_SECRET = getenv('ALPACA_SECRET')
ALPACA_ENDPOINT = getenv('ALPACA_ENDPOINT')

# Getting account info
trading_client = TradingClient(ALPACA_KEY, ALPACA_SECRET)
account = trading_client.get_account()
money = account.cash 
positions = trading_client.get_all_positions()

# Read the CSV file
df = read_csv("assets/S&P_500.csv")
companies = df[["Symbol"]].values.tolist()

###################
### Webscraping ###
###################

# Get historical data 
# TODO save the info 
prices = get_historical_data(["AAPL"], "20d")

# Get commodity data

# Get news data 

# process the data 
model = load_model("assets/model.h5")

# Predict the stock prices
# predictions = model.predict(prices)

# 