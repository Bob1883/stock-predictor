import openai 
import os
import json
import time
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

openai.api_key = "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"
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

def send_request(company_name, date, title, snippet):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Rate the potential impact of an article on the stock price from -100 (highly negative) to 100 (highly positive). Any integer between -100 and 100 is acceptable, it dosent need to be even could be 43 or anything. 0 indicates no impact or if the article is not related to the stock."},
            {"role": "user", "content": f"{company_name}\n Title: {title} \n Snippet: {snippet}"},
        ],
        max_tokens=7,
        temperature=0.8
    )

# def send(company_list): 
for company_name in company_list:
    with open(f"data-news/{company_name}", "r") as json_file:
        data = json.load(json_file)

        if len(data) != 0: 
            for date in data:
                if data[date]['artical1']['score'] == None:

                    print(f"Sending {company_name} {date}")

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(send_request, company_name.split('.')[0], date, data[date]['artical1']['title'], data[date]['artical1']['snippet'])
                        try:
                            completion = future.result(timeout=3)
                        except concurrent.futures.TimeoutError:
                            print("TimeoutError")
                            os.system("py AI.py")
                            exit()

                    print(completion.choices[0].message)

                    data[date]['artical1']["score"] = completion.choices[0].message["content"]
                    print(f"Score: {data[date]['artical1']['score']}")

                    with open(f"data-news/{company_name}", "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    time.sleep(0.1)

# chunks = chunks(company_list, 7)

# # start 4 threads
# with ThreadPoolExecutor(max_workers=7) as executor:
#     executor.map(send, chunks)