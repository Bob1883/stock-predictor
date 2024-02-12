from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime, timedelta
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
org_start_date = datetime.strptime("10/13/2023", "%m/%d/%Y")
starting_date = datetime.strptime("10/26/2018", "%m/%d/%Y") 

company_list = []

for company in os.listdir("data-news"):
    if company.endswith(".json"):
        with open(f"data-news/{company}", "r") as json_file:
            data = json.load(json_file)

            # ceck if the last date is at least 10/26/2018
            last_date = list(data.keys())[-1]
            last_date = datetime.strptime(last_date, "%m/%d/%Y")
            if last_date > datetime.strptime("11/01/2018", "%m/%d/%Y"):
                company_list.append(company.replace("-news.json", ""))


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

            last_date = list(data.keys())[-1]
            
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

                start_date = (datetime.strptime(last_date, "%m/%d/%Y") - timedelta(days=7)).strftime("%m/%d/%Y")
                end_date = (datetime.strptime(start_date, "%m/%d/%Y") - timedelta(days=7)).strftime("%m/%d/%Y")

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

                data.update(todays_articles)

                with open(f"data-news/{company}-news.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)    

                last_date = datetime.strptime(last_date, "%m/%d/%Y")
                if last_date < datetime.strptime("11/01/2018", "%m/%d/%Y"):
                    running = False

                last_date = start_date

        except Exception as e: 
            print(e)
            time.sleep(1)
            if "https://www.google.com/sorry/index" in driver.current_url:
                print(f"\033[91mChapcha found\033[0m")
                continue
            else: 
                print(e)    
                continue
                
        driver.quit()


with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(scrape, company_chunks)