from interception import  *
import keyboard
import pyperclip
import time
import json
import os 

# Set the company name and date range
prompt = "Rate this article from -100 (worst) to 100 (best) for its impact on the company's stock price. Only answer with the number:"
title = ""
snippet = ""

fail_safe = False

folder = "data-news/"

context = Interception()

def crash_system(): 
    global fail_safe
    fail_safe = True
    ff = int("crask")

# wait for esc key 
while True:
    if keyboard.is_pressed("esc"):
        break
# kill switch with keyboard package
keyboard.add_hotkey("esc", crash_system)

for filename in os.listdir(folder):
    if fail_safe:
        break
    company = filename.split(".")[0]

    # open the json file and load the data
    with open(f"{folder}{filename}", "r") as json_file:
        data = json.load(json_file)
    
    # data is not empty, there 
    for date in data:
        article = "artical1"
        if data[date][article]["score"] == None: 
            
            title = data[date][article]["title"]
            snippet = data[date][article]["snippet"]

            snippet = snippet.split("...")[0] 


            click(1050, 320, button="left", delay=0.1)

            time.sleep(0.3)

            press("tab")

            message = f"{prompt} {company} {title} {snippet}".lower()
            # send the message with keyboard package as fast as possible
            keyboard.write(message, delay=0.01)

            if fail_safe:
                break

            press("enter")

            time.sleep(0.5)

            click(560, 730, button="left", delay=0.1)
            click(560, 730, button="left", delay=0.1)

            time.sleep(0.2)

            with hold_key("ctrl"):
                press("c")
            
            time.sleep(0.2)

            answer = pyperclip.paste()

            # find second element with class "MessageItem_msg__1nYah" and get the span inside it and extract the text
            try:
                answer = int(answer)
            except:
                answer = 0

            print(answer)

            # add the answer to the json file
            data[date][article]["score"] = answer

            # Save the scraped data to a JSON file
            with open(f"{folder}{filename}", "w") as json_file:
                json.dump(data, json_file, indent=4)