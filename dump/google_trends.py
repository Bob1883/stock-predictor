import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import csv 

company_list =['Apple', 'Microsoft', 'Saudi Aramco', 'Google', 'Amazon', 'NVIDIA', 'Facebook', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson and Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter and Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "LOreal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']
driver = webdriver.Chrome(executable_path="assets/chromedriver.exe")

for company_name in company_list:
    if os.path.exists(f"data/data-google-trends/{company_name}-trend.json"):
        pass
    else:
        try:
            driver.get("https://trends.google.com/trends/?geo=US")

            time.sleep(1)

            # find input with class="VfPpkd-fmcmS-wGMbrd"
            search_box = driver.find_element(selenium.webdriver.common.by.By.CLASS_NAME, "VfPpkd-fmcmS-wGMbrd")
            search_box.click()

            time.sleep(1)
            search_box = driver.find_elements(selenium.webdriver.common.by.By.CLASS_NAME, "VfPpkd-fmcmS-wGMbrd")[1]
            search_box.send_keys(Keys.ENTER)

            time.sleep(1)

            search_box = driver.find_element(selenium.webdriver.common.by.By.ID, "input-29")
            search_box.send_keys(f"{company_name}")
            search_box.send_keys(Keys.ENTER)

            time.sleep(1)

            contray = driver.find_element(selenium.webdriver.common.by.By.CLASS_NAME, "compare-picker")
            contray.click()

            time.sleep(1)

            search_box = driver.find_elements(selenium.webdriver.common.by.By.CLASS_NAME, "hierarchy-picker-label")[0]
            search_box.click()

            time.sleep(1)

            time_interval = driver.find_elements(selenium.webdriver.common.by.By.CLASS_NAME, "compare-picker")[1]
            time_interval.click()

            time.sleep(1)

            search_box = driver.find_elements(selenium.webdriver.common.by.By.CLASS_NAME, "custom-date-picker-select-option")[8]
            search_box.click()

            time.sleep(1)

            download = driver.find_element(selenium.webdriver.common.by.By.CLASS_NAME, "export")
            download.click()

            time.sleep(1)

            with open(r'C:\Users\August\Downloads\multiTimeline.csv', 'r') as f:
                reader = csv.reader(f)
                your_list = list(reader)

            your_list = your_list[3:]

            # delet the file
            os.remove(r'C:\Users\August\Downloads\multiTimeline.csv')

            # remove <Â\xa form the list
            for n in range(len(your_list)):
                your_list[n][1] = your_list[n][1].replace('<Â\xa0', '')

            print(your_list)

            # save the list as a json file
            with open(f'data/data-google-trends/{company_name}-trend.json', 'w') as f:
                json.dump(your_list, f)
        
        except:
            print(f"Error with {company_name}")
            continue