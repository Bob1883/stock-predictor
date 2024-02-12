import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import csv 

company_list = ["apple", "microsoft", "amazon", "google", "facebook", "tesla", "berkshire_hathaway", "visa", "johnson", "walmart", "jpmorgan", "mastercard", "procter_gamble", "unitedhealth", "nvidia", "disney", "homedepot", "paypal", "bank_of_america", "verizon", "adobe", "comcast", "cocacola", "nike", "merck", "pepsi", "pfizer", "att", "intel", "salesforce", "abbott", "oracle", "abbvie", "cisco", "thermo_fisher", "broadcom", "exxonmobil", "accenture", "qualcomm", "chevron", "lilly", "mcdonalds", "danaher", "costco", "medtronic", "nextera_energy", "texas_instruments", "union_pacific", "linde", "bristol_meyers", "boeing", "american_tower", "lowes", "starbucks", "general_electric", "gilead_sciences", "charter_communications", "caterpillar", "amd", "cvs_health", "3m", "anthem", "goldman_sachs", "blackrock", "altria", "ups", "american_express", "tjx", "dominion_energy", "cigna", "chubb", "duke_energy", "southern_company", "becton_dickinson", "ibm", "s&p_global", "stryker", "raytheon", "intuitive_surgical", "zoetis", "citigroup", "prologis", "crown_castle", "target", "servicenow", "equinix", "vertex_pharmaceuticals", "illinois_tool_works", "lockheed_martin", "activision_blizzard", "adp", "regeneron_pharmaceuticals", "booking_holdings", "colgate_palmolive", "micron_technology", "csx", "trufinancial", "illumina", "fidelity_national_information", "us_bancorp", "square", "marsh_mclennan", "pnc_financial_services", "honeywell"]
driver = webdriver.Chrome(executable_path="chromedriver.exe")

for company_name in company_list:
    if os.path.exists(f"data-trend/{company_name}-trend.json"):
        print(f"File {company_name}-trend.json already exists")
        continue

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

        # go to download file and extract the data from the multiTimeline.csv (C:\Users\august.brunnbergfri\Downloads)
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
        with open(f'data-trend/{company_name}-trend.json', 'w') as f:
            json.dump(your_list, f)
    
    except:
        continue