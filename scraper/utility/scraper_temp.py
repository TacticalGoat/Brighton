import requests
from Queue import Queue
from threading import Thread,current_thread
from time import sleep
from pymongo import MongoClient
import sys
import json

DB_NAME = "mongo_test2"
DB_COLLECTION = "intray_day_data"
BASE_URL_PREFIX = "https://partner-query.finance.yahoo.com/v8/finance/chart/"
BASE_URL_SUFFIX = ".NS?range=1d&interval=1m"
THREAD_COUNT = 350
global q
db_client = MongoClient()
db = db_client[DB_NAME]
collection = db[DB_COLLECTION]

def get_url(symbol):
    return BASE_URL_PREFIX+symbol+BASE_URL_SUFFIX

def get_symbols(symbol):
    symbols = []
    with open('cm13JAN2017bhav.csv') as f:
        for line in f:
            symbol = line.split(',')[0]
            if symbol != "SYMBOL":
                symbols.append(symbol)
    return symbols

def get_json_data(url):
    try:
        req = requests.get(url)
        raw = req.text
        return raw
    except Exception as e:
        print e
        return "{}"


def do_work():
    while True:
        symbol = q.get()
        print str(current_thread) + "started with symbol:" + symbol
        url = get_url(symbol)
        sleep(0.035)
        _json = get_json_data(url)
        try:
            data = json.loads(_json)["chart"]["result"][0]
            if "meta" in data:
                try:
                    if len(data["indicators"]["quote"][0]) == 0:
                       # print symbol + " is not supported :("
                        return
                    try:
                        doc = collection.find({"symbol":symbol})[0]
                        if "last_timestamp" in doc:
                            for index,timestamp in enumerate(data["timestamp"]):
                                if int(timestamp) > int(doc["last_timestamp"]):
                                    res = collection.update_one({"symbol":symbol},
                                                                {"$push":{"timestamps":timestamp,
                                                                          "open":data["indicators"]["quote"][0]["open"][index],
                                                                          "close":data["indicators"]["quote"][0]["close"][index],
                                                                          "volume":data["indicators"]["quote"][0]["volume"][index],
                                                                          "low":data["indicators"]["quote"][0]["low"][index],
                                                                          "high":data["indicators"]["quote"][0]["high"][index],
                                                                         }
                                                            },True)
                                  #  print "successfully updated:" + symbol
                    except TypeError:
                        print symbol + ":has type error"
                    except IndexError:
                        insert_data = {}
                        insert_data["symbol"] = symbol
                        insert_data["last_timestamp"] = data["timestamp"][-1:][0]
                        insert_data["timestamps"] = data["timestamp"]
                        insert_data["open"] = data["indicators"]["quote"][0]["open"]
                        insert_data["close"] = data["indicators"]["quote"][0]["close"]
                        insert_data["volume"] = data["indicators"]["quote"][0]["volume"]
                        insert_data["low"] = data["indicators"]["quote"][0]["low"]
                        insert_data["high"] = data["indicators"]["quote"][0]["high"]
                        result = collection.insert_one(insert_data)
                        print symbol + " succsessfully added to collection"
                        print result.inserted_id

                except KeyError:
                    pass
                   # print "Somehow key error for " + symbol
        except IndexError:
            pass
           # print "No Result for " + symbol
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    q = Queue(THREAD_COUNT*2)
    symbols = []
    with open("symbols.txt") as f:
        for line in f:
            symbols.append(line.strip())
    for i in xrange(THREAD_COUNT):
        t = Thread(target=do_work)
        t.daemon = True
        t.start()
    while True
        try:
            for symbol in symbols:
                q.put(symbol)
            q.join()
        except KeyboardInterrupt:
            sys.exit(1)