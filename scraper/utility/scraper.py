import requests
import json
import httplib
import os
from datetime import datetime
from Queue import Queue
from threading import Thread
from time import sleep

class Scraper():
	__max_threads = 425
	__symbols = []
	__q = Queue(__max_threads*2)

	@classmethod
	def __do_work(self):
		while True:
			symbol = self.__q.get()
			#print "THREAD:"+symbol
			url = self.__get_url(symbol)
			sleep(0.015)
			raw_data = self.__getJsonData(url)
			data = json.loads(raw_data)
			company = data['meta']['ticker'].split('.')[0]
			self.__q.task_done()

	@classmethod
	def __getJsonData(self,url):
		try:
			req = requests.get(url)
			raw = str(req.text)
			raw_data = raw[raw.find("(")+1:raw.find(")")]
			return raw_data
		except Exception as e:
			print e
			return "{}"

	@staticmethod
	def __get_url(symbol):
		url = "http://chartapi.finance.yahoo.com/instrument/1.0/"+symbol+".NS/chartdata;type=quote;range=1d/json"
		return url

	@classmethod
	def __populate_symbols(self):
		here = os.path.dirname(os.path.abspath(__file__))
		filename = os.path.join(here,"symbols.txt")
		for line in open(filename):
			self.__symbols.append(line.strip())

		print "symbols loaded..."

	@classmethod
	def start(self):
		print "scraping initiated..."
		self.__populate_symbols()
		for i in range(self.__max_threads):
			t = Thread(target=self.__do_work)
			t.daemon = True
			t.start()
		try:
			for symbol in self.__symbols:
				self.__q.put(symbol)
			self.__q.join()
		except KeyboardInterrupt:
			sys.exit(1)
