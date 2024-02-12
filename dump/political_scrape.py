from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time
import os
import json

company_list = ['Apple', 'Microsoft', 'Saudi Aramco', 'Alphabet (Google)', 'Amazon', 'NVIDIA', 'Meta', 'Tesla', 'Berkshire Hathaway', 'Eli Lilly', 'UnitedHealth', 'Visa', 'TSMC', 'Novo Nordisk', 'Exxon Mobil', 'Walmart', 'JPMorgan Chase', 'LVMH', 'Johnson & Johnson', 'Mastercard', 'Broadcom', 'Tencent', 'Procter & Gamble', 'Samsung', 'Chevron', 'Nestlé', 'Oracle', 'Home Depot', 'Kweichow Moutai', 'AbbVie', 'Merck', 'Costco', 'Adobe', 'International Holding Company', 'Toyota', 'ASML', 'Coca-Cola', 'Shell', 'Pepsico', "L'Oréal", 'ICBC', 'Cisco', 'Bank of America', 'AstraZeneca', 'Alibaba', 'Roche', 'Novartis', 'Salesforce', 'Accenture', 'Reliance Industries', 'Hermès', 'PetroChina', 'McDonald', 'China Mobile', 'Comcast', 'Linde', 'Thermo Fisher Scientific', 'Pfizer', 'Agricultural Bank of China', 'Abbott Laboratories', 'AMD', 'T-Mobile US', 'TotalEnergies', 'Nike', 'HSBC', 'Walt Disney', 'Netflix', 'Tata Consultancy Services', 'Amgen', 'ConocoPhillips', 'Danaher', 'Wells Fargo', 'SAP', 'Intel', 'China Construction Bank', 'Intuit', 'HDFC Bank', 'Bank of China', 'Philip Morris', 'BHP Group', 'Pinduoduo', 'Texas Instruments', 'Sanofi', 'Caterpillar', 'Dior', 'United Parcel Service', 'Verizon', 'IBM', 'Union Pacific Corporation', 'Morgan Stanley', 'QUALCOMM', 'Prosus', 'Honeywell', 'Unilever', 'Bristol-Myers Squibb', 'Applied Materials', 'General Electric', 'BP', 'Royal Bank Of Canada', 'Inditex']

driver = webdriver.Chrome()

for company in company_list: 
    if os.path.exists(f"data-political/{company}-political.json"):
        print(f"File {company}-political.json already exists")
        continue
    try: 
        driver.get("https://www.capitoltrades.com/issuers#")
        time.sleep(1)

        search_box = driver.find_element(By.CLASS_NAME, "debounced-input")
        search_box.clear()
        time.sleep(1)

        search_box.send_keys(company)
        time.sleep(1)

        search_box.send_keys(Keys.ENTER)
        time.sleep(1)

        company_card = driver.find_elements(By.CLASS_NAME, "q-column--issuerName")[1]
        company_card.click()
        time.sleep(1)

        time_period = driver.find_element(By.CLASS_NAME, "val--all")
        time_period.click()
        time.sleep(2)

        data = driver.execute_script("return window.performance.getEntries();")
        print(data)
        
        time.sleep(1)  

        urls = []

        for res in data: 
            if "https://bff.capitoltrades.com/prices" in res["name"]:
                 urls.append(res["name"])

        url = urls[-1]

        print(url)

        if url != None: 
            driver.get(url)
            time.sleep(1)

            data = driver.find_element(By.TAG_NAME, "pre").text

            print(data)

            data = json.loads(data)

            with open(f"data-political/{company}-political.json", "w") as json_file:
                json.dump(data, json_file)

            time.sleep(100)
        else:
            print(f"Could not find url for {company}")   

    except Exception as e:
        print(e)
        time.sleep(100)
        close_button = driver.find_element(By.CLASS_NAME, "icon--close")
        close_button.click()
        time.sleep(1)

        continue