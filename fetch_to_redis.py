from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from urllib.request import urlopen
import csv
import redis

r = redis.Redis(
    host='127.0.0.1',
    port=6379)

resp = urlopen("https://www.bseindia.com/download/BhavCopy/Equity/EQ070219_CSV.ZIP")
zipfile = ZipFile(BytesIO(resp.read()))

items_file  = zipfile.open('EQ070219.CSV')

items_file  = TextIOWrapper(items_file, encoding='UTF-8', newline='')
cr = csv.DictReader(items_file)

# redis 
r.flushdb()
for row in cr:
    key = row["SC_CODE"]
    value = {
        "name": row["SC_NAME"],
        "open": row["OPEN"],
        "high": row["HIGH"],
        "low": row["LOW"], 
        "close": row["CLOSE"]
    }
    r.hmset(key, value)
    
    
