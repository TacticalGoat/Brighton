class Interval():
	fifteenmin_step = 900
	onehour_step = 3600
	fourhour_step = 14400
	onemin_step = 58

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
		for interval in intervals:
			interval_volume = 0.0
			for series in data['series']:
				if float(series['Timestamp']) < most_recent:
					continue

				elif float(series['Timestamp']) > interval:
					break

				else:
					total_volume += float(series['volume'])
					#print(series['volume'])
					interval_volume += float(series['volume'])
					series_count += 1

			interval_volumes.append(interval_volume)
			if series_count == 0:
				interval_averages.append(0.0)
			else:
				interval_averages.append(total_volume/series_count) 
			most_recent = interval

		volume_indications = {}
		volume_indications['intervals'] = intervals
		volume_indications['volumes'] = interval_volumes
		volume_indications['averages'] = interval_averages

		return volume_indications
