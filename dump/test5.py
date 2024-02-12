from components.constants import *
from components.load_data_for_test import Load_data
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import os
import numpy as np
from keras.models import load_model

    
def clac_accuracy(y_test, y_pred):
    # get the tops and see how far appart they are. If they both are negative or positive, then give it extra points
    points = 0
    for i in range(len(y_test)):
        # see how far apart they are
        if y_pred[i] != 0:
            distence = y_test[i] / y_pred[i]

            # the closer it is to 1, the more points it gets
            distence = 1 - abs(1 - distence) 

            if distence > 0: 
                points += distence

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5
        else:
            distence = abs(y_test[i] - y_pred[i]) 
            # the closer it is to 0, the more points it gets
            distence = 1 - distence

            if distence > 0: 
                points += distence 

            if y_test[i] < 0 and y_pred[i] < 0:
                points += 0.5
            
            if y_test[i] > 0 and y_pred[i] > 0:
                points += 0.5

    points = points / len(y_test)

    print(points)

# get the company names that are both in data/data-week and data/data-google-trends and data/data-political
companies = []
for filename in os.listdir("data/data-week"):
    company_name = filename.split("-")[0]
    if os.path.isfile(f"data/data-google-trends/{company_name}-trend.json") and os.path.isfile(f"data/data-political/{company_name}-political.json"):
        companies.append(company_name)

# get the data for the companies
data = {}
raw_data = {}
for company in companies:
    loader = Load_data(period=259, company=company.lower())
    company_data = loader.get_raw_data()
    company_data['Company'] = company  # add a new column for the company
    # create new cloumn for the change in price
    company_data['change'] = 0
    average_change_down = []
    average_change_up = []
    change = 0
    
    # cahnge adj close data to change in price
    for i in range(1, len(company_data['Adj Close'])):
        change = (company_data['Adj Close'][i] / company_data['Adj Close'][i - 1]) - 1
        company_data['change'][i] = change
        if change < 0:
            average_change_down.append(change)
        else:
            average_change_up.append(change)
    
    # get the average change
    average_change_down = sum(average_change_down) / len(average_change_down)
    average_change_up = sum(average_change_up) / len(average_change_up)

    # dont let the change be more than 10% of the average change
    change_limit = 2
    for i in range(1, len(company_data['Adj Close'])):
        if company_data['change'][i] > average_change_up * change_limit:
            company_data['change'][i] = average_change_up * change_limit
        if company_data['change'][i] < average_change_down * change_limit:
            company_data['change'][i] = average_change_down * change_limit

    #costume scaler, so i want the change to be 1 if it even increases a little, and the progressively higher, 5 (or less depending on a variable) being the highest. And the same if it goes down but negative
    max_change_up = max(company_data['change'])
    max_change_down = min(company_data['change'])
    
    for i in range(1, len(company_data['Adj Close'])):
        if i == 0:
            company_data['change'][i] = 0

        if company_data['change'][i] > 0:
            # change = company_data['change'][i] / max_change_up * 5
            # # round to the nearest whole number, not 0 
            # change = round(change)
            # if change == 0:
            #     change = 1
            # company_data['change'][i] = change
            company_data['change'][i] = 1
        else:
            # change = company_data['change'][i] / max_change_down * 5
            # # round to the nearest whole number, not 0 
            # change = round(change)
            # if change == 0:
            #     change = -1
            #     company_data['change'][i] = change
            # else:
            #     company_data['change'][i] = change - 6
            company_data['change'][i] = -1


    # # # show price on a graph
    # plt.plot(company_data['change'], label="Actual")
    # plt.legend()
    # plt.show()

    data[company] = company_data


# concatenate all the data
all_data = pd.concat(data.values(), ignore_index=True)

#Variables for training
cols = list(all_data)[0:len(all_data.columns)]  
print(cols)

# convert the names to a representiver number
all_data['Company'] = all_data['Company'].astype('category').cat.codes

print(all_data)

df_for_training = all_data[cols].astype(float)

# You need to convert the 'Company' column to a format that can be used in training.
# One common approach is one-hot encoding, which can be done with pandas' get_dummies function:
df_for_training = pd.get_dummies(df_for_training)

scaler = StandardScaler()
scaler = scaler.fit(df_for_training)
df_for_training_scaled = scaler.transform(df_for_training)

print(df_for_training_scaled)

trainX = []
trainY = []

n_future = 1   # Number of weeks we want to look into the future based on the past weeks.
n_past = 10  # Number of past weeks we want to use to predict the future.

for i in range(n_past, len(df_for_training_scaled) - n_future +1):
    trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]-1])  # Exclude 'change' from input features
    trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, -1])  # Use 'change' as target variable

trainX, trainY = np.array(trainX), np.array(trainY)

# define the Autoencoder model
model = Sequential()
model.add(LSTM(units=50,return_sequences=True,input_shape=(trainX.shape[1],trainX.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))
model.compile(optimizer='adam',loss='mean_squared_error')
model.summary()
model.fit(trainX,trainY,epochs=100,batch_size=32,verbose=1)


#  save the model
model.save("models/model_1.h5")

# test the model, with tesla 
test_data = {}
loader = Load_data(period=259, company="tesla")
company_data = loader.get_raw_data()
company_data['Company'] = "tesla"  # add a new column for the company
# create new cloumn for the change in price
company_data['change'] = 0
average_change_down = []
average_change_up = []
change = 0

# cahnge adj close data to change in price
for i in range(1, len(company_data['Adj Close'])):
    change = (company_data['Adj Close'][i] / company_data['Adj Close'][i - 1]) - 1
    company_data['change'][i] = change
    if change < 0:
        average_change_down.append(change)
    else:
        average_change_up.append(change)

# get the average change
average_change_down = sum(average_change_down) / len(average_change_down)
average_change_up = sum(average_change_up) / len(average_change_up)

# dont let the change be more than 10% of the average change
change_limit = 2

for i in range(1, len(company_data['Adj Close'])):
    if company_data['change'][i] > average_change_up * change_limit:
        company_data['change'][i] = average_change_up * change_limit
    if company_data['change'][i] < average_change_down * change_limit:
        company_data['change'][i] = average_change_down * change_limit

#costume scaler, so i want the change to be 1 if it even increases a little, and the progressively higher, 5 (or less depending on a variable) being the highest. And the same if it goes down but negative
max_change_up = max(company_data['change'])
max_change_down = min(company_data['change'])

for i in range(1, len(company_data['Adj Close'])):
    if i == 0:
        company_data['change'][i] = 0

    if company_data['change'][i] > 0:
        # change = company_data['change'][i] / max_change_up * 5
        # # round to the nearest whole number, not 0 
        # change = round(change)
        # if change == 0:
        #     change = 1
        # company_data['change'][i] = change
        company_data['change'][i] = 1
    else:
        # change = company_data['change'][i] / max_change_down * 5
        # # round to the nearest whole number, not 0 
        # change = round(change)
        # if change == 0:
        #     change = -1
        #     company_data['change'][i] = change
        # else:
        #     company_data['change'][i] = change - 6
        company_data['change'][i] = -1

# # # show price on a graph
# plt.plot(company_data['change'], label="Actual")
# plt.legend()
# plt.show()
            
test_data["tesla"] = company_data

# concatenate all the data
all_test_data = pd.concat(test_data.values(), ignore_index=True)

# convert the names to a representiver number
all_test_data['Company'] = all_test_data['Company'].astype('category').cat.codes

df_for_testing = all_test_data[cols].astype(float)

# You need to convert the 'Company' column to a format that can be used in training.
# One common approach is one-hot encoding, which can be done with pandas' get_dummies function:
df_for_testing = pd.get_dummies(df_for_testing)

scaler = StandardScaler()
scaler = scaler.fit(df_for_testing)
df_for_testing_scaled = scaler.transform(df_for_testing)

print(df_for_testing_scaled)

testX = []
testY = []

for i in range(n_past, len(df_for_testing_scaled) - n_future +1):
    testX.append(df_for_testing_scaled[i - n_past:i, 0:df_for_testing.shape[1]-1])  # Exclude 'change' from input features
    testY.append(df_for_testing_scaled[i + n_future - 1:i + n_future, -1])  # Use 'change' as target variable

testX, testY = np.array(testX), np.array(testY)

# load the model
model = load_model("models/model_1.h5")

# make predictions
predictions = model.predict(testX)

# get the accuracy
clac_accuracy(testY, predictions)

# show the predictions
plt.plot(predictions, label="Predicted", linestyle="--")  # Using a solid line for Predicted
plt.plot(testY, label="Actual", linestyle="-")  # Using a dashed line for Actual
plt.legend()
plt.show()
