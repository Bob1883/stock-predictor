from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import os
import json

driver = webdriver.Chrome()

URL = "https://companiesmarketcap.com/"


"""
['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet (Google)', 'Amazon', 'NVIDIA', 'Meta', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson & Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter & Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "L'Oréal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']
['AAPL', 'MSFT', '2222.SR', 'GOOG', '5AMZN', '6NVDA', '7META', '8TSLA', '9BRK-B', '10LLY', '11UNH', '12V', '13TSM', '14NVO', '15XOM', '16WMT', '17JPM', '18MC.PA', '19JNJ', '20MA', '21AVGO', '22TCEHY', '23PG', '24005930.KS', '25CVX', '26NESN.SW', '27ORCL', '28HD', '29600519.SS', '30ABBV', '31MRK', '32COST', '33ADBE', '34IHC.AE', '35TM', '36ASML', '37KO', '38SHEL', '39PEP', '40OR.PA', '411398.HK', '42CSCO', '43BAC', '44AZN', '45BABA', '46ROG.SW', '47NVS', '48CRM', '49ACN', '50RELIANCE.NS', '51RMS.PA', '52601857.SS', '53MCD', '540941.HK', '55CMCSA', '56LIN', '57TMO', '58PFE', '59601288.SS', '60ABT', '61AMD', '62TMUS', '63TTE', '64NKE', '65HSBC', '66DIS', '67NFLX', '68TCS.NS', '69AMGN', '70COP', '71DHR', '72WFC', '73SAP', '74INTC', '75601939.SS', '76INTU', '77HDB', '78601988.SS', '79PM', '80BHP', '81PDD', '82TXN', '83SNY', '84CAT', '85CDI.PA', '86UPS', '87VZ', '88IBM', '89UNP', '90MS', '91QCOM', '92PRX.AS', '93HON', '94UL', '95BMY', '96AMAT', '97GE', '98BP', '99RY', '100IDEXY']
"""

names = []
symbols = []

driver.get(URL) 

time.sleep(1) 

# get all company-name class elements and take the text from them 
name_elements = driver.find_elements(By.CLASS_NAME, "company-name")
for name_element in name_elements: 
    names.append(name_element.text)

# get all company-code class elements and take the text from them
symbol_elements = driver.find_elements(By.CLASS_NAME, "company-code")
for symbol_element in symbol_elements: 
    symbols.append(symbol_element.text)

print(names)
print(symbols)