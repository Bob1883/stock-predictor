from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import random
import os
import json

years = 5
delay = 0.5

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("--incognito")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")

options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--page-load-strategy=eager')

# Set the company name and date range
org_start_date = datetime.datetime.strptime("10/13/2023", "%m/%d/%Y")
starting_date = datetime.datetime.strptime("10/26/2018", "%m/%d/%Y")
company_list = ['BHP Group', 'Dior', 'General Electric', 'Morgan Stanley', 'Sanofi', 'SAP', 'Unilever', 'Union Pacific Corporation', 'United Parcel Service', 'Verizon']   
companys_scraped = []

# check what companies are already scraped
# for file in os.listdir("data-news"):
#     if file.endswith(".json"):
#         with open(f"data-news/{file}", "r") as json_file:
#             data = json.load(json_file)
#         if list(data.keys())[0] != "10/12/2023" and list(data.keys())[0] != "10/13/2023" and list(data.keys())[0] != "10/14/2023" and list(data.keys())[0] != "10/15/2023" and list(data.keys())[0] != "10/16/2023" and list(data.keys())[0] != "10/17/2023" and list(data.keys())[0] != "10/18/2023":
#             company_list.append(file.replace("-news.json", ""))  
        
#         companys_scraped.append(file.replace("-news.json", ""))

# random.shuffle(company_list)

for company in company_list:
   with open(f"data-news/{company}-news.json", "r") as json_file:
        data = json.load(json_file)
        if list(data.keys())[0] == "10/12/2023" or list(data.keys())[0] == "10/13/2023" or list(data.keys())[0] == "10/14/2023" or list(data.keys())[0] == "10/15/2023" or list(data.keys())[0] == "10/16/2023" or list(data.keys())[0] == "10/17/2023" or list(data.keys())[0] == "10/18/2023" or list(data.keys())[0] == "10/19/2023":
            company_list.remove(company)

print(len(company_list))
time.sleep(2)

def chunks(input_list, num_chunks):
    """Yield successive n-sized chunks from lst."""
    if num_chunks <= 0:
        raise ValueError("Number of chunks must be greater than 0")

    avg_chunk_size = len(input_list) // num_chunks
    remainder = len(input_list) % num_chunks

    chunks = []
    current_index = 0

    for i in range(num_chunks):
        chunk_size = avg_chunk_size + (1 if i < remainder else 0)
        chunk = input_list[current_index:current_index + chunk_size]
        chunks.append(chunk)
        current_index += chunk_size

    return chunks

company_chunks = chunks(company_list, 4)

def scrape(lst): 
    for company in lst: 
        try: 
            running = True 
            click_news = True 
            last_date = None
            
            with open(f"data-news/{company}-news.json", "r") as json_file:
                data = json.load(json_file)
                if data != {}:
                    last_date = list(data.keys())[0]
                else: 
                    last_date = starting_date.strftime("%m/%d/%Y")
            
            
            driver = webdriver.Chrome(options=options)
            driver.get(f"https://www.google.com/search?q={company} news")

            try:
                time_button = driver.find_elements(By.CLASS_NAME, "QS5gu")[2]
                time_button.click()
                time.sleep(1)
            except:
                pass 

            try:
                news_button = driver.find_element(By.XPATH, "//span[text()='Nyheter']")
                news_button.click()
                time.sleep(1)  
            except:
                news_button = driver.find_elements(By.CLASS_NAME, "bmaJhd")[1]
                news_button.click()
                time.sleep(1)

            while running: 

                start_date = (datetime.datetime.strptime(last_date, "%m/%d/%Y") + datetime.timedelta(days=7)).strftime("%m/%d/%Y")
                end_date = (datetime.datetime.strptime(start_date, "%m/%d/%Y") + datetime.timedelta(days=7)).strftime("%m/%d/%Y")

                if  datetime.datetime.strptime(start_date, "%m/%d/%Y") >= org_start_date:
                    running = False

                try: 
                    if click_news == True:
                        time_button = driver.find_element(By.CLASS_NAME, "nfSF8e")
                        time_button.click()
                        time.sleep(delay) 
                        click_news = False  
                except:
                    if click_news == True:
                        for n in range(3):
                            try:                                   
                                try:
                                    time_button = driver.find_element(By.CLASS_NAME, "t2vtad")
                                    time_button.click()
                                    time.sleep(delay)
                                    break
                                except:
                                    time_button = driver.find_element(By.XPATH, "//div[text()='Verktyg']")
                                    time_button.click()
                                    time.sleep(delay)
                                    break
                            except:
                                driver.refresh()
                                time.sleep(2)
                        
                        click_news = False

                try: 
                    time_button = driver.find_elements(By.CLASS_NAME, "KTBKoe")[1]
                    time_button.click()
                    time.sleep(delay)  
                except:
                    time_button = driver.find_element(By.XPATH, "//div[text()='Senaste']")
                    time_button.click()
                    time.sleep(delay)  
                        
                try:
                    news_button = driver.find_element(By.XPATH, "//span[text()='Anpassad period...']")
                    news_button.click()
                    time.sleep(delay)  
                except:
                    driver.refresh()

                    time_button = driver.find_elements(By.CLASS_NAME, "KTBKoe")[1]
                    time_button.click()
                    time.sleep(delay) 

                    news_button = driver.find_element(By.XPATH, "//span[text()='Anpassad period...']")
                    news_button.click()
                    time.sleep(delay)  

                start_date_input = driver.find_element(By.CLASS_NAME, "OouJcb")
                start_date_input.clear()
                time.sleep(delay)

                start_date_input.send_keys(start_date)
                time.sleep(delay) 

                end_date_input = driver.find_element(By.CLASS_NAME, "rzG2be")
                end_date_input.clear()
                time.sleep(delay)

                end_date_input.send_keys(end_date)
                time.sleep(delay)  

                end_date_input.send_keys(Keys.ENTER)
                time.sleep(delay)

                todays_articles = {
                    start_date: {
                        "artical1": {
                            "title": None,
                            "snippet": None,
                            "score": None,
                        }, 
                    }  
                }

                try:
                    for i in range(1):
                        todays_articles[start_date]["artical1"]["title"] = driver.find_elements(By.CLASS_NAME, "n0jPhd")[i].text
                        todays_articles[start_date]["artical1"]["snippet"] = driver.find_elements(By.CLASS_NAME, "GI74Re")[i].text
                except:
                    print(f"\033[91mNo articles found for {company} on {start_date}\033[0m")

                    for i in range(1): 
                        todays_articles[start_date]["artical1"]["title"] = None
                        todays_articles[start_date]["artical1"]["snippet"] = None
                        todays_articles[start_date]["artical1"]["score"] = 0
                    
                    continue

                data = {**todays_articles, **data}

                with open(f"data-news/{company}-news.json", "w") as json_file: 
                    json.dump(data, json_file, indent=4)    

                if  datetime.datetime.strptime(start_date, "%m/%d/%Y") >= org_start_date:
                    running = False

                last_date = start_date
                time.sleep(1)

        except Exception as e: 
            if "https://www.google.com/sorry/index" in driver.current_url:
                print(f"\033[91mChapcha found\033[0m")
                continue
            else: 
                print(e)    
                continue

        driver.quit()

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(scrape, company_chunks)