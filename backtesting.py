from constants import *
from load_data import Load_data 

#  TODO 
#  1. Create data pipeline for testing and future data
#  2. Create backtesting strategy

class Backtesting(Strategy):
    def initialize(self):
        self.sleeptime = "24H" 
        self.cash_at_risk = "0.5"
        self.api = api

    def on_trading_iteration(self):
        pass 


strategy = Backtesting()

strategy.backtest(
    YahooDataBacktesting, 
    start_date=datetime(2018, 10, 20),
    end_date=datetime(2023, 10, 10),
)