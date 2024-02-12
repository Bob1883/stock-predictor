import os
import json

# check wich ones have dates that are to ar apart
# mesed_up_companies = []
# for company in os.listdir("data-news"):
#     if company.endswith(".json"):
#         with open(f"data-news/{company}", "r") as json_file:
#             data = json.load(json_file)
#             prev_date = None
#             for date in data:
#                 if prev_date == None: 
#                     prev_date = date
#                     prev_day, prev_month, prev_year = prev_date.split('/')
#                 else:
#                     month, day, year = date.split('/')
                    
#                     # if year changes with more than 1 year
#                     if int(year) - int(prev_year) > 1 or int(year) - int(prev_year) <= -1:
#                         mesed_up_companies.append(company)
#                         break
                        
#                     # if month changes with more than 1 month
#                     if int(month) - int(prev_month) > 1 or int(month) - int(prev_month) <= -1:
#                         mesed_up_companies.append(company)
#                         break

#                     # if date changes with more than 8 days or less than 6 days
#                     if int(day) - int(prev_day) > 8 or int(day) - int(prev_day) < 6:
#                         mesed_up_companies.append(company)
#                         break

#                     prev_date = date
#                     prev_day, prev_month, prev_year = prev_date.split('/')


                
import os
import json
from datetime import datetime, timedelta

mesed_up_companies = []
messed_up_dates = []
messed_up_end_dates = []

for company in os.listdir("data-news"):
    if company.endswith(".json"):
        with open(f"data-news/{company}", "r") as json_file:
            data = json.load(json_file)
            prev_date = None
            for date in data:
                try:
                    current_date = datetime.strptime(date, "%m/%d/%Y")
                    if prev_date is not None:
                        # Calculate the difference in days between current and previous dates
                        day_difference = (current_date - prev_date).days * -1
    
                        # Check if the date difference is more than 8 days or less than 6 days
                        if day_difference > 8 or day_difference < 6:
                            print(day_difference)
                            print(company, prev_date)
                            mesed_up_companies.append(company)
                            break

                    prev_date = current_date      
                except: 
                    messed_up_dates.append(company)
                    break   
                    
            # ceck if the last date is at least 10/26/2018
            last_date = list(data.keys())[-1]
            last_date = datetime.strptime(last_date, "%m/%d/%Y")
            if last_date > datetime.strptime("11/01/2018", "%m/%d/%Y"):
                messed_up_end_dates.append(company)

               

print(mesed_up_companies)
print(len(mesed_up_companies))
print(messed_up_dates)
print(len(messed_up_dates))
print(len(messed_up_end_dates))

# delet all the messed up dates
# for company in os.listdir("data-news"):
#     if company in messed_up_dates: 
#         os.remove(f"data-news/{company}")
        
# new_data = {}
# prev_day = None 
# prev_month = None
# prev_year = None
# with open(f"data-news/Verizon-news.json", "r") as json_file:
#     data = json.load(json_file)
#     for date in data:
#         print(date)

#         day, month, year = date.split('/')

#         if prev_month == None and int(month) <= 12: 
#             prev_day = day
#             prev_month = month
#             prev_year = year
#         elif prev_month == None: 
#             prev_day = month
#             prev_month = day
#             prev_year = year

#         if int(month) <= 12:
#             if int(month) == int(prev_month):
#                 new_date = f"{month}/{day}/{year}"
#                 prev_day = day
#                 prev_month = month
#                 prev_year = year    
#             elif int(month) == int(prev_month) - 1:
#                 new_date = f"{month}/{day}/{year}"
#                 prev_day = day
#                 prev_month = month
#                 prev_year = year
#             elif int(day) == int(prev_month): 
#                 new_date = f"{day}/{month}/{year}"
#                 prev_day = day
#                 prev_month = month
#                 prev_year = year
#             elif int(day) == int(prev_month) - 1:
#                 new_date = f"{day}/{month}/{year}"
#                 prev_day = day
#                 prev_month = month
#                 prev_year = year
#             elif prev_year >= year: 
#                 if prev_month >= month:
#                     new_date = f"{month}/{day}/{year}"
#                     prev_day = day
#                     prev_month = month
#                     prev_year = year
#                 else:
#                     new_date = f"{day}/{month}/{year}"
#                     prev_day = month
#                     prev_month = day
#                     prev_year = year
#             elif prev_month > month:
#                 new_date = f"{month}/{day}/{year}"
#                 prev_day = day
#                 prev_month = month
#                 prev_year = year
#         else: 
#             new_date = f"{day}/{month}/{year}"
#             prev_day = month
#             prev_month = day
#             prev_year = year

#         new_data[new_date] = data[date]
# dates = []
# for date in new_data:
#     dates.append(date)
# print(dates)
