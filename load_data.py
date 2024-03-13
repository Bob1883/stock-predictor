from constants import *

# alot of them are missing dates so this funktion fixes that 
def fix_date_gaps(df, clm_name="Score"):
    # Ensure 'Date' column is a datetime type
    df['Date'] = pd.to_datetime(df['Date']) 

    # Get the dates from start to end 
    start_date = df['Date'].min()  # More efficient than iloc[0]
    end_date = df['Date'].max()   # More efficient than iloc[-1]

    # Get all the dates in between
    all_dates = pd.date_range(start_date, end_date)
    new_rows = []

    # Iterate through expected dates
    for i in range(len(df) - 1):
        current_date = df.loc[i, 'Date']
        next_date = df.loc[i + 1, 'Date']

        days_to_interpolate = (next_date - current_date).days - 1  # Subtract 1

        if days_to_interpolate > 0:  # Only interpolate if a gap exists
            df[clm_name] = pd.to_numeric(df[clm_name]) 
            score_diff = df.loc[i + 1, clm_name] - df.loc[i, clm_name]
            score_increment = score_diff / days_to_interpolate

            for j in range(1, days_to_interpolate):
                new_date = current_date + pd.Timedelta(days=j)
                new_score = df.loc[i, clm_name] + score_increment * j
                new_rows.append({'Date': new_date, clm_name: new_score})

    new_df = pd.DataFrame(new_rows)

    # Concatenate with the original DataFrame 
    df = pd.concat([df, new_df], ignore_index=True) 

    # Sort after filling gaps
    df = df.sort_values(by='Date').reset_index(drop=True)

    return df

class Load_data(): 
    """
    This class is used to load data from the data folder.
    (NOT PREPROCESSED)
    company: str - company name
    """

    def __init__(self, company:str):
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

                    self.google_trends_data = pd.DataFrame(scores, columns=['Score'])

                    # add dates to dataframe
                    self.google_trends_data['Date'] = dates
                    self.google_trends_data['Date'] = pd.to_datetime(self.google_trends_data['Date'])

                    self.google_trends_data.reset_index(drop=True, inplace=True)
                    self.google_trends_data.reset_index(drop=True, inplace=True)

        self.google_trends_data = fix_date_gaps(self.google_trends_data)

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
                    
                    self.political_data = pd.DataFrame(scores, columns=['Score'])

                    # add dates to dataframe
                    self.political_data['Date'] = dates
                    self.political_data['Date'] = pd.to_datetime(self.political_data['Date'])

                    self.political_data.reset_index(drop=True, inplace=True)
                    self.political_data = self.political_data.iloc[::-1]
                    self.political_data.reset_index(drop=True, inplace=True)

        self.political_data = fix_date_gaps(self.political_data)

         # smooth out the curve 
        if use_frec:
            lowess = sm.nonparametric.lowess
            z = lowess(self.political_data['Score'], self.political_data.index, frac=0.01)
            self.political_data['Score'] = z[:, 1]

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

        self.day_data = fix_date_gaps(self.day_data, clm_name="Adj Close")

        # smooth out the curve
        if use_frec:
            lowess = sm.nonparametric.lowess
            z = lowess(self.day_data['Adj Close'], self.day_data.index, frac=0.005)
            self.day_data['Adj Close'] = z[:, 1]

        # plt the data
        # plt.plot(self.day_data['Date'], self.day_data['Adj Close'])
        # plt.show()

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
                    self.news_data = pd.DataFrame(scores, columns=['Score'])

                    # add dates to dataframe
                    self.news_data['Date'] = dates
                    self.news_data['Date'] = pd.to_datetime(self.news_data['Date'])

                    self.news_data.reset_index(drop=True, inplace=True)
                    self.news_data = self.news_data.iloc[::-1]
                    self.news_data.reset_index(drop=True, inplace=True)

        self.news_data = fix_date_gaps(self.news_data)

        if use_frec: 
            lowess = sm.nonparametric.lowess
            z = lowess(self.news_data['Score'], self.news_data.index, frac=0.015)
            self.news_data['Score'] = z[:, 1]

        # plt.plot(self.news_data['Date'], self.news_data['Score'])
        # plt.show()

        return self.news_data

    def load_commodities(self):
        self.commodities_data = pd.DataFrame()

        for filename in os.listdir("data/commodity"):
            if filename.endswith(".json"):
                with open(f"data/commodity/{filename}") as f:
                    temp_df = []
                    json_data = json.load(f)
                    scores = []
                    dates = []
                    for data in json_data["series"][0]["data"]:
                        scores.append(data["y"])
                        dates.append(data["date"])

                    temp_df = pd.DataFrame(scores, columns=[str(filename.split(".")[0])])  
    
                    temp_df['Date'] = dates
                    temp_df['Date'] = pd.to_datetime(temp_df['Date'])

                    temp_df.reset_index(drop=True, inplace=True)

                    temp_df = fix_date_gaps(temp_df, clm_name=filename.split(".")[0])

                    if use_frec:
                        lowess = sm.nonparametric.lowess
                        z = lowess(temp_df[filename.split(".")[0]], temp_df.index, frac=0.01)
                        temp_df[filename.split(".")[0]] = z[:, 1]

                    if self.commodities_data.empty:
                        self.commodities_data = temp_df
                    else:
                        self.commodities_data = pd.merge(self.commodities_data, temp_df, on='Date', how='outer')

        self.commodities_data = self.commodities_data.dropna()
        self.commodities_data.reset_index(drop=True, inplace=True)

        return self.commodities_data

    def get_raw_data(self):
        self.historical_data = []
        self.news_data = []

        self.load_historical()
        self.load_news()

        data = pd.merge(self.historical_data, self.news_data, on='Date', how='outer')

        data = data.dropna()
        data.reset_index(drop=True, inplace=True)
        
        return data

# loader = Load_data(company = "tesla")
# g_trends = loader.load_google_trends()
# political = loader.load_political_data()
# world = loader.load_world_data()
# fundemental = loader.load_fundemental_data()
# day = loader.load_day_data()
# news = loader.load_news()
# commo = loader.load_commodities()