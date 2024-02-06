import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

directory = 'news'

# List to store data
data_list = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as f:
            # Load JSON data from file
            json_data = json.load(f)
            # Empty dictionary to store data for this company
            data = {}
            # Iterate over each date in JSON data
            for date in json_data:
                # Iterate over each article in date
                for article in json_data[date]:
                    try:
                        json_data[date][article]['description']
                    except:
                        print(json_data[date][article])
                        continue

                    if json_data[date][article]['description'] != 'error' and json_data[date][article]['description'] != '' and json_data[date][article]['description'] != 'null' and json_data[date][article]['description'] != None:
                        # Add count to data dictionary
                        if date in data:
                            data[date] += 1
                        else:
                            data[date] = 1

            # Convert data dictionary to pandas DataFrame
            temp_df = pd.DataFrame(list(data.items()), columns=['Date', 'Count'])
            # Convert 'Date' column to datetime
            temp_df['Date'] = pd.to_datetime(temp_df['Date'])
            # Add company column
            temp_df['Company'] = filename
            # Append to data list
            data_list.append(temp_df)

# Concatenate all dataframes in the list
df = pd.concat(data_list)

# Pivot DataFrame to get it in the right format for a heatmap
pivot_df = df.pivot(index='Company', columns='Date', values='Count')

# Convert the DataFrame to float
pivot_df = pivot_df.apply(pd.to_numeric, errors='coerce')

# Replace NaN with 0
pivot_df = pivot_df.fillna(0)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_df, cmap='Greens')
plt.title('Number of Articles per Date')
plt.show()