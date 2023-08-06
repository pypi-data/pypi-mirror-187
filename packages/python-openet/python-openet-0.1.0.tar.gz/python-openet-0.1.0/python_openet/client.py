
"""
docs: https://open-et.github.io/docs/build/html/index.html

swagger_api: https://openet.dri.edu/docs
"""


#%% Imports
from calendar import month
import geopandas as gpd
# from shapely.geometry import LineString
import pandas as pd
import requests
import json

from requests.adapters import HTTPAdapter, Retry



pd.options.display.float_format = '{:,.0f}'.format

class User:
	"""
	Tracks overall api usage and sets up the session for the subclasses
	"""
	def __init__(self,api_key,options,fields=None,area=None) -> None:
		header = {"Authorization": api_key}
		self.S = requests.Session()
		
		retries = Retry(total=5,backoff_factor=0.1,status_forcelist=[ 500, 502, 503, 504 ])
		self.S.mount('http://', HTTPAdapter(max_retries=retries))
		self.S.mount('https://', HTTPAdapter(max_retries=retries))

		self.S.headers.update(header)

		self.options = options
		self.area = area
		if area is not None:
			self.boundary = area.boundary
			self.coordinates = self.coordinates_from_boundary()



		self.fields = fields
		if self.fields is not None:
			# self.field_splits = [self.fields[s:s+1400] for s in range(0,((len(self.fields) // 1400 )+1) * 1400,1400)]
			self.field_splits = [self.get_field_ids_from_fields(self.fields[s:s+1400]) for s in range(0,((len(self.fields) // 1400 )+1) * 1400,1400)]
			# self.field_ids = self.get_field_ids_from_fields(field_split)


		self.starting_quota = self.check_quota()
	# def __call__(self):

		
	def check_quota(self):
		"""Get field ids in region of interest"""
		url = 'https://openet.dri.edu/home/user/quotas'
		R = self.S.get(url)
		J = json.loads(R.text)
		df = pd.DataFrame(J.values(),index=J.keys(),columns=['Quota'])
		return df
	
	
	# TODO: check quota before and after an api call to determine what changed
	def quota_change(self):
		# qc =  self.starting_quota.compare(self.check_quota(),result_names=('Starting', 'Current'))
		# qc['Change'] = qc['Quota']['Starting'] - qc['Quota']['Current']
		qc =  self.starting_quota.compare(self.check_quota())
		qc['Change'] = qc['Quota']['self'] - qc['Quota']['other']
		return qc


	def get_options(self,current_options):
		# current_options = ['model','interval']
		return {k:v for k,v in self.options.items() if k in current_options}


	def coordinates_from_boundary(self):
		coords = [f"{i} {j}" for i,j in self.boundary[0].coords]
		coordinate_list = ', '.join(coords)
		return coordinate_list

	def get_field_ids_from_fields(self,fields):
		middle = '\",\"'.join(fields)
		field_ids = f'["{middle}"]'
		return field_ids

	def make_bite_size(self,func):
		"""
		Make requests in chunks of 1400 fields at a time (The limit is 1500 at in one request)

		func = function that takes field_ids as its input
		"""
		# total_df = pd.DataFrame()
		all_dfs = []
		# field_splits = [self.fields[s:s+1400] for s in range(0,((len(self.fields) // 1400 )+1) * 1400,1400)]
		for field_split in self.field_splits:
			field_ids = self.get_field_ids_from_fields(field_split)
			data = func(field_ids)
			df = pd.DataFrame(data)
			all_dfs.append(df)
		total_df = pd.concat(all_dfs)
		return total_df



	def field_ids_in_ROI(self):
		"""Get field ids in region of interest"""
		url = 'https://openet.dri.edu/metadata/openet/region_of_interest/feature_ids_list'
		my_obj = {
			"coordinates": f"{self.coordinates}",
			# intersect gives all within and touching boundary
			"spatial_join_type": "intersect"
			}

		R = self.S.post(
			url,
			json=my_obj,
			verify=True
			)
		print(my_obj)
		print(R)
		J = json.loads(R.text)
		return J

	def get_raster_data(self):
		"""
		due to limited resources there is a 31 day extraction limit and 2000 acre area limit at this time.
		"""
		url = f"https://openet.dri.edu/raster/timeseries/polygon"

		cols = [
			"start_date",
			"end_date",
			"interval",
			"units",
			"model",
			"output_file_format",
		]
		my_obj = self.get_options(cols)

		# my_obj = {
		# "start_date": "2018-01-01",
		# "end_date": "2018-12-31",
		# "interval": "monthly",
		# "units": "english",
		# "model": "ensemble",
		# "output_file_format": "json",
		# }
		R = self.S.post(
			url,
			json=my_obj,
			verify=True
			)
		try:
			J = json.loads(R.text)
			return J
		except:
			return R


	def get_field_metadata(self,field_ids):
		"""Get field metadata"""
		base_url = f"https://openet.dri.edu/metadata/openet/features"
		url = f"{base_url}"

		my_obj = json.dumps({"field_ids": field_ids},indent=1)
		R = self.S.post(
			url,
			json=my_obj,
			verify=True,
			)
		print(my_obj)
		print(R)
		J = json.loads(R.text)
		return J
	
	def get_field_metadata_small(self,my_obj):
		base_url = f"https://openet.dri.edu/metadata/openet/features"
		url = f"{base_url}"

		# my_obj = json.dumps({"field_ids": field_ids})
		R = self.S.post(
			url,
			json=my_obj,
			verify=True,
			)
		print(my_obj)
		print(R)
		J = json.loads(R.text)
		return J


	def get_monthly_data(self,field_ids):
		url = f"https://openet.dri.edu/timeseries/features/monthly"
		cols = [
			"model",
			"variable",
			"start_date",
			"end_date",
			"field_ids",
			"output_format",
			"units",
		]
		my_obj = self.get_options(cols)
		my_obj["field_ids"] = field_ids

		# my_obj = {	
		# 	"model": "ensemble_mean",
		# 	"variable": "et",
		# 	"start_date": "2018-01-01",
		# 	"end_date": "2018-03-31",
		# 	"field_ids": field_ids,
		# 	"output_format": "json",
		# 	"units": "english"
		# 	}
		# url = f"https://openet.dri.edu/timeseries/features/monthly?model={O['model']}&variable={O['variable']}&field_ids={fields}&units=english&start_date=2018-01-01&end_date=2018-06-30&output_format=json"
		R = self.S.post(
			url,
			json=my_obj,
			# headers=header,
			verify=True
			)
		J = json.loads(R.text)
		return J

	def get_yearly_data(self):
		"""Max request = 1500"""
		url = f"https://openet.dri.edu/timeseries/features/annual"
		# url = f"https://openet.dri.edu/timeseries/features/stats/annual"
		# url = f"https://openet.dri.edu/timeseries/features/aggregate/annual"
			
		my_obj = {
			'feature_collection_name':"CA",
			# "field_ids": field_ids,
			"model": "ensemble_mean",
			"variable": "et",
			# "start_date": "2018-01-01",
			# "end_date": "2018-12-31",
			# "aggregation":"mean",
			"start_date": "2018",
			"end_date": "2018",
			"output_format": "json",
			"units": "english"
			}
		R = self.S.post(
			url,
			json=my_obj,
			# headers=self.header,
			verify=True
			)
		try:
			J = json.loads(R.text)
			return J
		except:
			return R
