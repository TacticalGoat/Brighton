import requests
import json


class Data():
	BASE_URI_PREFIX = "https://partner-query.finance.yahoo.com/v8/finance/chart/"
	BASE_URI_SUFFIX = ".NS?range=1d&interval=1m"
	
	@classmethod
	def get_url(self,symbol):
		return self.BASE_URI_PREFIX+symbol+self.BASE_URI_SUFFIX

	@staticmethod
	def get_json_data(url):
		try:
			req = requests.get(url)
			raw = req.text
			_json = raw
			return _json
		except Exception as e:
			print e
			return '{"status":"error"}'

	@classmethod
	def get_data(self,symbol):
		return json.loads(self.get_json_data(self.get_url(symbol)))

