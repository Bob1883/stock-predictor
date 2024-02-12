from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import random
import os
import json

years = 5
delay = 0.5
from_date = "2023-10-20"

# Set the company name and date range
company_list = ['Tata Consultancy Services', 'Amgen', 'ConocoPhillips']
org_start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")

with open("webscraping/avalible_proxies.txt", "r") as txt_file:
    proxy_list = txt_file.read()

with open("webscraping/used_proxies.txt", "r") as txt_file:
    used_proxies = txt_file.read()

proxy_list = proxy_list.split("\n")
used_proxies = used_proxies.split("\n")

# check what companies are already scraped
for file in os.listdir("data-news"):
    try:
        if file.endswith(".json"):
            with open(f"data-news/{file}", "r") as json_file:
                data = json.load(json_file)
            if len(data) >= int(years*52):
                    print(f"Already scraped {file.replace('-news.json', '')}")
                    try:
                        company_list.remove(file.replace("-news.json", ""))
                    except:
                        # convert first letter to uppercase
                        name = file.replace("-news.json", "")
                        name = name[0].upper() + name[1:]
                        company_list.remove(name)    
    except:
        pass

random.shuffle(company_list)

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

company_chunks = chunks(company_list, 10)
proxy_chunks = chunks(proxy_list, 10)

def scrape_company(args):
    company_list, proxy_list, from_date = args
    PROXY = proxy_list[0]
    used_proxies.append(PROXY)
    for company_name in company_list:
        company_data = {}
        retries = 0
        while retries < 5:
            reload_attempts = 0
            try:
                try:
                    options = webdriver.ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument("--disable-extensions")
                    options.add_argument("--incognito")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-infobars")
                    options.add_argument('--proxy-server=%s' % PROXY)
                    # options.add_argument('--headless')

                    # make the network speed faster
                    options.add_argument('--blink-settings=imagesEnabled=false')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_argument('--page-load-strategy=eager')

                    prefs = {
                    "profile.managed_default_content_settings.images": 2, 
                    "profile.managed_default_content_settings.stylesheets": 2, 
                    "profile.managed_default_content_settings.cookies": 2, 
                    "profile.managed_default_content_settings.javascript": 1, 
                    "profile.managed_default_content_settings.media_stream": 2
                    }
                    
                    if os.path.isfile(f"data-news/{company_name}-news.json"):
                        with open(f"data-news/{company_name}-news.json", "r") as json_file:
                            data = json.load(json_file)
                            company_data = data

                            # change from_date to the last date scraped
                            try:
                                from_date = list(data.keys())[-1]
                                from_date = from_date.split("/")
                                from_date = f"{from_date[2]}-{from_date[0]}-{from_date[1]}"
                            except:
                                from_date = org_start_date.strftime("%Y-%m-%d")

                    else:
                        data = {}

                    try: 
                        test_date = (datetime.datetime.strptime(from_date, "%Y-%m-%d") - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
                    except:
                        from_date = org_start_date.strftime("%Y-%m-%d")

                    if len(data) >= int(years*52):
                        print(f"Already scraped {company_name}")
                        return
                    
                    

                    time.sleep(1)
                    driver = webdriver.Chrome(options=options, desired_capabilities=prefs)
                    driver.get(f"https://www.google.com/search?q={company_name} news")

                    time.sleep(1)

                    loading = True

                    while loading:
                        if len(driver.find_elements(By.CLASS_NAME, "QS5gu")) > 0 or len(driver.find_elements(By.CLASS_NAME, "bmaJhd")) > 0 or len(driver.find_elements(By.XPATH, "//span[text()='Nyheter']")) > 0:
                            print(f"\033[93mLoading\033[0m")
                            with open("webscraping/working_proxies.txt", "a") as txt_file:
                                txt_file.write(PROXY + "\n")
                            reload_attempts = 0
                            loading = False
                        elif "https://www.google.com/sorry/index" in driver.current_url:
                            print(f"\033[91mChapcha found\033[0m")
                            int("crash")
                        elif len(driver.find_elements(By.ID, "main-frame-error")) > 0:
                            if reload_attempts < 3:
                                print(f"\033[93mReload\033[0m")
                                driver.refresh()
                                reload_attempts += 1
                            else:
                                reload_attempts = 0
                                print(f"\033[91mProxy to slow\033[0m")
                                int("crash")

                        time.sleep(10)

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

                    for n in range(int(years*52) - len(data)):
                        try:
                            start_date = (datetime.datetime.strptime(from_date, "%Y-%m-%d") - datetime.timedelta(days=(1 + n)*7)).strftime("%Y-%m-%d")

                            start = start_date.split("-")
                            start = f"{start[1]}/{start[2]}/{start[0]}"
                            start = (datetime.datetime.strptime(start, "%m/%d/%Y") - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

                            if start in data:
                                print(f"Date {start_date} already scraped")
                                continue

                            try: 
                                if n == 0:
                                    time_button = driver.find_element(By.CLASS_NAME, "nfSF8e")
                                    time_button.click()
                                    time.sleep(delay)  
                            except:
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
                                # there is somthing wrong with the page so reload it
                                driver.refresh()

                                time_button = driver.find_elements(By.CLASS_NAME, "KTBKoe")[1]
                                time_button.click()
                                time.sleep(delay) 

                                news_button = driver.find_element(By.XPATH, "//span[text()='Anpassad period...']")
                                news_button.click()
                                time.sleep(delay)  

                            start_date_input = driver.find_element(By.CLASS_NAME, "OouJcb")
                            start_date = start_date.split("-")
                            start_date = f"{start_date[1]}/{start_date[2]}/{start_date[0]}"
                            start_date_input.clear()
                            start_date_input.send_keys(start_date)
                            time.sleep(delay) 

                            end_date_input = driver.find_element(By.CLASS_NAME, "rzG2be")
                            end_date = (datetime.datetime.strptime(from_date, "%Y-%m-%d") - datetime.timedelta(days=(n)*7)).strftime("%Y-%m-%d")
                            end_date = end_date.split("-")
                            end_date = f"{end_date[1]}/{end_date[2]}/{end_date[0]}"
                            end_date_input.clear()
                            end_date_input.send_keys(end_date)
                            time.sleep(delay)  

                            apply_button = driver.find_element(By.CLASS_NAME, "Ru1Ao")
                            apply_button.click()
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
                                    todays_articles[start_date][f"artical{i+1}"]["title"] = driver.find_elements(By.CLASS_NAME, "n0jPhd")[i].text
                                    todays_articles[start_date][f"artical{i+1}"]["snippet"] = driver.find_elements(By.CLASS_NAME, "GI74Re")[i].text
                            except:
                                for i in range(1): 
                                    todays_articles[start_date][f"artical{i+1}"]["title"] = None
                                    todays_articles[start_date][f"artical{i+1}"]["snippet"] = None
                                    todays_articles[start_date][f"artical{i+1}"]["score"] = 0
                            time.sleep(delay) 

                            data.update(todays_articles)

                            # Save the scraped data to a JSON file
                            with open(f"data-news/{company_name}-news.json", "w") as json_file:
                                json.dump(data, json_file, indent=4)

                            company_data = data
    
                        except Exception as e:
                            if "does not match format '%Y-%m-%d'" in str(e):
                                print(f"\033[95m{company_name} has wrong format\033[0m")
                                time.sleep(5)
                                int("crash")

                            if e == "list index out of range":
                                time.sleep(1)
                                if reload_attempts < 3:
                                    print(f"\033[93mReload\033[0m")
                                    driver.refresh()
                                    reload_attempts += 1
                                else:
                                    reload_attempts = 0
                                    print(f"\033[91mProxy to slow\033[0m")
                                    int("crash")

                            if "https://www.google.com/sorry/index" in driver.current_url:
                                print(f"\033[91mChapcha found\033[0m")
                                int("crash")

                            if reload_attempts < 3:
                                print(f"\033[93mReload\033[0m")
                                driver.refresh()
                                reload_attempts += 1
                            else:
                                reload_attempts = 0
                                print(f"\033[91m{e}\033[0m")
                
                    driver.quit()

                except:
                    old_proxy = PROXY
                    used_proxies.append(PROXY)

                    for proxy in proxy_list:
                        if proxy not in used_proxies:
                            with open("webscraping/used_proxies.txt", "a") as txt_file:
                                txt_file.write(PROXY + "\n")
                            PROXY = proxy
                            driver.quit()
                            break

                if old_proxy == PROXY:
                    print(f"\033[91mNo proxy working\033[0m")
                    driver.quit()
                    int("crash")

            except:
                retries += 1
                print(f"\033[91m{company_name} crashed\033[0m")
                pass
    
    print(f"\033[95m{company_name} is done\033[0m")
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrape_company, zip(company_chunks, proxy_chunks, from_date))