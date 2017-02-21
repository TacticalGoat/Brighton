from bs4 import BeautifulSoup
import requests
import json

class Scraper():
	base_uri = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol="

	"""
		Returns a dictionary of options after api call to yahoo
	"""
	@classmethod
	def get_options(self,symbol):
		options = {}
		options['symbol'] = symbol
		r = requests.get(self.base_uri+symbol)
		soup = BeautifulSoup(r.text)
		table = soup.find('table',id='octable')
		rows = table.find_all('tr')
		data = []
		for row in rows:
			cols = row.find_all('td')
			cols = [str(ele.text.strip()) for ele in cols]
			data.append([ele for ele in cols if ele])

		quotes = []
		for ele in data:
			if len(ele) == 21:
				call = {}
				put = {}
				strike_price = ''
				call['oi'] = ele[0]
				call['chng_in_oi'] = ele[1]
				call['volume'] = ele[2]
				call['iv'] = ele[3]
				call['ltp'] = ele[4]
				call['net_chng'] = ele[5]
				call['bid_qty'] = ele[6]
				call['bid_price'] = ele[7]
				call['ask_price'] = ele[8]
				call['ask_qty'] = ele[9]
				strike_price = ele[10]
				put['bid_qty'] = ele[11]
				put['bid_price'] = ele[12]
				put['ask_price'] = ele[13]
				put['ask_qty'] = ele[14]
				put['net_chng'] = ele[15]
				put['ltp'] = ele[16]
				put['iv']=ele[17]
				put['volume'] = ele[18]
				put['chng_in_oi'] = ele[19]
				put['oi'] = ele[20]
				quote = {}
				quote['strike_price'] = strike_price
				quote['call'] = call
				quote['put'] = put
				quotes.append(quote)
		options['quotes'] = quotes
		return options
