from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import keyboard
import os 
import time

# "10/13/2023" in the format of mm/dd/yyyy datetime
start_date = datetime.strptime("10/13/2023", "%m/%d/%Y") - timedelta(days=365*5)
end_date = datetime.strptime("10/13/2023", "%m/%d/%Y")

# to yyyy-mm-dd
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("--incognito")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")

# make the network speed faster
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--page-load-strategy=eager')

driver = webdriver.Chrome(options=options, executable_path="assets/chromedriver.exe")
driver.get("https://finance.yahoo.com/")
'''
['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet (Google)', 'Amazon', 'NVIDIA', 'Meta', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson & Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter & Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "L'Oréal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']
['AAPL', 'MSFT', '2222.SR', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'LLY', 'UNH', 'V', 'TSM', 'NVO', 'XOM', 'WMT', 'JPM', 'MC.PA', 'JNJ', 'MA', 'AVGO', 'TCEHY', 'PG', '005930.KS', 'CVX', 'NESN.SW', 'ORCL', 'HD', '600519.SS', 'ABBV', 'MRK', 'COST', 'ADBE', 'IHC.AE', 'TM', 'ASML', 'KO', 'SHEL', 'PEP', 'OR.PA', '1398.HK', 'CSCO', 'BAC', 'AZN', 'BABA', 'ROG.SW', 'NVS', 'CRM', 'ACN', 'RELIANCE.NS', 'RMS.PA', '601857.SS', 'MCD', '0941.HK', 'CMCSA', 'LIN', 'TMO', 'PFE', '601288.SS', 'ABT', 'AMD', 'TMUS', 'TTE', 'NKE', 'HSBC', 'DIS', 'NFLX', 'TCS.NS', 'AMGN', 'COP', 'DHR', 'WFC', 'SAP', 'INTC', '601939.SS', 'INTU', 'HDB', '601988.SS', 'PM', 'BHP', 'PDD', 'TXN', 'SNY', 'CAT', 'CDI.PA', 'UPS', 'VZ', 'IBM', 'UNP', 'MS', 'QCOM', 'PRX.AS', 'HON', 'UL', 'BMY', 'AMAT', 'GE', 'BP', 'RY', 'IDEXY']
'''
symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'LLY', 'UNH', 'V', 'NVO', 'XOM', 'WMT', 'JPM', 'MC.PA', 'JNJ', 'MA', 'AVGO', 'TCEHY', 'PG', '005930.KS', 'CVX', 'NESN.SW', 'ORCL', 'HD', '600519.SS', 'ABBV', 'MRK', 'COST', 'ADBE', 'IHC.AE', 'TM', 'ASML', 'KO', 'SHEL', 'PEP', 'OR.PA', '1398.HK', 'CSCO', 'BAC', 'AZN', 'BABA', 'ROG.SW', 'NVS', 'CRM', 'ACN', 'RELIANCE.NS', 'RMS.PA', '601857.SS', 'MCD', '0941.HK', 'CMCSA', 'LIN', 'TMO', 'PFE', '601288.SS', 'ABT', 'AMD', 'TMUS', 'TTE', 'NKE', 'HSBC', 'DIS', 'NFLX', 'TCS.NS', 'AMGN', 'COP', 'DHR', 'WFC', 'SAP', 'INTC', '601939.SS', 'INTU', 'HDB', '601988.SS', 'PM', 'BHP', 'PDD', 'TXN', 'SNY', 'CAT', 'CDI.PA', 'UPS', 'VZ', 'IBM', 'UNP', 'MS', 'QCOM', 'PRX.AS', 'HON', 'UL', 'BMY', 'AMAT', 'GE', 'BP', 'RY', 'IDEXY']
names = ["s&p 500", 'Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet', 'Amazon', 'NVIDIA', 'Facebook', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson and Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter and Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "LOreal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']

try: 
       # find class accept-all
       accept_all = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "accept-all")))
       accept_all.click()
except:
       pass

# find class accept-all
time.sleep(1)
index = 0 
for symbol, name in zip(symbols, names):
       if os.path.exists(f"data-week/{name}-week.csv"):
              continue
       #find id yfin-usr-qry
       if index == 0: 
              search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "yfin-usr-qry")))
              search_bar.clear()
              search_bar.send_keys(name)
              index += 1

              # result-quotes-0 
              result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "modules_quoteRightCol__xPEOm")))
              result.click()

              time.sleep(1)

              # find span with text Historical Data
              historical_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Historical Data']")))
              historical_data.click()

              time.sleep(1)

              # find class C($linkColor)
              time_period = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dateRangeBtn")))
              time_period.click()

              time.sleep(1)

              #  find name startDate
              start_date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "startDate")))
              start_date_input.clear()
              start_date_input.send_keys(start_date.split("-")[0])
              start_date_input.send_keys(Keys.ARROW_RIGHT)
              start_date_input.send_keys(start_date.split("-")[1])
              start_date_input.send_keys(Keys.ARROW_RIGHT)
              start_date_input.send_keys(start_date.split("-")[2])

              time.sleep(1)

              # find name endDate
              end_date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "endDate")))
              end_date_input.clear()
              end_date_input.send_keys(end_date.split("-")[0])
              end_date_input.send_keys(Keys.ARROW_RIGHT)
              end_date_input.send_keys(end_date.split("-")[1])
              end_date_input.send_keys(Keys.ARROW_RIGHT)
              end_date_input.send_keys(end_date.split("-")[2])

              time.sleep(1)

              #  find span with text Done
              done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Done']")))
              done.click()

              time.sleep(1)

              # if you find a span with the text Daily, click it
              if index == 1:
                     time.sleep(10)
                     index += 1

              # find Apply button
              apply = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Apply']")))
              apply.click()

              time.sleep(1)

       else:
              # second element with class finsrch-inpt
              search_bar = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "finsrch-inpt")))[1]
              search_bar.clear()
              search_bar.send_keys(name)

              time.sleep(1)

              search_bar.send_keys(Keys.ENTER)

              time.sleep(1)

              apply = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Apply']")))
              apply.click()

       time.sleep(2)

       # find dawnload button
       download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Download']")))
       download.click()

       time.sleep(4)

       keyboard.press_and_release('enter')

       time.sleep(3)

       # move file from Downloads to data-week. find the first file with .csv extension
       for filename in os.listdir("C:\\Users\\August\\Downloads"):
              if filename.endswith(".csv"):
                     os.rename(f"C:\\Users\\August\\Downloads\\{filename}", f"C:\\Users\\August\\projects\\istock\\data-week\\{name}-week.csv")
                     break
    
       
       time.sleep(100)
       
# https://query1.finance.yahoo.com/v7/finance/download/{symbols}?period1=1539475200&period2=1697155200&interval=1wk&events=history&includeAdjustedClose=true