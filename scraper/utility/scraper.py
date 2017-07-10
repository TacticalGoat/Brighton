import requests
import json
import httplib
import os
import sys
from datetime import datetime
from Queue import Queue
from threading import Thread
from time import sleep

class Scraper():
	__max_threads = 425
	__symbols = []
	__q = Queue(__max_threads*2)
	__failed_to_fetch = []
	__counter = 0
	__failed = 0

	@classmethod
	def do_work(self):
		while True:
			symbol = self.__q.get()
			try:
				#print "THREAD:"+symbol
				url = self.__get_url(symbol.strip())
				sleep(0.050)
				#raw_data = self.__getJsonData(url)
				data = self.__getJsonData(url)
				company = data['meta']['ticker'].split('.')[0]
				print company
				self.__counter += 1
				print "done:"+str(self.__counter)
				print "failed:"+str(self.__failed)
				self.__q.task_done()
			except KeyboardInterrupt:
				sys.exit(1)
			except Exception as e:
				print e
				self.__failed_to_fetch.append(symbol)
				self.__failed += 1
				self.__q.task_done()

	@staticmethod
	def __getJsonData(url):
		try:
			#print url
			req = requests.get(url)
			raw = req.text
			raw_data = raw[raw.find("(")+1:raw.find(")")]
			raw_data = raw_data.strip().replace(" ","")
			return json.loads(raw_data,strict=False)
		except KeyboardInterrupt:
			sys.exit(1)
		except Exception as e:
			print e
			print "failed url:" + url
			return {}

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
	def test_method(self,symbol):
		#self.__populate_symbols()
		#print self.__symbols
		url = self.__get_url(symbol)
		data = self.__getJsonData(url)
		#data = json.loads(raw_data)
		print data

	@classmethod
	def start(self):
		print "scraping initiated..."
		self.__populate_symbols()
		for i in range(self.__max_threads):
			t = Thread(target=self.do_work)
			t.daemon = True
			t.start()
		try:
			for symbol in self.__symbols:
				self.__q.put(symbol)
			print "*******************WAITING FOR JOIN********************"
			self.__q.join()
			print self.__failed_to_fetch
		except KeyboardInterrupt:
			sys.exit(1)
