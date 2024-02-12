import json
import os
import requests
from requests.exceptions import ConnectionError, RequestException, Timeout
from concurrent.futures import ThreadPoolExecutor

# Load proxy list from the txt file
with open("proxys.txt", "r") as txt_file:
    proxy2 = txt_file.read()

proxy2 = proxy2.split("\n")
proxy2 = [proxy.split(":") for proxy in proxy2]
proxy_list = [{"ip": proxy[0], "port": proxy[1]} for proxy in proxy2]

# find the second ip and port 176.124.199.65:3128 from the list
index = 0
for proxy in proxy_list:
    if proxy["ip"] == "176.124.199.65" and proxy["port"] == "3128":
        index += 1
        if index == 1: 
            #reomove the duplicate
            proxy_list.remove(proxy)
        if index == 2:
            # remove all the proxies before this one
            proxy_list = proxy_list[proxy_list.index(proxy):]


# Define the URL you want to test (e.g., "https://www.google.com")
test_url = "https://www.google.com"

# Function to check if a proxy is available
def is_proxy_available(proxy):
    print(f"Checking {proxy['ip']}:{proxy['port']}")
    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
    try:
        response = requests.get(test_url, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
        if response.status_code == 200:
            return proxy_url
    except (ConnectionError, RequestException, Timeout):
        pass
    return None

avalible_proxies = []
# Use ThreadPoolExecutor to check multiple proxies at once
with ThreadPoolExecutor(max_workers=10) as executor:
    for proxy_url in executor.map(is_proxy_available, proxy_list):
        if proxy_url:
            print(f"\033[93mFound available proxy: {proxy_url}\033[0m")
            avalible_proxies.append(proxy_url)
            # add to a txt file 
            with open("avalible_proxies.txt", "a") as txt_file:
                txt_file.write(proxy_url + "\n")
    else:
        print("No available proxies found.")

print(avalible_proxies)