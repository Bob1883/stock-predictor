from constants import *
from preprocessing import *
from load_data import *

# settings
MONEY_TO_INVEST = 0.20 # % that can be invested per day
RISK = 10 # % how risky the investment is

money = 2000 # Dollar 
stocks = [] # List of stocks
data = {} # Dict of stock data

def make_predictions(data, days_from_start):
    # load the best.h5 model
    model = load_model('models/stock-predictor-1/best_model.h5')
    predictions = {} # Dict of predictions

    #  the data is aranged day by day starting from the first date. We only want the first days_from_start days
    for stocks in data: 
        commodity1 = data[stocks]["commodity1"][:days_from_start]
        commodity2 = data[stocks]["commodity2"][:days_from_start]
        commodity3 = data[stocks]["commodity3"][:days_from_start]
        google_trends = data[stocks]["google_trends"][:days_from_start]
        changes = data[stocks]["changes"][:days_from_start]
        temp_change = data[stocks]["temp_change"]
        prices = data[stocks]["prices"][:days_from_start]
        political = data[stocks]["political"][:days_from_start]
        news = data[stocks]["news"][:days_from_start]
        names = data[stocks]["names"][:days_from_start]
        rsi = data[stocks]["rsi"][:days_from_start]
        macd = data[stocks]["macd"][:days_from_start]
        ema_20 = data[stocks]["ema_20"][:days_from_start]
        ema_50 = data[stocks]["ema_50"][:days_from_start]
        ema_200 = data[stocks]["ema_200"][:days_from_start]
        bb_low = data[stocks]["bb_low"][:days_from_start]
        bb_high = data[stocks]["bb_high"][:days_from_start]
        obv = data[stocks]["obv"][:days_from_start]
        debt = data[stocks]["debt"][:days_from_start]
        gdp = data[stocks]["gdp"][:days_from_start]
        inflation = data[stocks]["inflation"][:days_from_start]
        unemployement = data[stocks]["unemployement"][:days_from_start]

        prices = np.array(prices)
        news = np.array(news)
        commodity1 = np.array(commodity1)
        commodity2 = np.array(commodity2)
        commodity3 = np.array(commodity3)
        names = np.array(names)
        rsi = np.array(rsi)
        macd = np.array(macd)
        ema_20 = np.array(ema_20)
        ema_50 = np.array(ema_50)
        ema_200 = np.array(ema_200)
        bb_low = np.array(bb_low)
        bb_high = np.array(bb_high)
        obv = np.array(obv)
        debt = np.array(debt)
        gdp = np.array(gdp)
        inflation = np.array(inflation)
        unemployement = np.array(unemployement)
        changes = np.array(changes)

        # make predictions for the next day
        prediction = model.predict([prices, news, commodity1, commodity2, commodity3, names, rsi, macd, ema_20, ema_50, ema_200, bb_low, bb_high, obv, debt, gdp, inflation, unemployement], verbose=0)
        loader = Load_data(company=stock.lower())
        entire_price_data = loader.load_day_data()["Adj Close"].values[:days_from_start]
        # unscale the prediction using the temp_change data
        unscaled_prediction = prediction[0][0] * (max(temp_change) - min(temp_change)) + min(temp_change)
        # turn the unscaled prediction into a price
        current_price = entire_price_data[-1]
        predicted_price = current_price * (1 + unscaled_prediction / 100)
        predictions[stocks] = {
            "current_price": current_price,
            "predicted_price": predicted_price,
        }

    return predictions
        

for filename in os.listdir('data/data-day'):
    if filename.endswith('.csv'):
        stocks.append(filename.split('.')[0].lower())
# stocks.append("apple")
# stocks.append("tesla")

# Get data from the stock
for stock in stocks:
    # periode should be 2023-10-13 - date years
    commodties, google_trends, changes, prices, political, news, names, rsi, macd, ema_20, ema_50, ema_200, bb_low, bb_high, obv, debt, gdp, inflation, unemployement = preprocessing([stock], test_stock="vinm", periode=periode)
    commodity1, commodity2, commodity3 = [], [], []

    # if data is empty, skip the stock
    if len(commodties) == 0:
        continue

    # so its an array of a few hundred lists, the first list should go in commodity1, the second in commodity2, and the third in commodity3, then the fourth in commodity1 and so on
    for i, commodity in enumerate(commodties):
        if i % 3 == 0:
            for n in range(len(commodity)):
                commodity1.append(commodity[n])
        elif i % 3 == 1:
            for n in range(len(commodity)):
                commodity2.append(commodity[n])
        else:
            for n in range(len(commodity)):
                commodity3.append(commodity[n])

    loader = Load_data(company=stock.lower())
    entire_price_data = loader.load_day_data()

    temp_change = []
    last_date = pd.to_datetime(loader.load_day_data()['Date'].iloc[-1])   

    # the other data is scaled so we need this to scale it back
    for date in range((periode*365)-n_past):
        current_date = last_date - pd.DateOffset(days=((periode*365)-n_past)-date)
        future_date = current_date + pd.DateOffset(days=n_future)
        if future_date > last_date:
            break
        current_price = entire_price_data[entire_price_data["Date"] == current_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
        future_price = entire_price_data[entire_price_data["Date"] == future_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
        if current_price != 0: 
            temp_change.append(round(((future_price / current_price) - 1)*100, 2))
        else: 
            temp_change.append(0)

    data[stock] = {
        "commodity1": commodity1,
        "commodity2": commodity2,
        "commodity3": commodity3,
        "google_trends": google_trends,
        "changes": changes,
        "temp_change": temp_change, 
        "prices": prices,
        "political": political,
        "news": news,
        "names": names,
        "rsi": rsi,
        "macd": macd,
        "ema_20": ema_20,
        "ema_50": ema_50,
        "ema_200": ema_200,
        "bb_low": bb_low,
        "bb_high": bb_high,
        "obv": obv,
        "debt": debt,
        "gdp": gdp,
        "inflation": inflation,
        "unemployement": unemployement
    }

portfolio = {}

day = 20
for i in range((periode*365)-n_past-day):
    print(portfolio)

    predictions = make_predictions(data, day)

    # Take top 5 stocks
    top_stocks = sorted(predictions, key=lambda x: predictions[x]["predicted_price"], reverse=True)[:5]

    for commpany in portfolio: 
        if commpany not in top_stocks:
            loader = Load_data(company=commpany.lower())
            last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
            money += last_price * portfolio[commpany]["amount"]
            print("gain: " + str(last_price * portfolio[commpany]["amount"]))
            portfolio = portfolio.pop(commpany)

    for commpany in top_stocks:
        if predictions[commpany]["predicted_price"] > 0:
            loader = Load_data(company=commpany.lower())
            last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
            amount_to_invest = int(MONEY_TO_INVEST * money /last_price)
            if commpany not in portfolio and last_price*amount_to_invest <= money:
                portfolio[commpany] = {
                    "price": last_price,
                    "amount": amount_to_invest
                }
                money -= last_price*amount_to_invest
                print("invested: " + str(last_price*amount_to_invest))
            elif commpany in portfolio and last_price*amount_to_invest <= money:
                portfolio[commpany]["amount"] += amount_to_invest
                portfolio[commpany]["price"] = last_price

                money -= last_price*amount_to_invest
                print("invested: " + str(last_price*amount_to_invest))
        elif commpany in portfolio:
            loader = Load_data(company=commpany.lower())
            last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
            money += last_price * portfolio[commpany]["amount"]
            print("gain: " + str(last_price * portfolio[commpany]["amount"]))
            portfolio = portfolio.pop(commpany)

    day += 1
    print("\033[91m" + str(money + sum([portfolio[commpany]["amount"] * portfolio[commpany]["price"] for commpany in portfolio])) + "\033[0m")
    print(portfolio)

plt.plot(money)
plt.show()