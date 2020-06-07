# app/robo_advisor.py


import csv
import json
import os 

from dotenv import load_dotenv
import requests

load_dotenv()

def to_usd(my_price):
  # return "${0:,.2f}".format(my_price)
  return f"${my_price:,.2f}"

# INPUTS   
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

symbol = "MSFT" # TODO accept user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
# print(type(response)) #> <class 'requests.models.Response'>
# print(response.status_code) #> 200
# print(response.text) #> dictionary object 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


tsd = parsed_response["Time Series (Daily)"]

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

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_filepath, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() 
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

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



