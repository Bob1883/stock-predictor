import json
import os 
import openai

folder = "data-news/"

openai.api_key = os.getenv("OPENAI_API_KEY")

for filename in os.listdir(folder):
    company = filename.split(".")[0]

    # open the json file and load the data
    with open(f"{folder}{filename}", "r") as json_file:
        data = json.load(json_file)
    
    # data is not empty, there 
    for date in data:
        for article in data[date]:
            answer = 0 
            if data[date][article]["score"] == None: 
                title = data[date][article]["title"]
                snippet = data[date][article]["snippet"]
                
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Rate this article based on how good it is for the companys stock price. Your answer should be a number between -100 and 100, witch is the rating. 100 is the best rating, -100 is the worst rating. If the artikal is not related to the stock answer with 0. Only answer with a number, nothing else:"},
                        {"role": "user", "content": f"--{company}-- {title}: {snippet}"}
                    ]
                )
                try:
                    answer = int(completion.choices[0].text)
                except:
                    print("error")   
                # add the answer to the json file
                data[date][article]["score"] = answer

                # Save the scraped data to a JSON file
                with open(f"{folder}{filename}", "w") as json_file:
                    json.dump(data, json_file, indent=4)