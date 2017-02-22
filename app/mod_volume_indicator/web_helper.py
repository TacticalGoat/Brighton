import requests
import json


class Data():
	BASE_URI_PREFIX = "http://chartapi.finance.yahoo.com/instrument/1.0/"
	BASE_URI_SUFFIX = ".NS/chartdata;type=quote;range=1d/json"
	
	@classmethod
	def get_url(self,symbol):
		return self.BASE_URI_PREFIX+symbol+self.BASE_URI_SUFFIX

	@staticmethod
	def get_json_data(url):
		try:
			req = requests.get(url)
			raw = req.text
			_json = raw[raw.find("(")+1:raw.find(")")]
			return _json
		except Exception as e:
			print e
			return '{"status":"error"}'

	@classmethod
	def get_data(self,symbol):
		return json.loads(self.get_json_data(self.get_url(symbol)))