# from constants import *
# from preprocessing import *

# # load AI model
# model = load_model("models/model.h5")

# class Backtesting(Strategy):
#     def initialize(self, symbols):
#         self.symbols = symbols
#         self.cash_at_risk = "0.5"
#         self.api = api

#     def on_trading_iteration(self):
#         for symbol in self.symbols:
#             # super duper advanced strat with AI

#             # get data
#             data = self.api.get_historical_data(symbol, "1D", "5y")
#             data = data.dropna()
#             data.reset_index(drop=True, inplace=True)

#             # get last 20 days
#             data = data.iloc[-20:, :]
#             data.reset_index(drop=True, inplace=True)

#             # get last 3 days
#             last_3_days = data.iloc[-3:, :]
#             last_3_days.reset_index(drop=True, inplace=True)

#             # get last 20 days
#             last_20_days = data.iloc[-20:, :]
#             last_20_days.reset_index(drop=True, inplace=True)

#             # get news data
#             #news_data = get_news_data(symbol, last_3_days['Date'].iloc[-1], last_3_days['Date'].iloc[0])

#             # get commodities
#             #commodity_data = get_commodities_data(last_3_days['Date'].iloc[-1], last_3_days['Date'].iloc[0])

#             # get name
#             #name = get_name(symbol)

#             # get current price
#             current_price = last_3_days['Adj Close'].iloc[-1]

#             # get future price
#             future_price = last_3_days['Adj Close'].iloc[0]

#             # scale data
#             news_data = scaler.fit_transform(np.array(news_data).reshape(-1, 1)).reshape(-1)
#             commodity_data = scaler.fit_transform(np.array(commodity_data).reshape(-1, 1)).reshape(-1)
#             last_20_days = scaler.fit_transform(np.array(last_20_days['Adj Close']).reshape(-1, 1)).reshape(-1)

#             # get prediction
#             prediction = model.predict([last_20_days, news_data, commodity_data])

#             # check if we should buy
#             if prediction > 0.5:
#                 self.api.buy(symbol, self.cash_at_risk)
#                 print(f"Bought {symbol} for {current_price}")

#             # check if we should sell
#             elif prediction < 0.5:
#                 self.api.sell(symbol)
#                 print(f"Sold {symbol} for {current_price}")

# # Define the list of symbols you want to backtest on
# symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB']

# # Initialize the strategy with the list of symbols
# strategy = Backtesting(symbols)

# # Run the backtest
# strategy.backtest(
#     YahooDataBacktesting, 
#     start_date=datetime(2018, 10, 20),
#     end_date=datetime(2023, 10, 10),
# )