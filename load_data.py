from constants import *

def fix_date_gaps(df, clm_name="Score"):
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    all_dates = pd.date_range(start_date, end_date)
    new_df = pd.DataFrame({'Date': all_dates})
    merged_df = pd.merge(new_df, df, on='Date', how='left')
    merged_df[clm_name] = merged_df[clm_name].interpolate()

    return merged_df

def monthly_to_daily(df, date_col='Date', value_col='Score'):
    df[date_col] = pd.to_datetime(df[date_col])
    start_date = df[date_col].min()
    end_date = df[date_col].max()
    daily_dates = pd.date_range(start_date, end_date, freq='D')
    daily_df = pd.DataFrame({date_col: daily_dates})
    merged_df = pd.merge(daily_df, df, on=date_col, how='left')
    merged_df[value_col] = merged_df[value_col].ffill()
    
    return merged_df

def add_missing_dates(data, clm_name="Score"):
    last_date = data['Date'].max()
    target_date = pd.to_datetime('2023-10-13')
    
    if last_date < target_date:
        date_range = pd.date_range(start=last_date + pd.Timedelta(days=1), end=target_date)
        missing_dates = pd.DataFrame({'Date': date_range})
        missing_dates[clm_name] = data[clm_name].iloc[-1] 
        data = pd.concat([data, missing_dates], ignore_index=True)

    return data

def freq_smooth(data, clm_name="Score"):
    if use_freq:
        lowess = sm.nonparametric.lowess
        z = lowess(data[clm_name], data.index, frac=0.01)
        data[clm_name] = z[:, 1]

    return data

# TODO 
# Fundemental data

class Load_data(): 
    """
    This class is used to load data from the data folder.
    (NOT PREPROCESSED)
    company: str - company name
    """

    def __init__(self, company:str):
        self.company = company

        self.world_economy_data = []
        self.google_trends_data = []
        self.historical_data = []
        self.political_data = []
        self.volumes_data = []
        self.news_data = []
        self.day_data = []

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
        
        self.google_trends_data = monthly_to_daily(self.google_trends_data)
        self.google_trends_data = fix_date_gaps(self.google_trends_data)
        self.google_trends_data = add_missing_dates(self.google_trends_data)

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
        self.political_data = add_missing_dates(self.political_data)

        # smooth out the curve 
        if use_freq:
            lowess = sm.nonparametric.lowess
            z = lowess(self.political_data['Score'], self.political_data.index, frac=0.01)
            self.political_data['Score'] = z[:, 1]

        return self.political_data

    def load_world_data(self):
        self.world_economy_data = pd.DataFrame()
        for filename in os.listdir("data/world"):
            if filename.endswith(".xls"):
                
                # Export data ends in 2014, so we skip it
                if filename == "Export.xls":
                    continue

                df = pd.read_excel(f"data/world/{filename}")

                # Remove rows with all NaN values
                df = df.dropna(how='all')
                
                # Remove columns with all NaN values
                df = df.dropna(axis=1, how='all')
                
                # Set the first column as the index
                df.set_index(df.columns[0], inplace=True)
                
                # Select the row with the desired data (e.g., "Advanced economies")
                row_name = "Advanced economies"
                if row_name in df.index:
                    data_row = df.loc[row_name]
                    
                    # Create a new DataFrame with the desired format
                    new_df = pd.DataFrame(columns=['Date', filename.split('.')[0]])
                    
                    # Extract the year from the date strings and create the 'Date' column
                    new_df['Date'] = pd.to_datetime(data_row.index.astype(str).str[:4], format='%Y')
                    
                    new_df[filename.split('.')[0]] = data_row.values
                    
                    # Fill missing values using linear interpolation
                    new_df = fix_date_gaps(new_df, clm_name=filename.split('.')[0])
                    
                    # Merge with the main DataFrame
                    if self.world_economy_data.empty:
                        self.world_economy_data = new_df
                    else:
                        self.world_economy_data = pd.merge(self.world_economy_data, new_df, on='Date', how='outer')
        
        self.world_economy_data = self.world_economy_data.dropna()
        self.world_economy_data.reset_index(drop=True, inplace=True)

        for col in self.world_economy_data.columns:
            if col == "Date":
                continue
            self.world_economy_data = monthly_to_daily(self.world_economy_data, date_col='Date', value_col=col)
            self.world_economy_data = fix_date_gaps(self.world_economy_data, clm_name=col)
        
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

        # Add missing dates and values until the last date is 2023-10-13
        last_date = self.day_data['Date'].max()
        if last_date < pd.to_datetime("2023-10-13"):
            date_range = pd.date_range(start=last_date + pd.Timedelta(days=1), end="2023-10-13")
            missing_dates = pd.DataFrame({"Date": date_range})
            missing_dates['Adj Close'] = self.day_data['Adj Close'].mean()
            self.day_data = pd.concat([self.day_data, missing_dates], ignore_index=True)

        # smooth out the curve
        if use_freq:
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
                                pass
                        
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
        self.news_data = add_missing_dates(self.news_data)

        if use_freq: 
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
                    if use_freq:
                        lowess = sm.nonparametric.lowess
                        z = lowess(temp_df[filename.split(".")[0]], temp_df.index, frac=0.01)
                        temp_df[filename.split(".")[0]] = z[:, 1]
                    if self.commodities_data.empty:
                        self.commodities_data = temp_df
                    else:
                        self.commodities_data = pd.merge(self.commodities_data, temp_df, on='Date', how='outer')

        
        for commodity in self.commodities_data.columns:
            if commodity == "Date":
                continue
            self.commodities_data = add_missing_dates(self.commodities_data, clm_name=commodity)
            self.commodities_data = fix_date_gaps(self.commodities_data, clm_name=commodity)
            
        self.commodities_data = self.commodities_data.dropna()
        self.commodities_data.reset_index(drop=True, inplace=True)
        return self.commodities_data
    
    def load_volumes(self):
        self.volumes_data = pd.DataFrame()
        for filename in os.listdir("data/data-week"):
            if filename.endswith(".csv"):
                if filename.split("-")[0].lower() == self.company:
                    df = pd.read_csv(f"data/data-week/{filename}")
                    volumes = []
                    dates = []
                    for date in df['Date']:
                        volumes.append(df[df['Date'] == date]['Volume'].values[0])
                        dates.append(date)
                    
                    self.volumes_data = pd.DataFrame(volumes, columns=['Volume'])
                    # add dates to dataframe
                    self.volumes_data['Date'] = dates
                    self.volumes_data['Date'] = pd.to_datetime(self.volumes_data['Date'])

                    self.volumes_data.reset_index(drop=True, inplace=True)
                    
        self.volumes_data = fix_date_gaps(self.volumes_data, clm_name="Volume")
        self.volumes_data = add_missing_dates(self.volumes_data, clm_name="Volume") 

        return self.volumes_data

    def load_indicators(self):
        self.load_day_data()
        self.load_volumes()
        close_prices = self.day_data['Adj Close'].values
        volume = self.volumes_data['Volume'].values
        dates = self.day_data['Date'].values
        
        rsi_data = calculate_rsi(close_prices)
        macd_data, macd_signal_data, macd_histogram_data = calculate_macd(close_prices)
        ema_20 = calculate_ema(close_prices, window=20)
        ema_50 = calculate_ema(close_prices, window=50)
        ema_200 = calculate_ema(close_prices, window=200)
        bb_high_data, bb_low_data = calculate_bollinger_bands(close_prices)
        obv_data = calculate_obv(close_prices, volume)

        # Create DataFrames for each indicator
        rsi_df = pd.DataFrame({'RSI': rsi_data, 'Date': dates[14:]})
        macd_df = pd.DataFrame({'MACD': macd_data, 'Signal': macd_signal_data, 'Histogram': macd_histogram_data, 'Date': dates})
        ema_df = pd.DataFrame({'EMA_20': ema_20, 'EMA_50': ema_50, 'EMA_200': ema_200, 'Date': dates})
        bb_df = pd.DataFrame({'BB_High': bb_high_data, 'BB_Low': bb_low_data, 'Date': dates})
        obv_df = pd.DataFrame({'OBV': obv_data, 'Date': dates})

        # plot the data on top of the price data
        plt.plot(self.day_data['Date'], close_prices, label='Close Prices')
        plt.plot(rsi_df['Date'], rsi_df['RSI'], label='RSI')
        plt.plot(macd_df['Date'], macd_df['MACD'], label='MACD')
        plt.plot(ema_df['Date'], ema_df['EMA_20'], label='EMA 20')
        plt.plot(ema_df['Date'], ema_df['EMA_50'], label='EMA 50')
        plt.plot(ema_df['Date'], ema_df['EMA_200'], label='EMA 200')
        plt.plot(bb_df['Date'], bb_df['BB_High'], label='Bollinger Bands High')
        plt.plot(bb_df['Date'], bb_df['BB_Low'], label='Bollinger Bands Low')
        plt.legend()
        plt.show()

        return rsi_df, macd_df, ema_df, bb_df, obv_df

loader = Load_data(company = "tesla")
loader.load_indicators()