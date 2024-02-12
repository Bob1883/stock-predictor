from GoogleNews import GoogleNews
from datetime import datetime, timedelta
import time

company_list = ['Apple', 'Microsoft', 'Saudi Aramco', 'Google', 'Amazon', 'NVIDIA', 'Facebook', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson and Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter and Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "LOreal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']

googlenews = GoogleNews(lang='en', period='7d')

start_date = datetime.strptime("10/13/2023", "%m/%d/%Y") - timedelta(days=365*5)
end_date = datetime.strptime("10/20/2023", "%m/%d/%Y") - timedelta(days=365*5)

for company in company_list:
    # get top 7 news evrey week for 5 years
    for i in range(0, 52*5):
        start_date += timedelta(days=7)
        end_date += timedelta(days=7)
        googlenews.set_time_range(start_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y"))
        googlenews.clear()
        googlenews.search(company)
        results = googlenews.results()
        title = []
        description = []
        for result in results:
            title.append(result['title'])
            description.append(result['desc'])
        # with open(f'news/{company}.txt', 'a') as f:
        #     f.write(news)
        
        # time.sleep(1)