from indicators import Indicators   
from load_data import Load_data
from constants import *

indicator = Indicators()

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
        loader = Load_data(company=company.lower())

        # indicator_data = []
        best_commodities = []
        changes_data = [] 
        price_data = []
        news_data = []

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
                
                # Calculate difference (Several options here)
                # diff2 = np.abs(commodity_price - company_price).sum()  # Option 1: Sum of absolute differences
                # # diff1 = np.corrcoef(commodity_price, company_price)[0, 1]  # Option 2: Correlation coefficient
                # diff3 = np.mean(np.abs(commodity_price - company_price))  # Option 3: Mean of absolute differences
                # diff4 = np.mean((commodity_price - company_price) ** 2)  # Option 4: Mean of squared differences
                diff = np.sqrt(np.mean((commodity_price - company_price) ** 2))  # Option 5: Root mean squared error

                diffs[commodity] = diff 

        best_commodities = sorted(diffs, key=diffs.get)[:3]  # Get the 3 best commodities
        # print(sorted(diffs4, key=diffs4.get)[:3])

        last_date = pd.to_datetime(loader.load_day_data()['Date'].iloc[0])   
        for date in range(periode*365):
            current_date = last_date - pd.DateOffset(days=(periode*365)-date)
            future_date = current_date + pd.DateOffset(days=n_future)

            price = []

            for index in range(n_past):
                    past_date = current_date - pd.DateOffset(days=n_past - index)
                    price.append(entire_price_data[past_date])

                    print(price)

            price_data.append(price)

        print(price_data)

data = preprocessing(["pfizer"], "apple", 7)