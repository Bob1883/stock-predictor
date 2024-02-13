from indicators import Indicators   
from load_data import Load_data
from constants import *

indicator = Indicators()

def preprocessing(companies, test_stock, periode, exclude=[]): 
    indicators = []
    commodties = []
    changes = []
    prices = []
    news = []
    names = []

    test_indicators = []
    test_commodties = []
    test_changes = []
    test_prices = []
    test_news = []
    test_names = []

    # companies.append(test_stock)
    company_to_int = {company: i for i, company in enumerate(companies)}

    commodity_prices = {}

    for commodity in os.listdir("data/commodity"):
        with open(f"data/commodity/{commodity}") as f:
            data = json.load(f)

        commodity = commodity.split(".")[0]
        commodity_prices[commodity] = {}

        num_days = len(pd.date_range(data["series"][0]["data"][0]["date"], data["series"][0]["data"][-1]["date"], freq='D')) + 5
        current_date = datetime.datetime.strptime(data["series"][0]["data"][0]["date"], '%Y-%m-%dT%H:%M:%S')
        for day in range(num_days): 
            if current_date.strftime('%Y-%m-%dT%H:%M:%S') in [data["series"][0]["data"][i]["date"] for i in range(len(data["series"][0]["data"]))]:
                index = [data["series"][0]["data"][i]["date"] for i in range(len(data["series"][0]["data"]))].index(current_date.strftime('%Y-%m-%dT%H:%M:%S'))
                commodity_prices[commodity][current_date.strftime('%Y-%m-%dT%H:%M:%S')] = data["series"][0]["data"][index]["y"]
            else: 
                commodity_prices[commodity][current_date.strftime('%Y-%m-%dT%H:%M:%S')] = commodity_prices[commodity][(current_date - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')]
            current_date = current_date + datetime.timedelta(days=1)

    for company in companies:
        indicator_data = []
        commodity_data = [[], [], []]
        changes_data = [] 
        price_data = []
        name_data = []
        news_data = []

        average_change_down = []
        average_change_up = []

        entire_price_data = {}
        best_commodities = []

        name = company_to_int[company]

        iteration = ((companies.index(company) / len(companies) + 1) * 100) 
        printProgressBar(iteration, 100, length = 50, description="Loading data...")

        loader = Load_data(period=periode, company=company.lower())
        company_data = loader.get_raw_data()
        day_data = loader.load_day_data()

        num_days = len(pd.date_range(day_data['Date'].iloc[0], day_data['Date'].iloc[-1], freq='D'))
        current_date = pd.to_datetime(day_data['Date'].iloc[0])

        for day in range(num_days): 
            if current_date in day_data['Date'].values:
                entire_price_data[current_date] = day_data[day_data['Date'] == current_date]['Adj Close'].values[0]
            else:
                entire_price_data[current_date] = entire_price_data[current_date - pd.DateOffset(days=1)]

            current_date = current_date + pd.DateOffset(days=1)
        
        diffs = {}
        for commodity in commodity_prices:
            commodity_price = [commodity_prices[commodity][date] for date in commodity_prices[commodity]]

            if len(commodity_price) != len(entire_price_data):
                commodity_price = commodity_price[:len(entire_price_data)]

            commodity_price = scaler.fit_transform(np.array(commodity_price).reshape(-1, 1)).reshape(-1)
            company_price = scaler.transform(np.array([entire_price_data[date] for date in entire_price_data]).reshape(-1, 1)).reshape(-1)

            diff = 0
            for i in range(len(commodity_price)):
                diff += abs(commodity_price[i] - company_price[i])

            diffs[commodity] = diff
        
        best_commodities = sorted(diffs, key=diffs.get)[:3]

        for date in range(len(company_data['Date'])):
            price = []
            current_date = pd.to_datetime(company_data['Date'][date])
            future_date = current_date + pd.DateOffset(days=n_future)

            for index in range(n_past):
                try: 
                    past_date = current_date - pd.DateOffset(days=n_past - index)
                    price.append(entire_price_data[past_date])
                except: 
                    price.append(0)

            price_data.append(price)

            # change 
            current_price = entire_price_data[current_date]
            future_price = entire_price_data[future_date]
            if current_price != 0: 
                changes_data.append(round(((future_price / current_price) - 1)*100, 2))
            else: 
                changes_data.append(0)

            # indicators
            # indicator_data.append(indicator.get_indicators(company_data, start_date=current_date - pd.DateOffset(days=n_past), end_date=current_date))
            
            # name
            name_data.append(name)

            # commodity
            for commodity in best_commodities:
                index = best_commodities.index(commodity)
                commodity_data[index].append(commodity_prices[commodity][current_date.strftime('%Y-%m-%dT%H:%M:%S')])

            # news get from company_data
            news_data.append(company_data['score'][date])

        if company == test_stock:
            test_indicators = indicator_data
            test_commodties = commodity_data
            test_changes = changes_data
            test_prices = price_data
            test_news = news_data
            test_names = name_data
        else:
            indicators.append(indicator_data)
            commodties.append(commodity_data)
            changes.append(changes_data)
            prices.append(price_data)
            news.append(news_data)
            names.append(name_data)

    def preprocess_data(prices, news, commodity, name, changes):
        x_prices = np.array(prices)
        x_news = np.array(news)
        x_commodity = np.array(commodity)
        x_name = np.array(name)

        y_changes = np.array(changes)

        # Normalize the prices
        x_prices_normalized = scaler.fit_transform(x_prices.reshape(-1, x_prices.shape[-1])).reshape(x_prices.shape)

        # Reshape the news
        if len(x_news.shape) < 2:
            x_news = np.expand_dims(x_news, axis=1)

        x_news_reshaped = x_news.reshape(x_news.shape[0], x_news.shape[1], 1)

        # Reshape the commodity
        if len(x_commodity.shape) < 3:
            x_commodity = np.expand_dims(x_commodity, axis=2)

        x_commodity_reshaped = x_commodity.reshape(x_commodity.shape[0], x_commodity.shape[1], x_commodity.shape[2], 1)

        return x_prices_normalized, x_news_reshaped, x_commodity_reshaped, x_name, y_changes

    x_prices_normalized, x_news_reshaped, x_commodity_reshaped, x_name, y_changes = preprocess_data(prices, news, commodties, name, changes)
    test_x_prices_normalized, test_x_news_reshaped, test_x_commodity_reshaped, test_x_name, test_y_changes = preprocess_data(test_prices, test_news, test_commodties, test_names, test_changes)

    return x_prices_normalized, x_news_reshaped, x_commodity_reshaped, x_name, y_changes, test_x_prices_normalized, test_x_news_reshaped, test_x_commodity_reshaped, test_x_name, test_y_changes