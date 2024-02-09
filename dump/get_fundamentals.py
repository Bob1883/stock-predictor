import requests
import json
import os
import time

API_KEY = "2cf5ad25c51056e4e79ad5dc9174649726f05aaa00ec12c0d871"

symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'LLY', 'UNH', 'V', 'NVO', 'XOM', 'WMT', 'JPM', 'MC.PA', 'JNJ', 'MA', 'AVGO', 'TCEHY', 'PG', '005930.KS', 'CVX', 'NESN.SW', 'ORCL', 'HD', '600519.SS', 'ABBV', 'MRK', 'COST', 'ADBE', 'IHC.AE', 'TM', 'ASML', 'KO', 'SHEL', 'PEP', 'OR.PA', '1398.HK', 'CSCO', 'BAC', 'AZN', 'BABA', 'ROG.SW', 'NVS', 'CRM', 'ACN', 'RELIANCE.NS', 'RMS.PA', '601857.SS', 'MCD', '0941.HK', 'CMCSA', 'LIN', 'TMO', 'PFE', '601288.SS', 'ABT', 'AMD', 'TMUS', 'TTE', 'NKE', 'HSBC', 'DIS', 'NFLX', 'TCS.NS', 'AMGN', 'COP', 'DHR', 'WFC', 'SAP', 'INTC', '601939.SS', 'INTU', 'HDB', '601988.SS', 'PM', 'BHP', 'PDD', 'TXN', 'SNY', 'CAT', 'CDI.PA', 'UPS', 'VZ', 'IBM', 'UNP', 'MS', 'QCOM', 'PRX.AS', 'HON', 'UL', 'BMY', 'AMAT', 'GE', 'BP', 'RY', 'IDEXY']
companies = ['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet', 'Amazon', 'NVIDIA', 'Facebook', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson and Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter and Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "LOreal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']

for company in companies: 
    if os.path.exists(f"data/fundamentals/{company}.json"):
        continue

    try: 
        symbol = symbols[companies.index(company)]

        url = f"https://api.datajockey.io/v0/company/financials?apikey={API_KEY}&ticker={symbol}&period=Q"

        response = requests.get(url)
        data = response.json()

        with open(f"data/fundamentals/{company}.json", "w") as file:
            json.dump(data, file, indent=4)

        time.sleep(6) 

        print(company, "done")
        
    except Exception as e:
        print(e)
        time.sleep(6) 
        continue