from load_data import Load_data
from constants import *
import multiprocessing

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

    rsi = []
    macd = []
    ema_20 = []
    ema_50 = []
    ema_200 = []
    bb_low = []
    bb_high = []
    obv = []
    debt = []
    gdp = []
    inflation = []
    unemployement = []
    commodties = []
    google_trends = []
    changes = []
    prices = []
    political = []
    news = []
    names = []

    test_rsi = []
    test_macd = []
    test_ema_20 = []
    test_ema_50 = []
    test_ema_200 = []
    test_low_bb = []
    test_bb_high = []
    test_obv = []
    test_debt = []
    test_gdp = []
    test_inflation = []
    test_unemployement = []
    test_commodties = []
    test_google_trends = []
    test_changes = []
    test_prices = []
    test_political = []
    test_news = []
    test_names = []

    company_to_int = {company: i for i, company in enumerate(companies)}
    
    commodity_prices = Load_data("tesla").load_commodities()

    for company in companies:
        try:
            printProgressBar(companies.index(company), len(companies), description=f"Preprocessing {company}" )
            loader = Load_data(company=company.lower())

            rsi_data = []
            macd_data = []
            ema_20_data = []
            ema_50_data = []
            ema_200_data = []
            bb_low_data = []
            bb_high_data = []
            obv_data = []
            debt_data = []
            gdp_data = []
            inflation_data = []
            unemployement_data = []
            best_commodities = []
            commodity_data = [[], [], []]
            changes_data = [] 
            price_data = []
            g_trends = []
            political_data = []
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
            temp_google_trends = loader.load_google_trends()
            temp_political_data = loader.load_political_data()
            temp_indicators = loader.load_indicators()
            temp_world_data = loader.load_world_data()
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

                # google trends data
                g_trends.append(temp_google_trends[temp_google_trends["Date"] == current_date.strftime('%Y-%m-%d')]["Score"].values[0])

                # political data
                political_data.append(temp_political_data[temp_political_data["Date"] == current_date.strftime('%Y-%m-%d')]["Score"].values[0]) 

                # indicators
                rsi_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["RSI"].values[0])
                macd_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["MACD"].values[0])
                ema_20_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["EMA_20"].values[0])
                ema_50_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["EMA_50"].values[0])
                ema_200_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["EMA_200"].values[0])
                bb_low_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["BB_Low"].values[0])
                bb_high_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["BB_High"].values[0])
                obv_data.append(temp_indicators[temp_indicators["Date"] == current_date.strftime('%Y-%m-%d')]["OBV"].values[0])

                # world data
                debt_data.append(temp_world_data[temp_world_data["Date"] == current_date.strftime('%Y-%m-%d')]["debt"].values[0])
                gdp_data.append(temp_world_data[temp_world_data["Date"] == current_date.strftime('%Y-%m-%d')]["GDP"].values[0])
                inflation_data.append(temp_world_data[temp_world_data["Date"] == current_date.strftime('%Y-%m-%d')]["Inflation"].values[0])
                unemployement_data.append(temp_world_data[temp_world_data["Date"] == current_date.strftime('%Y-%m-%d')]["Unemployment"].values[0])


            price_data = scaler.fit_transform(price_data).tolist()
            news_data = scaler.fit_transform(np.array(news_data).reshape(-1, 1)).flatten().tolist()
            commodity_data[0] = scaler.fit_transform(np.array(commodity_data[0]).reshape(-1, 1)).flatten().tolist()
            commodity_data[1] = scaler.fit_transform(np.array(commodity_data[1]).reshape(-1, 1)).flatten().tolist()
            commodity_data[2] = scaler.fit_transform(np.array(commodity_data[2]).reshape(-1, 1)).flatten().tolist()
            changes_data = scaler.fit_transform(np.array(changes_data).reshape(-1, 1)).flatten().tolist()
            g_trends = scaler.fit_transform(np.array(g_trends).reshape(-1, 1)).flatten().tolist()
            political_data = scaler.fit_transform(np.array(political_data).reshape(-1, 1)).flatten().tolist()

            rsi_data = scaler.fit_transform(np.array(rsi_data).reshape(-1, 1)).flatten().tolist()
            macd_data = scaler.fit_transform(np.array(macd_data).reshape(-1, 1)).flatten().tolist()
            ema_20_data = scaler.fit_transform(np.array(ema_20_data).reshape(-1, 1)).flatten().tolist()
            ema_50_data = scaler.fit_transform(np.array(ema_50_data).reshape(-1, 1)).flatten().tolist()
            ema_200_data = scaler.fit_transform(np.array(ema_200_data).reshape(-1, 1)).flatten().tolist()
            bb_low_data = scaler.fit_transform(np.array(bb_low_data).reshape(-1, 1)).flatten().tolist()
            bb_high_data = scaler.fit_transform(np.array(bb_high_data).reshape(-1, 1)).flatten().tolist()
            obv_data = scaler.fit_transform(np.array(obv_data).reshape(-1, 1)).flatten().tolist()

            debt_data = scaler.fit_transform(np.array(debt_data).reshape(-1, 1)).flatten().tolist()
            gdp_data = scaler.fit_transform(np.array(gdp_data).reshape(-1, 1)).flatten().tolist()
            inflation_data = scaler.fit_transform(np.array(inflation_data).reshape(-1, 1)).flatten().tolist()
            unemployement_data = scaler.fit_transform(np.array(unemployement_data).reshape(-1, 1)).flatten().tolist()

            if company == test_stock:
                for i in range(len(price_data)):
                    test_prices.append(price_data[i])
                    test_news.append(news_data[i])
                    test_commodties.append([commodity_data[0][i], commodity_data[1][i], commodity_data[2][i]])
                    test_names.append(name_data[i])
                    test_google_trends.append(g_trends[i])
                    test_changes.append(changes_data[i])
                    test_political.append(political_data[i])
                    
                    test_rsi.append(rsi_data[i])
                    test_macd.append(macd_data[i])
                    test_ema_20.append(ema_20_data[i])
                    test_ema_50.append(ema_50_data[i])
                    test_ema_200.append(ema_200_data[i])
                    test_low_bb.append(bb_low_data[i])
                    test_bb_high.append(bb_high_data[i])
                    test_obv.append(obv_data[i])

                    test_debt.append(debt_data[i])
                    test_gdp.append(gdp_data[i])
                    test_inflation.append(inflation_data[i])
                    test_unemployement.append(unemployement_data[i])

                test_commodties.append(commodity_data[0])
                test_commodties.append(commodity_data[1])
                test_commodties.append(commodity_data[2])
            else:
                for i in range(len(price_data)):
                    prices.append(price_data[i])
                    news.append(news_data[i]) 
                    names.append(name_data[i])
                    google_trends.append(g_trends[i])
                    changes.append(changes_data[i])
                    political.append(political_data[i])

                    rsi.append(rsi_data[i])
                    macd.append(macd_data[i])
                    ema_20.append(ema_20_data[i])
                    ema_50.append(ema_50_data[i])
                    ema_200.append(ema_200_data[i])
                    bb_low.append(bb_low_data[i])
                    bb_high.append(bb_high_data[i])
                    obv.append(obv_data[i])

                    debt.append(debt_data[i])
                    gdp.append(gdp_data[i])
                    inflation.append(inflation_data[i])
                    unemployement.append(unemployement_data[i])

                commodties.append(commodity_data[0])
                commodties.append(commodity_data[1])
                commodties.append(commodity_data[2])

        except Exception as e:
            print("\033[91m" + f"Failed to preprocess {company}" + "\033[0m")
            
    return commodties, google_trends, changes, prices, political, news, names, rsi, macd, ema_20, ema_50, ema_200, bb_low, bb_high, obv, debt, gdp, inflation, unemployement

companies = []
for filename in os.listdir('data/data-day'):
    if filename.endswith('.csv'):
        companies.append(filename.split('.')[0].lower())

import plotly.graph_objects as go

def plot_commodity_data(commodities, points):
    fig = go.Figure()

    sizes = [point * 0.3 for point in points]  # Adjust the scaling factor as needed

    fig.add_trace(go.Scatter(
        x=[i for i in range(len(commodities))],
        y=[i % 5 for i in range(len(commodities))],  # Adjust the y-coordinates for better layout
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=points,
            colorscale='Viridis',
            opacity=0.7
        ),
        text=commodities,
        textposition='middle center',
        textfont=dict(
            family='sans serif',
            size=12,
            color='black'
        ),
        hoverinfo='text',
        hovertext=[f"Points: {point}" for point in points]
    ))

    annotations = [
        go.layout.Annotation(
            x=i,
            y=i % 5 + 0.5,  # Adjust the y-coordinate for score position
            text=str(point),
            showarrow=False,
            font=dict(size=12)
        )
        for i, point in enumerate(points)
    ]

    fig.update_layout(
        title='Commodity Importance',
        annotations=annotations,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        showlegend=False,
        width=800,
        height=600
    )

    fig.show()

def calculate_commodity_points(companies):
    commodity_points = {}

    for company in companies:
        loader = Load_data(company=company.lower())
        commodity_prices = loader.load_commodities()

        diffs = {}
        entire_price_data = loader.load_day_data()["Adj Close"].values

        for commodity in commodity_prices:
            if commodity != "Date":
                commodity_price = [str(price) for price in commodity_prices[commodity]]

                if len(commodity_price) > len(entire_price_data):
                    commodity_price = commodity_price[:len(entire_price_data)]

                commodity_price = scaler.fit_transform(np.array(commodity_price).reshape(-1, 1)).reshape(-1)
                company_price = scaler.transform(np.array(entire_price_data).reshape(-1, 1)).reshape(-1)

                if len(commodity_price) != len(company_price):
                    company_price = company_price[:len(commodity_price)]

                diff = np.sqrt(np.mean((commodity_price - company_price) ** 2))
                diffs[commodity] = diff

        sorted_commodities = sorted(diffs, key=diffs.get)

        for i, commodity in enumerate(sorted_commodities[:5]):
            if commodity not in commodity_points:
                commodity_points[commodity] = 0
            commodity_points[commodity] += 5 - i

    return commodity_points

# Rest of your code...

if __name__ == "__main__":
    # Your existing code...

    commodity_points = calculate_commodity_points(companies)
    commodities = list(commodity_points.keys())
    points = list(commodity_points.values())

    plot_commodity_data(commodities, points)