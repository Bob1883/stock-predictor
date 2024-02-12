import os 
import json
import datetime
import time

#1. check so all the dates are in order
#2. check so all dates are scraped
#3. check so all the companies are scraped

wrong_format = []
dates_to_fix = []
news_articles = 0

for file in os.listdir("data-news"):
    try:
        if file.endswith(".json"):
            with open(f"data-news/{file}", "r") as json_file:
                data = json.load(json_file)
            for date in data:
                news_articles += 1
                try:
                    date = date.split("/")
                    date = f"{date[2]}-{date[0]}-{date[1]}"
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                except:
                    wrong_format.append(file + "wrong date format")

            if list(data.keys())[0] != "10/12/2023" and list(data.keys())[0] != "10/13/2023" and list(data.keys())[0] != "10/14/2023" and list(data.keys())[0] != "10/15/2023" and list(data.keys())[0] != "10/16/2023" and list(data.keys())[0] != "10/17/2023" and list(data.keys())[0] != "10/18/2023":
                wrong_format.append(file + "wrong start date")

                # get all the dates that are missing, its for every 7 days so take the first date count up in 7 day intervalls ontill we get to an expected date
                first_date = list(data.keys())[0]
                first_date = datetime.datetime.strptime(first_date, "%m/%d/%Y")
                while first_date < datetime.datetime.strptime("10/12/2023", "%m/%d/%Y"):
                    first_date += datetime.timedelta(days=7)
                    first_date = first_date.strftime("%m/%d/%Y")
                    if first_date not in data:
                        dates_to_fix.append(file + first_date)
                    first_date = datetime.datetime.strptime(first_date, "%m/%d/%Y")

    except:
        pass

# print data errors in red and bold
print("\033[1m\033[91m")
print("Data errors:")
print(wrong_format)
print("\033[0m")

# print dates that are missing in red and bold
# print("\033[1m\033[91m")
# print("Dates that are missing:")
# print(dates_to_fix)
# print(len(dates_to_fix))
# print("\033[0m")
while True:
    news_articles = 0
    wrong_format = []
    dates_to_fix = []
    scores = 0

    for file in os.listdir("data-news"):
        try:
            if file.endswith(".json"):
                with open(f"data-news/{file}", "r") as json_file:
                    data = json.load(json_file)
                for date in data:
                    if data[date]["artical1"]["score"] == None:
                        scores += 1
                    news_articles += 1
                    try:
                        date = date.split("/")
                        date = f"{date[2]}-{date[0]}-{date[1]}"
                        datetime.datetime.strptime(date, "%Y-%m-%d")
                    except:
                        wrong_format.append(file + "wrong date format")

                if list(data.keys())[0] != "10/12/2023" and list(data.keys())[0] != "10/13/2023" and list(data.keys())[0] != "10/14/2023" and list(data.keys())[0] != "10/15/2023" and list(data.keys())[0] != "10/16/2023" and list(data.keys())[0] != "10/17/2023" and list(data.keys())[0] != "10/18/2023":
                    wrong_format.append(file + "wrong start date")

                    # get all the dates that are missing, its for every 7 days so take the first date count up in 7 day intervalls ontill we get to an expected date
                    first_date = list(data.keys())[0]
                    first_date = datetime.datetime.strptime(first_date, "%m/%d/%Y")
                    while first_date < datetime.datetime.strptime("10/12/2023", "%m/%d/%Y"):
                        first_date += datetime.timedelta(days=7)
                        first_date = first_date.strftime("%m/%d/%Y")
                        if first_date not in data:
                            dates_to_fix.append(file + first_date)
                        first_date = datetime.datetime.strptime(first_date, "%m/%d/%Y")

        except:
            pass
    print("DONE:", news_articles)
    print("LEFT:", len(dates_to_fix))
    print("WRONG:", len(dates_to_fix))
    print("PROSSECED:", scores)
    time.sleep(5)
    os.system("cls")
# company_list = ['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet', 'Amazon', 'NVIDIA', 'Meta', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson & Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter & Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "L'Oréal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']
# avalible_companies = []
# for file in os.listdir("data-news"): 
#     if file.endswith(".json"):
#         with open(f"data-news/{file}", "r") as json_file:
#             data = json.load(json_file)
#         print(data)
#         dates = list(data.keys())
#         new_dates = dates.sort()
#         print(new_dates)

#         if dates != new_dates:
#             # print that the dates are not in order in red  
#             print(f"\033[91m{file} dates are not in order\033[0m")
#         else:
#             print(f"{file} dates are in order")

#         # check so all the dates are scraped, the dates are for evrey 7 days so take the first date and the last date and check so the diffrence is 7 days  
#         first_date = dates[0]
#         last_date = dates[-1]
#         first_date = datetime.datetime.strptime(first_date, "%Y-%m-%d")
#         last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
#         diffrence = last_date - first_date
#         print(diffrence)

#         if diffrence.days < 52: 
#             print(f"\033[91m{file} dates are not scraped\033[0m")
#         else:
#             print(f"{file} dates are scraped")

#         avalible_companies.append(file.replace(".json", "").replace("-news", ""))   

#         time.sleep(1)

# for company in company_list:
#     if company not in avalible_companies:
#         print(f"\033[91m{company} is not scraped\033[0m")
#     else:
#         print(f"{company} is scraped")