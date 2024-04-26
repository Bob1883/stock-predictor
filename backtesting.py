from constants import *
from preprocessing import *
from load_data import *
import plotly.graph_objects as go
import random
import math

file_name = input("Enter the file name: ")

# settings
MONEY_TO_INVEST = 0.20  # % that can be invested per day
RISK_TOLERANCE = 0.05  # Maximum acceptable risk level
DIVERSIFICATION = 5  # Number of stocks to invest in each day
STOP_LOSS = 0.05  # Stop loss percentage
TAKE_PROFIT = 0.10  # Take profit percentage
CONFIDENCE_THRESHOLD = 0.75  # Minimum confidence level required for investment
TRAILING_STOP_LOSS = 0.03  # Trailing stop loss percentage
REBALANCE_THRESHOLD = 0.10  # Portfolio rebalance threshold

money = 2000  # Dollar
day = 20  # Day
money_graph = []  # List of money per day
stocks = []  # List of stocks
portfolio = {}  # Dict of stocks in portfolio
data = {}  # Dict of stock data

def make_predictions(data):
    model = load_model('models/test_1-2_xprice_ychange/best_model.h5')
    predictions = {}
    for stocks in data:
        commodity1 = data[stocks]["commodity1"]
        commodity2 = data[stocks]["commodity2"]
        commodity3 = data[stocks]["commodity3"]
        google_trends = data[stocks]["google_trends"]
        changes = data[stocks]["changes"]
        temp_change = data[stocks]["temp_change"]
        prices = data[stocks]["prices"]
        political = data[stocks]["political"]
        news = data[stocks]["news"]
        names = data[stocks]["names"]
        rsi = data[stocks]["rsi"]
        macd = data[stocks]["macd"]
        ema_20 = data[stocks]["ema_20"]
        ema_50 = data[stocks]["ema_50"]
        ema_200 = data[stocks]["ema_200"]
        bb_low = data[stocks]["bb_low"]
        bb_high = data[stocks]["bb_high"]
        obv = data[stocks]["obv"]
        debt = data[stocks]["debt"]
        gdp = data[stocks]["gdp"]
        inflation = data[stocks]["inflation"]
        unemployement = data[stocks]["unemployement"]
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
        prediction = model.predict([prices], verbose=0)
        loader = Load_data(company=stock.lower())
        current_prices = loader.load_day_data()["Adj Close"].values
        max_temp_change = max(temp_change)
        min_temp_change = min(temp_change)
        predicted_price = [0] * len(prediction)
        for i in range(len(prediction)):
            current_price = current_prices[i]
            if not math.isnan(current_price) and current_price != 0:
                unscaled_prediction = prediction[i][0] * (max_temp_change - min_temp_change) + min_temp_change
                predicted_price[i] = (current_price * unscaled_prediction) - current_price
        predictions[stocks] = {
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
        try:
            current_price = entire_price_data[entire_price_data["Date"] == current_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
            future_price = entire_price_data[entire_price_data["Date"] == future_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
            if current_price != 0:
                temp_change.append(round(((future_price / current_price) - 1)*100, 2))
            else:
                temp_change.append(0)
        except IndexError:
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

# load state
if os.path.exists(f"back_test/{file_name}.json"):
    with open(f"back_test/{file_name}.json", "r") as f:
        state = json.loads(f.read())
        day = state["day"]
        money = state["money"]
        portfolio = state["portfolio"]
        money_graph = state["money_graph"]

predictions = make_predictions(data)

for i in range((periode*365)-n_past-day):
    # Find the top stocks for each day based on predicted price, risk, and confidence
    print(money)
    top_stocks = []
    for company in predictions:
        predicted_price = predictions[company]["predicted_price"][i]
        risk_factor = 1 - (RISK_TOLERANCE / 100)
        adjusted_price = predicted_price * risk_factor
        top_stocks.append((company, adjusted_price))
   
    top_stocks.sort(key=lambda x: x[1], reverse=True)
    top_stocks = top_stocks[:DIVERSIFICATION]
   
    new_portfolio = {}
    for company in portfolio:
        loader = Load_data(company=company.lower())
        try:
            last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
            if not math.isnan(last_price):
                # Check stop loss, take profit, and trailing stop loss conditions
                if last_price <= portfolio[company]["price"] * (1 - STOP_LOSS):
                    money += last_price * portfolio[company]["amount"]
                    print(f"Stop loss triggered for {company}. Sold at {last_price}")
                elif last_price >= portfolio[company]["price"] * (1 + TAKE_PROFIT):
                    money += last_price * portfolio[company]["amount"]
                    print(f"Take profit triggered for {company}. Sold at {last_price}")
                elif last_price <= portfolio[company]["trailing_stop"]:
                    money += last_price * portfolio[company]["amount"]
                    print(f"Trailing stop loss triggered for {company}. Sold at {last_price}")
                else:
                    new_portfolio[company] = portfolio[company]
                    new_portfolio[company]["trailing_stop"] = max(portfolio[company]["trailing_stop"], last_price * (1 - TRAILING_STOP_LOSS))
        except IndexError:
            continue
   
    portfolio = new_portfolio
    print(money)
   
    # Rebalance portfolio if necessary
    portfolio_value = sum([portfolio[company]["amount"] * portfolio[company]["price"] for company in portfolio])
    if portfolio_value > 0:
        for company in portfolio:
            current_weight = portfolio[company]["amount"] * portfolio[company]["price"] / portfolio_value
            target_weight = 1 / len(portfolio)
            if abs(current_weight - target_weight) > REBALANCE_THRESHOLD:
                # Rebalance by selling or buying shares
                loader = Load_data(company=company.lower())
                try:
                    last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
                    if not math.isnan(last_price):
                        target_value = portfolio_value * target_weight
                        target_amount = target_value / last_price
                        if target_amount < portfolio[company]["amount"]:
                            sell_amount = portfolio[company]["amount"] - target_amount
                            money += sell_amount * last_price
                            portfolio[company]["amount"] = target_amount
                            print(f"Rebalanced portfolio by selling {sell_amount} shares of {company}")
                        else:
                            buy_amount = target_amount - portfolio[company]["amount"]
                            if buy_amount * last_price <= money:
                                money -= buy_amount * last_price
                                portfolio[company]["amount"] = target_amount
                                print(f"Rebalanced portfolio by buying {buy_amount} shares of {company}")
                except IndexError:
                    continue
    print(money)
   
    for company, predicted_price in top_stocks:
        if predicted_price > 0:
            loader = Load_data(company=company.lower())
            try:
                last_price = loader.load_day_data()["Adj Close"].values[:day][-1]
                if not math.isnan(last_price) and last_price != 0:
                    amount_to_invest = int(MONEY_TO_INVEST * money / last_price)
                    if company not in portfolio and last_price * amount_to_invest <= money:
                        portfolio[company] = {
                            "price": last_price,
                            "amount": amount_to_invest,
                            "trailing_stop": last_price * (1 - TRAILING_STOP_LOSS)
                        }
                        money -= last_price * amount_to_invest
                        print(f"Invested {last_price * amount_to_invest} in {company}")
                    elif company in portfolio and last_price * amount_to_invest <= money:
                        portfolio[company]["amount"] += amount_to_invest
                        if portfolio[company]["amount"] != 0:
                            portfolio[company]["price"] = (portfolio[company]["price"] * portfolio[company]["amount"] + last_price * amount_to_invest) / (portfolio[company]["amount"] + amount_to_invest)
                        money -= last_price * amount_to_invest
                        print(f"Invested additional {last_price * amount_to_invest} in {company}")
            except IndexError:
                continue
   
    day += 1
    total_value = money + sum([portfolio[company]["amount"] * portfolio[company]["price"] for company in portfolio])
    print("\033[91m" + str(total_value) + "\033[0m")
    money_graph.append(total_value)
   
    # save state
    if os.path.exists(f"back_test/{file_name}.json"):
        with open(f"back_test/{file_name}.json", "w") as f:
            f.write(json.dumps({
                "day": day,
                "money": money,
                "portfolio": portfolio,
                "money_graph": money_graph
            }))
    else:
        with open(f"back_test/{file_name}.json", "x") as f:
            f.write(json.dumps({
                "day": day,
                "money": money,
                "portfolio": portfolio,
                "money_graph": money_graph
            }))

fig = go.Figure(data=go.Scatter(y=money_graph))
fig.show()