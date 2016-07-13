from graph import *
import json
from pprint import pprint

with open('streets_network.geojson') as data_file:
    data = json.load(data_file)
    
feature_list = data['features']

node_map = dict()

for feature in feature_list:
	geometry = feature['geometry']
	if geometry['type'] == "MultiLineString":
		start_coordinates = geometry['coordinates'][0][0]
		start_lat = start_coordinates[0]
		start_lon = start_coordinates[1]
		start_node = Node(start_lat, start_lon)
		if str(start_node) in node_map:
			start_node = node_map[str(start_node)]
		else:
			node_map[str(start_node)] = start_node
		end_coordinates = geometry['coordinates'][0]
		last_coordinate_index = len(end_coordinates) - 1
		end_coordinates = end_coordinates[last_coordinate_index]
		end_lat = end_coordinates[0]
		end_lon = end_coordinates[1]
		end_node = Node(end_lat, end_lon)
		if str(end_node) in node_map:
			end_node = node_map[str(end_node)]
		else:
			node_map[str(end_node)] = end_node
		start_node.connect(end_node)

print(len(feature_list))
print(len(node_map))

