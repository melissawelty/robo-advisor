# app/robo_advisor.py


import csv
import json
import os 

import requests

def to_usd(my_price):
  # return "${0:,.2f}".format(my_price)
  return f"${my_price:,.2f}"

# INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"

response = requests.get(request_url)
# print(type(response)) #> <class 'requests.models.Response'>
# print(response.status_code) #> 200
# print(response.text) #> dictionary object 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]



tsd = parsed_response["Time Series (5min)"]

dates = list(tsd.keys()) #sort to ensure latest day is first, assuming latest day is first 

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]


#max of all high prices


high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))


recent_high = max(high_prices) 
recent_low = min(low_prices)

# OUTPUTS
 
csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_filepath, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") ##datetime module 
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!") # conditions for recommendation 
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_filepath}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



