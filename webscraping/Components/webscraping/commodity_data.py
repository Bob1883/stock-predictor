from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep as time_sleep
from os.path import exists as path_exists
from json import loads as json_loads    
from json import dumps as json_dumps
from random import uniform

# TODO: check if the data is already saved, if it is then just add the resent data to the file
def get_commodity_data(commodities: list) -> dict:
    """
    Get the commodity data for a specific commodity.
    commodity: Commodity to get the data for (e.g., "Crude Oil")

    The available commodities are:
    - Crude Oil, Iron Ore, Lithium, Indium, Manganese, Germanium, Gallium, Magnesium, Palladium, 
    Nickel, Zinc, Tin, Aluminum, Lead, Cobalt, Cotton, Coffee, Titanium, Platinum, Gold, Silver, 
    Copper, Steel
    """

    URL = "https://tradingeconomics.com/commodities"

    driver = Chrome()

    commodities_data = {}

    for material in commodities: 
        commodities_data[material] = {}
        if path_exists(f"data-commodity/{material.lower().replace(' ', '-')}.json"):
            print(f"File {material.lower().replace(' ', '-')}.json already exists")
            continue

        driver.get(URL)

        time_sleep(uniform(0.5, 1.0))

        try: 
            material_button = driver.find_element(By.XPATH, f"//b[text()='{material}']")
            material_button.click()
        except:
            time_sleep(uniform(0.5, 1.0))
            material_button = driver.find_element(By.XPATH, f"//b[text()='{material}']")
            material_button.click()


        time_sleep(uniform(0.5, 1.0))

        data = driver.execute_script("return window.performance.getEntries();")

        for res in data: 
            if "https://markets.tradingeconomics.com/chart" in res["name"]:
                url = res["name"]
                break

        if url != None: 
            driver.get(url)
            time_sleep(uniform(0.5, 1.0))

            data = driver.find_element(By.TAG_NAME, "pre").text

            print(data)

            int("crash")
        else:
            print(f"Could not find url for {material}") 

    driver.quit()
    return commodities_data

# test 
get_commodity_data(["Crude Oil"])