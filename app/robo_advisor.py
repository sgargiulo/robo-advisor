# app/robo_advisor.py

import csv
import json
import os
import pandas
from dotenv import load_dotenv

import requests
import datetime

load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price) 
#
# INFO INPUTS
#

api_key = os.environ.get("ALPHAVANTAGE_API_KEY") #directs to env file to obtain api key

symbol = input("PLEASE ENTER STOCK SYMBOL (EX: AAPL) AND PRESS ENTER: ") #"MSFT"

number =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

if str(number) in symbol:   #prevents HTML request for numberic entry
    print("OH MAN....WE COULDN'T FIND ANY TRADING ACTIVITY FOR THAT SYMBOL. TRY AGAIN USING A VALID STOCK SYMBOL LIKE AAPL")
    exit()

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)  #this turns string into dictionary

if "Error Message" in parsed_response:   #this validates stock symbol is locted on url
    print("OH MAN....WE COULDN'T FIND ANY TRADING ACTIVITY FOR THAT SYMBOL. TRY AGAIN USING A VALID STOCK SYMBOL LIKE AAPL")
    exit()

last_refreshed  = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())    #assuming latest day is first on list

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

# get high price from each day
#high_prices = [ 10, 20, 30]
#recent_high = max(high_prices)

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO OUTPUT 
#

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates: 
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["6. volume"],
        })

now = datetime.datetime.now()


# TODO: stock recommentation 

if float(latest_close) < .90 * float(recent_high) and float(latest_close) < .98 * float(tsd[latest_day]["2. high"]):
    stock_recommendation = "BUY"
    recommendation_reason = "Current Stock Price is less than 90 percent of recent high over the last 100 trading days and less than 98 percent of the current daily high"
else: 
    stock_recommendation = "DON'T BUY"
    recommendation_reason = "Current Stock Price is greater than 90 percent of recent high over the last 100 trading days and/ or greater than 98 percent of the current daily high"



print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %H:%M"))   #https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") 
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: " + stock_recommendation)
print("RECOMMENDATION REASON: " + recommendation_reason)
print("-------------------------")
print("Writing Data to: " + csv_file_path)
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


