from flask import Blueprint
from app.mod_options.web_helper import Scraper
import json

mod_opt = Blueprint('options',__name__,url_prefix='/options')

@mod_opt.route('/<symbol>/',methods=['GET'])
def options(symbol):
	return json.dumps(Scraper.get_options(symbol),sort_keys=True,indent=4,separators=(',',': '))

