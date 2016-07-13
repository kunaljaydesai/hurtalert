import json
from pprint import pprint

with open('streets_network.geojson') as data_file:
    data = json.load(data_file)
    
feature_list = data['features']

class GraphData:
	def __init__