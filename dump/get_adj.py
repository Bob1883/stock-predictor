import alpaca_trade_api as tradeapi

# Replace 'your_api_key' and 'your_api_secret' with your Alpaca API key and secret
api_key = 'your_api_key'
api_secret = 'your_api_secret'
base_url = 'https://paper-api.alpaca.markets'  # Use 'https://api.alpaca.markets' for live trading

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Replace 'AAPL' with the stock symbol you're interested in
symbol = 'AAPL'

# Retrieve historical data for adjusted close prices
barset = api.get_barset(symbol, 'day', limit=100)  # Adjust 'limit' as needed
stock_bars = barset[symbol]

for bar in stock_bars:
    print(f"Time: {bar.t} | Adjusted Close: {bar.c}")
