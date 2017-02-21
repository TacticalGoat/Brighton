import requests
import json


class Indicator():
	BASE_URI_PREFIX = "http://chartapi.finance.yahoo.com/instrument/1.0/"
	BASE_URI_SUFFIX = ".NS/chartdata;type=quote;range=1d/json"

	@classmethod
	def get_url(self,symbol):
		return self.BASE_URI_PREFIX+symbol+self.BASE_URI_SUFFIX