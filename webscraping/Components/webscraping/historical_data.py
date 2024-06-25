from yfinance import download

def get_historical_data(symbols:list, period:str) -> dict:
    """
    Get the historical data for a list of symbols.
    symbols: List of symbols (e.g., ["AAPL", "MSFT"])
    period: Period for the historical data (e.g., "20d" for 20 days)
    """
    prices = {}
    for symbol in symbols:
        prices[symbol] = {}
        data = download(symbol, period=period, interval="1d")

        if len(data) > 0:
            prices[symbol]["Open"] = data["Open"].tolist()
            prices[symbol]["High"] = data["High"].tolist()
            prices[symbol]["Low"] = data["Low"].tolist()
            prices[symbol]["Close"] = data["Adj Close"].tolist()
            prices[symbol]["Volume"] = data["Volume"].tolist()

        else:
            prices[symbol]["Open"] = []
            prices[symbol]["High"] = []
            prices[symbol]["Low"] = []
            prices[symbol]["Close"] = []
            prices[symbol]["Volume"] = []

    return prices