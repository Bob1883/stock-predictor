from alpaca_trade_api.rest import REST
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame
import yfinance as yf
from json import loads, dumps
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import pandas as pd
import os 

start_date = datetime(2023, 10, 14) - timedelta(days=365*5)
end_date = datetime(2023, 10, 14)

API_KEY = os.getenv("ALPACA_KEY") 
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"

client = StockHistoricalDataClient(API_KEY, API_SECRET)

symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'LLY', 'UNH', 'V', 'NVO', 'XOM', 'WMT', 'JPM', 'MC.PA', 'JNJ', 'MA', 'AVGO', 'TCEHY', 'PG', '005930.KS', 'CVX', 'NESN.SW', 'ORCL', 'HD', '600519.SS', 'ABBV', 'MRK', 'COST', 'ADBE', 'IHC.AE', 'TM', 'ASML', 'KO', 'SHEL', 'PEP', 'OR.PA', '1398.HK', 'CSCO', 'BAC', 'AZN', 'BABA', 'ROG.SW', 'NVS', 'CRM', 'ACN', 'RELIANCE.NS', 'RMS.PA', '601857.SS', 'MCD', '0941.HK', 'CMCSA', 'LIN', 'TMO', 'PFE', '601288.SS', 'ABT', 'AMD', 'TMUS', 'TTE', 'NKE', 'HSBC', 'DIS', 'NFLX', 'TCS.NS', 'AMGN', 'COP', 'DHR', 'WFC', 'SAP', 'INTC', '601939.SS', 'INTU', 'HDB', '601988.SS', 'PM', 'BHP', 'PDD', 'TXN', 'SNY', 'CAT', 'CDI.PA', 'UPS', 'VZ', 'IBM', 'UNP', 'MS', 'QCOM', 'PRX.AS', 'HON', 'UL', 'BMY', 'AMAT', 'GE', 'BP', 'RY', 'IDEXY']
names = ['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet', 'Amazon', 'NVIDIA', 'Facebook', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson and Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter and Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "LOreal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']

for symbol in symbols:
    try: 
        adj_close = []
        dates = []

        request_params = StockBarsRequest(
                            symbol_or_symbols=symbol,
                            timeframe=TimeFrame.Day,
                            start=start_date,
                            end=end_date,
                        )
        bars = client.get_stock_bars(request_params).df

        # Use yfinance to get splits and dividends data
        yf_ticker = yf.Ticker(symbol)
        yf_splits = yf_ticker.splits
        yf_dividends = yf_ticker.dividends

        # Convert the MultiIndex to a single level index
        bars = bars.reset_index()
        
        bars['timestamp'] = bars['timestamp'].dt.strftime('%Y-%m-%d')  # Adjust Alpaca timestamp format

        #  convert date to datetime
        yf_splits.index = pd.to_datetime(yf_splits.index)
        yf_dividends.index = pd.to_datetime(yf_dividends.index)

        #  convert date to string
        yf_splits.index = yf_splits.index.strftime('%Y-%m-%d')
        yf_dividends.index = yf_dividends.index.strftime('%Y-%m-%d')
        
        print(bars)
        print(yf_splits)
        print(yf_dividends)

        split = 1
        dividend = 0
        for date in bars['timestamp']:
            # use the data from yfinance to adjust the price
            price = 0 
            if date in yf_splits.index:
                split = split * yf_splits[date]
            if date in yf_dividends.index:
                dividend = dividend + yf_dividends[date]
            price = bars[bars['timestamp'] == date]['close'].values[0] * split + dividend
            adj_close.append(price)
            dates.append(date)
        
        print(adj_close)

        difrence = adj_close[-1] / bars['close'].values[-1]
        # devide all the prices by difrence
        adj_close = [i / difrence for i in adj_close]
        print(adj_close)

        # save the data to a file, csv
        df = pd.DataFrame(adj_close, columns=['Adj Close'])
        df['Date'] = dates
        df.to_csv(f"data/data-day/{names[symbols.index(symbol)]}.csv", index=False)
        print(df)
    except Exception as e:
        print(e)
        continue
