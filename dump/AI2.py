from gnews import GNews
import os
import json
from concurrent.futures import ThreadPoolExecutor
from textblob import TextBlob

company_list = []

for company in os.listdir("data-news"):
    if company.endswith(".json"):
        company_list.append(company)

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

def send(company_list): 
    for company_name in company_list:
        with open(f"data-news/{company_name}", "r") as json_file:
            data = json.load(json_file)

            if len(data) != 0: 
                for date in data:
                    if data[date]['artical1']['score'] == None:

                        print(f"Sending {company_name} {date}")

                        googlenews = GNews(language="en")

                        # get full article
                        for n in range(7):
                            full_article = googlenews.get_full_article(data[date][f"artical{n+1}"]['link'])

                            # get sentiment
                            sentiment = TextBlob(full_article).sentiment.polarity

                            # add to data
                            data[date][f"artical{n+1}"]['score'] = sentiment
                            # add the full article
                            data[date][f"artical{n+1}"]['full_article'] = full_article
                        
                        # save data
                        with open(f"data-news/{company_name}", "w") as json_file:
                            json.dump(data, json_file, indent=4)                    


chunks = chunks(company_list, 4)

# start 4 threads
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(send, chunks)