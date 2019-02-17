import os
import csv
import redis
import datetime
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from urllib.request import urlopen

# Connect to redis
redis_host = os.getenv('REDIS_URL', 'localhost')
redis = redis.StrictRedis.from_url(redis_host, charset="utf-8", decode_responses=True)

# Fetch zip from bseIndia
host = "https://www.bseindia.com/download/BhavCopy/Equity/"
today = str(datetime.date.today())
year, month, day = today.split("-")
file_name = "EQ{}{}{}".format(int(day) - 2, month, year[2:])
# Print(host + file_name + "_CSV.ZIP")

# Extract the csv
resp = urlopen(host + file_name + "_CSV.ZIP")
zipfile = ZipFile(BytesIO(resp.read()))
items_file  = zipfile.open(file_name + ".CSV")

# Read CSV
items_file  = TextIOWrapper(items_file, encoding='UTF-8', newline='')
cr = csv.DictReader(items_file)

redis.flushdb()

# Create hashmaps for Searching and Sortedsets for finding top 10 stocks
all_stocks = {}
net_turnover_stocks = {}
for row in cr:
    key = row["SC_NAME"].strip()
    value = {
        "Open": row["OPEN"],
        "High": row["HIGH"],
        "Low": row["LOW"], 
        "Close": row["CLOSE"]
    }
    all_stocks[key] = value
    net_turnover_stocks[row["SC_NAME"]] = row["NET_TURNOV"]
    redis.hset("whole_data", key, str(value))

redis.zadd("turnover_based_stocks", net_turnover_stocks)
