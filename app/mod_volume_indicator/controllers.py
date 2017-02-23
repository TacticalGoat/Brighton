from flask import Blueprint,request,render_template, \
				  flash, session, redirect, url_for
import requests
import time
import json
import pytz
from datetime import datetime,timedelta,time as dtime
from app.mod_volume_indicator.interval_helper import Interval,Volume
from app.mod_volume_indicator.web_helper import Data

mod_vi = Blueprint('volume_indicator',__name__,url_prefix='/volumes')

@mod_vi.route('/<interval>/<symbol>/',methods=['GET'])
def volumes(interval,symbol):
	"""
		Tried to do utc but apparently I dont understand it enough so for 
		now bodged together so should work now
	"""
	today = datetime.utcnow()
	current_time = today.time()
	daily_start_time = dtime(3,45)
	daily_end_time = dtime(10,15)
	volume_indicator = {} 
	start_timestamp = 0
	end_timestamp = 0
	if current_time < daily_start_time:
		yesterday = today - timedelta(days=1)
		start_timestamp = time.mktime(datetime(yesterday.year,yesterday.month,yesterday.day,
													9,15,0,0,tzinfo=pytz.UTC).timetuple())
		end_timestamp = time.mktime(datetime(yesterday.year,yesterday.month,yesterday.day,
													15,45,0,0,tzinfo=pytz.UTC).timetuple())
		intervals = Interval.get_intervals(start_timestamp,end_timestamp,interval)
		data = Data.get_data(symbol)
		volume_indicator = Volume.get_volume_indications(intervals,data)

	elif current_time > daily_end_time:
		start_timestamp = time.mktime(datetime(today.year,today.month,today.day,9,15,0,0,
										tzinfo=pytz.UTC).timetuple())
		end_timestamp = time.mktime(datetime(today.year,today.month,today.day,15,45,0,0,
										tzinfo=pytz.UTC).timetuple())
		intervals = Interval.get_intervals(start_timestamp,end_timestamp,interval)
		data = Data.get_data(symbol)
		volume_indicator = Volume.get_volume_indications(intervals,data)

	else:

		start_timestamp = time.mktime(datetime(today.year,today.month,today.day,9,15,0,0,
											tzinfo=pytz.UTC).timetuple())
		current_time = datetime.now()
		end_timestamp = time.mktime(datetime(today.year,today.month,today.day,current_time.hour,
												current_time.minute,0,0,tzinfo=pytz.UTC).timetuple())
		intervals = Interval.get_intervals(start_timestamp,end_timestamp,interval)
		data = Data.get_data(symbol)
		volume_indicator = Volume.get_volume_indications(intervals,data)

	return json.dumps(volume_indicator,sort_keys=True,indent=4,separators=(',',': '))