import json 

class Interval():
	fifteenmin_step = 896
	onehour_step = 3596
	fourhour_step = 14396
	onemin_step = 58
	halfhour_step = 1796
	fivemin_step=298

	@classmethod
	def get_intervals(self,start_timestamp,end_timestamp,interval):
		intervals = []
		step = start_timestamp
		while step < end_timestamp:
			intervals.append(step)
			if interval == '15min':
				step += self.fifteenmin_step
			elif interval == '1hr':
				step += self.onehour_step
			elif interval == '4hr':
				step += self.fourhour_step
			elif interval=='1min':
				step +=self.onemin_step
			elif interval=='30min':
				step +=self.halfhour_step
			elif interval=='5min':
				step +=self.fivemin_step
			else:
				step += self.fifteenmin_step

		return intervals[1:]

class Volume():

	@staticmethod
	def get_volume_indications(intervals,data):
		total_volume = 0
		most_recent = 0
		#interval_opens = []
		#interval_closes = []
		interval_volumes = []
		interval_averages = []
		series_count=0
		interval_count =0 
		length = len(data['chart']['result'][0]['timestamp'])
		timestamps = data['chart']['result'][0]['timestamp']
		volumes=data['chart']['result'][0]['indicators']['quote'][0]['volume']
		for interval in intervals:
			interval_volume = 0.0
			for i in range(0,length):
				if float(timestamps[i]) < most_recent:
					continue

				elif float(timestamps[i]) > interval:
					break

				else:
					total_volume += float(volumes[i])
					#print(series['volume'])
					interval_volume += float(volumes[i])
					series_count += 1

			interval_volumes.append(interval_volume)
			interval_count += 1
			interval_averages.append(total_volume/interval_count) 
			most_recent = interval

		volume_indications = {}
		volume_indications['intervals'] = intervals
		volume_indications['volumes'] = interval_volumes
		volume_indications['averages'] = interval_averages

		return volume_indications
