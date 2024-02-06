import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

from gensim.summarization import summarize

# for removeing illegal characters
import re

from get_sentment import estimate_sentiment

directory = 'news'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as f:
            # Load JSON data from file
            json_data = json.load(f)
            for date in json_data:
                for article in json_data[date]:
                    try: 
                        
                        # if score is not null, skip 
                        try:
                            score = json_data[date][article]['probability']
                            if score != None:
                                continue
                        except:
                            pass

                        description = json_data[date][article]['description']
                        # if there is no space after the period, add one
                        description = description.replace('.','. ')
                        # remove double spaces
                        description = description.replace('  ',' ')

                        if description == 'error' or description == '' or description == 'null' or description == None:
                            continue

                        description = re.sub(r'[^\x00-\x7F]+',' ', description)
                        summary = summarize(description)
                        summary = description[:2000]

                        summary = summary.rsplit(' ', 1)[0]

                        print(summary)
                        try:
                            probability, sentiment = estimate_sentiment(summary)
                        except:
                            summary = summary[:1600]
                            probability, sentiment = estimate_sentiment(summary)

                        probability = probability.item()  # Convert tensor to float

                        print(probability, sentiment) 

                        # add data to json
                        json_data[date][article]['probability'] = probability
                        json_data[date][article]['sentiment'] = sentiment

                        # time.sleep(1)
                        # print(json_data[date][article])

                                        # write data to json
                        with open(os.path.join(directory, filename), 'w') as f:
                            json.dump(json_data, f, indent=4)

                    except Exception as e:
                        # print in red 
                        print(e)
                        print('\033[91m' + 'Error on ' + filename + ' ' + date + ' ' + article + '\033[0m')
                        continue
