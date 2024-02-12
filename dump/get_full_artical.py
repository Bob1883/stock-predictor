from gnews import GNews
import json 
import os 
import datetime
from concurrent.futures import ThreadPoolExecutor
import random
# from textblob import TextBlob

names = []

for file in os.listdir("data-news"):
    if file.endswith(".json"):
        names.append(file.split("-")[0])


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

company_chunks = chunks(names, 4)

# randomize the order of the companies
for chunk in company_chunks:
    random.shuffle(chunk)

print(company_chunks)

def scrape(lst):

    googlenews = GNews(language="en", max_results=7)

    for company in lst:
        data = {}
        print(company)

        if os.path.isfile(f"data-news2/{company}-news.json"):
            with open(f"data-news2/{company}-news.json", "r") as json_file:
                data = json.load(json_file)
        
        for date in data:
            
            for article in data[date]:  
                try:
                    try: 
                        test = data[date][article]["description"]
                    except:
                        arc = googlenews.get_full_article(data[date][article]["link"])

                        if arc == "":
                            arc = "No description"

                        # extract the article text from the article object
                        description = arc.text

                        print(description)
                        # remove \n from the description
                        description = description.replace("\n", "")
                    
                        data[date][article]["description"] = description

                        with open(f"data-news2/{company}-news.json", "w") as json_file:
                            json.dump(data, json_file, indent=4)
                except:
                    # add erroe to description
                    data[date][article]["description"] = "error"

                    with open(f"data-news2/{company}-news.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    print("error")
                    pass
            
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(scrape, company_chunks)