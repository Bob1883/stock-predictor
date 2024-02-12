from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import os
import json

"""
Oil
Natural gas
Wheat
Copper
Iron ore
Cotton

Gold
Coffee
Coal
Lithium
Lumber
Rubber

Nickel
Zinc
Tin
Aluminum
Lead
Cobalt
"""

MATERIALS = ["Crude Oil", "Iron Ore", "Lithium", "Indium", "Manganese", "Germanium", "Gallium", "Magnesium", "Palladium", "Nickel", "Zinc", "Tin", "Aluminum", "Lead", "Cobalt", "Cotton", "Coffee", "Titanium", "Platinum", "Gold", "Silver", "Copper", "Steel"]
URL = "https://tradingeconomics.com/commodities"

driver = webdriver.Chrome()

for material in MATERIALS: 

    if os.path.exists(f"data-commodity/{material.lower().replace(' ', '-')}.json"):
        print(f"File {material.lower().replace(' ', '-')}.json already exists")
        continue

    driver.get(URL)

    time.sleep(1)

    # find b element with text="Crude Oil"
    try: 
        material_button = driver.find_element(By.XPATH, f"//b[text()='{material}']")
        material_button.click()
    except:
        time.sleep(1)
        material_button = driver.find_element(By.XPATH, f"//b[text()='{material}']")
        material_button.click()


    time.sleep(1)

    # get the network traffic data from the page
    data = driver.execute_script("return window.performance.getEntries();")

    for res in data: 
        if "https://markets.tradingeconomics.com/chart" in res["name"]:
            url = res["name"]
            break

    if url != None: 
        driver.get(url)
        time.sleep(1)

        data = driver.find_element(By.TAG_NAME, "pre").text

        print(data)

        data = json.loads(data)

        material = material.lower().replace(" ", "-")
        with open(f"data-commodity/{material}.json", "w") as json_file:
            json.dump(data, json_file)
    else:
        print(f"Could not find url for {material}")