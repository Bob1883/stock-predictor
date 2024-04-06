from indicators import Indicators   
from load_data import Load_data
from constants import *

indicator = Indicators()

# TODO: add google trends
# TODO: add indicators
# TODO: add world data
# TODO: add political data

def preprocessing(companies:list, test_stock:str, periode:int, exclude:list=[]): 
    """
    This function preprocesses the data for the model.
    companies: list - list of companies
    test_stock: str - test stock
    periode: int - periode
    exclude: list - list of companies to exclude
    (indicators, g_trends, commodties, changes, prices, news, names) 
    """

    # indicators = []
    # world = []
    commodties = []
    g_trends = []
    changes = []
    prices = []
    news = []
    names = []

    # test_indicators = []
    # test_world = []
    test_commodties = []
    test_g_trends = []
    test_changes = []
    test_prices = []
    test_news = []
    test_names = []

    company_to_int = {company: i for i, company in enumerate(companies)}
    
    commodity_prices = Load_data("tesla").load_commodities()

    for company in companies:
        try:
            printProgressBar(companies.index(company), len(companies), description=f"Preprocessing {company}" )
            loader = Load_data(company=company.lower())

            # indicator_data = []
            best_commodities = []
            commodity_data = [[], [], []]
            changes_data = [] 
            price_data = []
            news_data = []
            name_data = []

            name = company_to_int[company]

            #  get best commodities
            diffs = {}  # Store differences for each commodity
            entire_price_data = loader.load_day_data()["Adj Close"].values

            for commodity in commodity_prices:
                if commodity not in "Date": 
                    commodity_price = []
                    for n in range(len(commodity_prices[commodity])):
                        commodity_price.append(str(commodity_prices[commodity][n]))  # Convert 'Timestamp' object to string

                    # Ensure lengths are consistent:
                    if len(commodity_price) > len(entire_price_data):
                        commodity_price = commodity_price[:len(entire_price_data)]  # Trim if necessary

                    # Scaling (consider appropriateness for your use case)
                    commodity_price = scaler.fit_transform(np.array(commodity_price).reshape(-1, 1)).reshape(-1)
                    company_price = scaler.transform(np.array(entire_price_data).reshape(-1, 1)).reshape(-1)

                    if len(commodity_price) != len(company_price):
                        company_price = company_price[:len(commodity_price)]  # Trim if necessary
                    
                    diff = np.sqrt(np.mean((commodity_price - company_price) ** 2))  # Option 5: Root mean squared error

                    diffs[commodity] = diff 

            best_commodities = sorted(diffs, key=diffs.get)[:3]  # Get the 3 best commodities

            last_date = pd.to_datetime(loader.load_day_data()['Date'].iloc[-1])   

            temp_news_data = loader.load_news()
            # loade price data
            entire_price_data = loader.load_day_data()

            for date in range((periode*365)-n_past):
                current_date = last_date - pd.DateOffset(days=((periode*365)-n_past)-date)
                future_date = current_date + pd.DateOffset(days=n_future)

                # lave the last three days, so we can predict the future
                if future_date > last_date:
                    break

                # Price data
                price = []

                for index in range(n_past):
                        past_date = current_date - pd.DateOffset(days=n_past - index)
                        price.append(entire_price_data.loc[entire_price_data["Date"] == past_date.strftime('%Y-%m-%d'), "Adj Close"].values[0])

                price_data.append(price)

                # Changes data
                current_price = entire_price_data[entire_price_data["Date"] == current_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
                future_price = entire_price_data[entire_price_data["Date"] == future_date.strftime('%Y-%m-%d')]["Adj Close"].values[0]
                if current_price != 0: 
                    changes_data.append(round(((future_price / current_price) - 1)*100, 2))
                else: 
                    changes_data.append(0)

                # name data
                name_data.append(name)

                # commodity data
                for commodity in best_commodities:
                    # find the price on the current date by using boolean indexing
                    price = commodity_prices.loc[commodity_prices["Date"] == current_date.strftime('%Y-%m-%d'), commodity].values[0]
                    # append the price to the corresponding commodity data
                    commodity_data[best_commodities.index(commodity)].append(price)

                # news data   
                news_data.append(temp_news_data[temp_news_data["Date"] == current_date.strftime('%Y-%m-%d')]["Score"].values[0])
    

            price_data = scaler.fit_transform(price_data).tolist()
            news_data = scaler.fit_transform(np.array(news_data).reshape(-1, 1)).flatten().tolist()
            commodity_data[0] = scaler.fit_transform(np.array(commodity_data[0]).reshape(-1, 1)).flatten().tolist()
            commodity_data[1] = scaler.fit_transform(np.array(commodity_data[1]).reshape(-1, 1)).flatten().tolist()
            commodity_data[2] = scaler.fit_transform(np.array(commodity_data[2]).reshape(-1, 1)).flatten().tolist()
            # name_data = scaler.fit_transform(np.array(name_data).reshape(-1, 1)).flatten().tolist()
            changes_data = scaler.fit_transform(np.array(changes_data).reshape(-1, 1)).flatten().tolist()

            if company == test_stock:
                for i in range(len(price_data)):
                    test_prices.append(price_data[i])
                    test_news.append(news_data[i])
                    test_commodties.append([commodity_data[0][i], commodity_data[1][i], commodity_data[2][i]])
                    test_names.append(name_data[i])
                    test_changes.append(changes_data[i])
                test_commodties.append(commodity_data[0])
                test_commodties.append(commodity_data[1])
                test_commodties.append(commodity_data[2])
            else:
                for i in range(len(price_data)):
                    prices.append(price_data[i])
                    news.append(news_data[i])
                    names.append(name_data[i])
                    changes.append(changes_data[i])
                commodties.append(commodity_data[0])
                commodties.append(commodity_data[1])
                commodties.append(commodity_data[2])

        except Exception as e:
            print("\033[91m" + f"Failed to preprocess {company}" + "\033[0m")
            time.sleep(1)
            
    return commodties, g_trends, changes, prices, news, names