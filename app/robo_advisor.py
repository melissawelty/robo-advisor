# app/robo_advisor.py


import csv
import json
import os 

from dotenv import load_dotenv
import requests

from datetime import datetime

import matplotlib.pyplot as plt


load_dotenv()

def to_usd(my_price):
  # return "${0:,.2f}".format(my_price)
  return f"${my_price:,.2f}"

# INPUTS   

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

symbol = input("Please enter a stock symbol and press enter:")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)



if 'Error' in response.text:
    print("Invalid Symbol. Please enter valid stock symbol.")
    exit()

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
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
now = datetime.now()
date_time = now.strftime("%D, %r")
print("REQUEST AT:" + date_time)  
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
if float(latest_close) > (float(recent_high) * .75):
    print("RECOMMENDATION: DON'T BUY! The stock price is too high and not a good investment.")
elif float(latest_close) < (float(recent_low) * 1.15):
    print("RECOMMENDATION: BUY AND HOLD! The price is low and could generate high returns when it increases!")
else:
    print("RECOMMENDATION: DON'T BUY! Keep watching, this could be a potential buy soon..")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_filepath}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


x = []
y = []

with open(csv_filepath, 'r') as csvfile:
    plots=csv.reader(csvfile, delimiter=",")
    for row in plots:
        x.append(row(str('timestamp'))) 
        y.append(row[float('close')])

plt.plot(x,y,marker='o')

plt.title('Data from Prices')

plt.xlabel('Date')
plt.ylabel('Price')

plt.show()



