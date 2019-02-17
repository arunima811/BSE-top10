from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from urllib.request import urlopen
import os
import csv
import redis
import json
import datetime

redis_host = os.getenv('REDIS_URL', 'localhost')

r = redis.Redis(
    host=redis_host,
    port=6379)
redisClient = redis.StrictRedis(
    host=redis_host,
    port=6379)

host = "https://www.bseindia.com/download/BhavCopy/Equity/"
today = str(datetime.date.today())
year, month, day = today.split("-")

file_name = "EQ{}{}{}".format(int(day) - 2, month, year[2:])
print(host + file_name + "_CSV.ZIP")
resp = urlopen(host + file_name + "_CSV.ZIP")
zipfile = ZipFile(BytesIO(resp.read()))

items_file  = zipfile.open(file_name + ".CSV")
items_file  = TextIOWrapper(items_file, encoding='UTF-8', newline='')
cr = csv.DictReader(items_file)

# redis 
r.flushdb()
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
    redisClient.hset("whole_data", key, str(value))
    # redisClient.zadd("turnover_based_stocks", row["NET_TURNOV"], row["SC_NAME"])
# redisClient.hmset("whole_data", all_stocks)
redisClient.zadd("turnover_based_stocks", net_turnover_stocks)
