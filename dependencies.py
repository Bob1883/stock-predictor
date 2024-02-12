from indicators import Indicators   
from load_data import Load_data
from constants import *

encoder = OneHotEncoder(sparse=False)
indicator = Indicators()
loader = Load_data(period=259, company=test_stock) 

def clac_accuracy(y_test, y_pred):
    points = 0
    for i in range(len(y_test)):
        if y_pred[i] != 0:
            distence = y_test[i] / y_pred[i]
            distence = 1 - abs(1 - distence) 

            if distence > 0: 
                points += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
        else:
            distence = abs(y_test[i] - y_pred[i]) 
            distence = 1 - distence

            if distence > 0: 
                points += distence 

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5

    points = points / len(y_test)
    print(points)

def preprocessing(companies, test_stock, exclude=[]):
    data = {}
    indicators = []

    for company in companies:
        if company != test_stock:
            percent = round(((companies.index(company) / len(companies)) * 100) + 1)
            printProgressBar(percent, 100, length = 50)

            loader = Load_data(period=259, company=company.lower())

            company_data = loader.get_raw_data()
            day_data = loader.load_day_data()

            data[company] = {}

            average_change_down = []
            average_change_up = []

            prices = []
            changes = []

            for date in range(len(company_data['Date'])):

                price = []

                current_date = pd.to_datetime(company_data['Date'][date])

                for index in range(n_past):
                    try:
                        past_date = current_date - pd.DateOffset(days=n_past - index)
                        price.append(day_data[day_data['Date'] == past_date]['Adj Close'].values[0].round(2))
                    except Exception as e:
                        if len(price) > 0:
                            price.append(price[-1])
                        else:
                            if len(prices) > 0:
                                price.append(prices[-1][-1])
                            else:
                                price.append(0)
                
                prices.append(price)

            for date in range(len(prices)):
                current_date = pd.to_datetime(company_data['Date'][date])
                future_date = current_date + pd.DateOffset(days=n_future)

                dates = [str(date).split("T")[0] for date in day_data['Date'].values]
                
                if str(future_date).split(" ")[0] in dates:
                    future_price = day_data[day_data['Date'] == future_date]['Adj Close'].values[0]
                    change = ((future_price / prices[date][-1]) - 1)
                    if change < 0:
                        changes.append(-1)
                    else:
                        changes.append(1)
                else:
                    changes.append(0)

                # add indicators, to the same spand 
                indicators.append(indicator.get_indicators(company, (current_date - pd.DateOffset(days=n_past)).strftime('%Y-%m-%d'), current_date.strftime('%Y-%m-%d')))
                    
            data[company]['prices'] = prices
            data[company]['changes'] = changes
            data[company]['news'] = company_data['score'].values.tolist()

    # Remove excluded data types
    for company in data:
        for dtype in exclude:
            if dtype in data[company]:
                del data[company][dtype]

    return data, indicators