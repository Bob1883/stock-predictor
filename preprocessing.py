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
        try:
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

            iteration = (((companies.index(company)+1) / len(companies)) * 100) 
            printProgressBar(iteration, 100, length = 50, description="Loading data...")

            loader = Load_data(period=periode, company=company.lower())
            company_data = loader.get_raw_data()
            day_data = loader.load_day_data()

            num_days = len(pd.date_range(day_data['Date'].iloc[0], day_data['Date'].iloc[-1], freq='D')) + n_future
            current_date = pd.to_datetime(day_data['Date'].iloc[0])

            for day in range(num_days): 
                if current_date in day_data['Date'].values:
                    entire_price_data[current_date] = round(day_data[day_data['Date'] == current_date]['Adj Close'].values[0], 2)
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
                for i in range(len(price_data)):
                    # test_indicators.append(indicator_data[i])
                    test_prices.append(price_data[i])
                    test_news.append(news_data[i])
                    test_commodties.append([commodity_data[0][i], commodity_data[1][i], commodity_data[2][i]])
                    test_names.append(name_data[i])
                    test_changes.append(changes_data[i])
            else:
                for i in range(len(price_data)):
                    # indicators.append(indicator_data[i])
                    prices.append(price_data[i])
                    news.append(news_data[i])
                    commodties.append([commodity_data[0][i], commodity_data[1][i], commodity_data[2][i]])
                    names.append(name_data[i])
                    changes.append(changes_data[i])
        except Exception as e:
            print(e)
            print(f"Failed to load {company}")
            time.sleep(1)

    # normalize the data
    scaled_prices = np.array(prices)
    scaled_news = np.array(news)
    scaled_names = np.array(names)
    scaled_changes = np.array(changes)

    test_scaled_prices = np.array(test_prices)
    test_scaled_news = np.array(test_news)
    test_scaled_names = np.array(test_names)
    test_scaled_changes = np.array(test_changes)

    # scale 
    # scaled_prices = scaler.fit_transform(scaled_prices)
    # scaled_news = scaler.fit_transform(scaled_news)
    # scaled_names = scaler.fit_transform(scaled_names)
    # scaled_changes = scaler.fit_transform(scaled_changes)

    # test_scaled_prices = scaler.fit_transform(test_scaled_prices)
    # test_scaled_news = scaler.fit_transform(test_scaled_news)
    # test_scaled_names = scaler.fit_transform(test_scaled_names)
    # test_scaled_changes = scaler.fit_transform(test_scaled_changes)

    return scaled_prices, scaled_news, scaled_names, scaled_changes, test_scaled_prices, test_scaled_news, test_scaled_names, test_scaled_changes