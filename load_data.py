from constants import *
import datetime

class Load_data(): 

    def __init__(self, period = 1, company = "tesla"):
        self.period = period
        self.company = company

        self.historical_data = []
        self.day_data = []
        self.news_data = []
        self.google_trends_data = []

    def load_google_trends(self):
        for filename in os.listdir("data/google-trends"):
            if filename.endswith(".json") and filename.split("-")[0].lower() == self.company:
                with open(f"data/google-trends/{filename}") as f:
                    json_data = json.load(f)
                    scores = []
                    dates = []
                    for i in range(len(json_data)):
                        dates.append(json_data[i][0])
                        scores.append(json_data[i][1])

                    self.google_trends_data = pd.DataFrame(scores, columns=['score'])

                    # add dates to dataframe
                    self.google_trends_data['Date'] = dates
                    self.google_trends_data['Date'] = pd.to_datetime(self.google_trends_data['Date'])

                    self.google_trends_data.reset_index(drop=True, inplace=True)
                    self.google_trends_data = self.google_trends_data.iloc[-self.period:, :]
                    self.google_trends_data.reset_index(drop=True, inplace=True)

        return self.google_trends_data

    def load_political_data(self):
        for filename in os.listdir("data/political"):
            if filename.endswith(".json") and filename.split("-")[0].lower() == self.company:
                with open(f"data/political/{filename}") as f:
                    json_data = json.load(f)["data"] 
                    scores = []
                    dates = []

                    for i in range(len(json_data)):
                        dates.append(json_data[i][0])
                        scores.append(json_data[i][1])
                    
                    self.political_data = pd.DataFrame(scores, columns=['score'])

                    # add dates to dataframe
                    self.political_data['Date'] = dates
                    self.political_data['Date'] = pd.to_datetime(self.political_data['Date'])

                    self.political_data.reset_index(drop=True, inplace=True)
                    self.political_data = self.political_data.iloc[::-1]
                    self.political_data = self.political_data.iloc[-(self.period+14):, :]
                    self.political_data.reset_index(drop=True, inplace=True)

        return self.political_data

    def load_world_data(self):  
        for filename in os.listdir("data/data-world"):
            if filename.endswith(".xls"):
                df = pd.read_excel(f"data/data-world/{filename}")
                df = df.iloc[1]
                df = df[2:]
                df = df.values.tolist()
                df = df[:-5]
                df = df[-6:]
                week_data = []
                for i in range(12):
                    week_data.append(df[0])
                for i in range(1, len(df)-1):
                    for j in range(52):
                        week_data.append(df[i])
                for i in range(41):
                    week_data.append(df[-1])
                if len(week_data) > self.period:
                    week_data = week_data[len(week_data) - self.period:]
                self.world_economy_data.append(pd.DataFrame(week_data, columns=[filename.split(".")[0]]))

        return self.world_economy_data 

    def load_fundemental_data(self):
        pass 

    def find_best_commodity(self, companies): 
        commodity_data = {}
        best_commodies = {}

        for commodity in os.listdir("data/commodity"):
            # open json file
            with open(f"data/commodity/{commodity}") as f:
                data = json.load(f)

            commodity_data[commodity] = []

            for i in range(len(data["series"][0]["data"])): 
                commodity_data[commodity].append(data["series"][0]["data"][i]["y"])

            # there are missing values in the data, there are 7 day intervals. If a value is missing, take the average of the previous and next value
            start_date = datetime.datetime.strptime(data["series"][0]["data"][0]["date"], '%Y-%m-%dT%H:%M:%S')
            date = start_date
            for i in range(len(data["series"][0]["data"])):
                if data["series"][0]["data"][i]["date"] != date.strftime('%Y-%m-%dT%H:%M:%S'):
                    commodity_data[commodity].insert(i, (commodity_data[commodity][i-1] + commodity_data[commodity][i]) / 2)
                date = date + datetime.timedelta(days=7)

            # keep only self.period values
            commodity_data[commodity] = commodity_data[commodity][-self.period:]

        for company in companies:
            # loading bar 
            percent = round(((companies.index(company) / len(companies)) * 100) + 1)
            printProgressBar(percent, 100, length = 50, description="Finding best commodities...")

            df = pd.read_csv(f"data/data-day/{company}.csv")
            df = df.dropna()
            data = df.copy()

            prices = data['Adj Close'].values   

            prices = [np.mean(prices[i:i+30]) for i in range(0, len(prices), 30)]

            best_commodies[company] = {}
            diffs = {}

            for commodity in commodity_data:    
                for commodity in commodity_data:
                    commodity_prices = commodity_data[commodity]

                    # make sure the price data is the same length
                    if len(prices) > len(commodity_prices):
                        prices = prices[:len(commodity_prices)]
                    else:
                        commodity_prices = commodity_prices[:len(prices)]

                    # scale the prices
                    scaler = MinMaxScaler()
                    prices_scaled = scaler.fit_transform(np.array(prices).reshape(-1, 1)).flatten()
                    commodity_prices_scaled = scaler.transform(np.array(commodity_prices).reshape(-1, 1)).flatten()

                    # scale the prices
                    scaler = MinMaxScaler()
                    prices_scaled = scaler.fit_transform(np.array(prices).reshape(-1, 1)).flatten()
                    commodity_prices_scaled = scaler.transform(np.array(commodity_prices).reshape(-1, 1)).flatten()

                    # calculate the diff
                    diff = 0
                    for i in range(len(prices_scaled)):
                        diff += abs(prices_scaled[i] - commodity_prices_scaled[i])

                    diffs[commodity] = diff
                
            best_commodies[company] = sorted(diffs, key=diffs.get)[:3]
 
            for commodity in range(len(best_commodies[company])):
                best_commodies[company][commodity] = commodity_data[best_commodies[company][commodity]] 

        return best_commodies

    def load_historical(self): 
        for filename in os.listdir("data/data-week"):
            if filename.endswith(".csv") and filename.split("-")[0].lower() == self.company:
                df = pd.read_csv(f"data/data-week/{filename}")
                prices = []
                dates = []
                for date in df['Date']:
                    prices.append(df[df['Date'] == date]['Adj Close'].values[0])

                    # take dattes and subtract with 2 days
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    date = date + datetime.timedelta(days=4)
                    date = date.strftime('%Y-%m-%d')
                    dates.append(date)
                
                self.historical_data = pd.DataFrame(prices, columns=['Adj Close'])
                # add dates to dataframe
                self.historical_data['Date'] = dates
                self.historical_data['Date'] = pd.to_datetime(self.historical_data['Date'])


                self.historical_data.reset_index(drop=True, inplace=True)
                # remove the last self.period amount of rows
                self.historical_data = self.historical_data.iloc[-self.period:, :]
                self.historical_data.reset_index(drop=True, inplace=True)

        return self.historical_data 

    def load_day_data(self):
        for filename in os.listdir("data/data-day"):
            if filename.endswith(".csv") and filename.split(".")[0].lower() == self.company:
                df = pd.read_csv(f"data/data-day/{filename}")
                prices = []
                dates = []
                for date in df['Date']:
                    prices.append(df[df['Date'] == date]['Adj Close'].values[0])
                    dates.append(date)
                
                self.day_data = pd.DataFrame(prices, columns=['Adj Close'])
                # add dates to dataframe
                self.day_data['Date'] = dates
                self.day_data['Date'] = pd.to_datetime(self.day_data['Date'])

                self.day_data.reset_index(drop=True, inplace=True)

        return self.day_data 
    
    def load_news(self): 
        for filename in os.listdir("data/news"):
            if filename.endswith(".json") and filename.split("-")[0].lower() == self.company:
                with open(f"data/news/{filename}") as f:
                    json_data = json.load(f)
                    scores = []
                    dates = []
                    for date in json_data:
                        weeks_score = 0
                        weeks_index = 0  
                        for article in json_data[date]:

                            try:
                                probability = json_data[date][article]['probability']
                                sentiment = json_data[date][article]['sentiment']

                                if sentiment == "positive":
                                    weeks_score += 100 * probability  
                                    weeks_index += 1 

                                elif sentiment == "negative":
                                    weeks_score -= 100 * probability 
                                    weeks_index += 1

                            except:
                                continue
                        
                        if weeks_index > 2: 
                            weeks_score = weeks_score / weeks_index
                            weeks_score = round(weeks_score, 2)

                            # dmy to ymd
                            date = date.split("/")
                            date = f"{date[2]}-{date[0]}-{date[1]}"
                            scores.append(weeks_score)
                            dates.append(date)

                    # scores = replace_zeroes_with_average(scores)
                    self.news_data = pd.DataFrame(scores, columns=['score'])

                    # add dates to dataframe
                    self.news_data['Date'] = dates
                    self.news_data['Date'] = pd.to_datetime(self.news_data['Date'])

                    self.news_data.reset_index(drop=True, inplace=True)
                    self.news_data = self.news_data.iloc[::-1]
                    self.news_data = self.news_data.iloc[-self.period:, :]
                    self.news_data.reset_index(drop=True, inplace=True)

        return self.news_data
                            
    def get_raw_data(self):
        self.historical_data = []
        self.news_data = []

        self.load_historical()
        self.load_news()

        data = pd.merge(self.historical_data, self.news_data, on='Date', how='outer')

        data = data.dropna()
        data.reset_index(drop=True, inplace=True)
        
        return data

# loader = Load_data(period = 100, company = "tesla")
# data = loader.load_political_data()
# print(data)