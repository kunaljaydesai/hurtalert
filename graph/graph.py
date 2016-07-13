import heapq


class Graph:

	def __init__(self):
		self.list_nodes = []

	def add_node(self, node):
		self.list_nodes.append(node)

	def shortest_path(self, start_pt, end_pt):
		min_distance = 9999999
		start_node = None
		for node in self.list_nodes:
			distance = node.get_distance_pt(start_pt)
			if distance < min_distance:
				min_distance = distance
				start_node = node
		min_distance_end = 9999999
		end_node = None
		for node in self.list_nodes:
			distance = node.get_distance_pt(end_pt)
			if distance < min_distance_end:
				min_distance_end = distance
				end_node = node
		print("start " + str(start_node.get_pt()))
		print("end " + str(end_node.get_pt()))
		def get_shortest(start_node, end_node):
			if start_node is not None and end_node is not None:
				rt_node = RouteNode(
					start_node, start_node.get_distance_node(end_node), None)
				heap = [rt_node]
				visited = set()
				visited.add(start_node)
				while len(heap) != 0:
					rt_start_node = heapq.heappop(heap)
					connected = rt_start_node.get_connections()
					for node in connected:
						if node not in visited:
							visited.add(node)
							rt_node = RouteNode(
								node, node.get_distance_node(end_node), rt_start_node)
							if rt_node == RouteNode(end_node, 0, None):
								path = []
								while rt_node.get_parent():
									path.append(rt_node)
									rt_node = rt_node.get_parent()
								path.append(rt_node)
								return path[::-1]
							heapq.heappush(heap, rt_node)
			raise ValueError("No path found.")
		return get_shortest(start_node, end_node)


class RouteNode:

	def __init__(self, node, distance, parent):
		self.node = node
		self.cost = 0
		if parent is not None:
			self.cost = parent.cost + \
				Cost(distance=node.get_distance_node(parent.node)).value()
		self.weight = self.cost + distance
		self.parent = parent

	def get_parent(self):
		return self.parent

	def get_connections(self):
		return self.node.get_connections()

	def __cmp__(self, other):
		return cmp(self.weight, other.weight)

	def __eq__(self, other):
		return self.node == other.node

	def __hash__(self):
		return hash(self.node)


class Node:

	def __init__(self, latitude, longitude):
		self.connected_nodes = []
		self.point = Point(latitude, longitude)

	def connect(self, node):
		self.connected_nodes.append(node)
		node.connected_nodes.append(self)

	def get_lat(self):
		return self.point.get_lat()

	def get_lon(self):
		return self.point.get_lon()

	def get_pt(self):
		return self.point

	def get_distance_node(self, node):
		return self.point.get_distance(node.get_pt())

	def get_distance_pt(self, pt):
		return self.point.get_distance(pt)

	def get_connections(self):
		return self.connected_nodes

	def __str__(self):
		return str(self.point)

class Point:

	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

	def __str__(self):
		return "(" + str(self.latitude) + ", " + str(self.longitude) + ")"

	def get_lat(self):
		return self.latitude

	def get_lon(self):
		return self.longitude

	def get_distance(self, pt):
		return ((self.latitude - pt.get_lat()) ** 2 + (self.longitude - pt.get_lon()) ** 2) ** 0.5


class Cost:

	def __init__(self, distance=0):
		self.output = distance

	def value(self):
		return self.output
