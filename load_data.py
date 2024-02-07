from constants import *
import datetime

class Load_data(): 

    def __init__(self, period = 1, company = "tesla"):
        self.period = period
        self.company = company

        self.historical_data = []
        self.day_data = []
        self.news_data = []

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
