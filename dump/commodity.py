# https://tradingeconomics.com/commodities

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import csv 

driver = webdriver.Chrome(executable_path="chromedriver.exe")

company_name = "commodity"

driver.get("https://tradingeconomics.com/commodities")

time.sleep(100)

#/commodity/crude-oil
