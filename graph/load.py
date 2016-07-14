from parse import parse

def load_graph(filename):
	return parse(filename)

loaded_graph = load_graph('streets_network.geojson')