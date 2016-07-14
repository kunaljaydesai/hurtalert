from flask import request, jsonify, url_for
from models import Intersection, Reports
from graph.graph import Point
from graph.load import loaded_graph

def add_intersection():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    street_1 = request.args.get('street1')
    street_2 = request.args.get('street2')
    intersection = Intersection(latitude, longitude, street_1, street_2)
    return jsonify(success=0, intersection=intersection.insert_into_db())

def add_report():
	time = request.args.get('time')
	reporter = 3
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	type_report = request.args.get('type')
	report = Reports(time, reporter, latitude, longitude, type_report)
	return jsonify(success=0, report=report.insert_into_db())

def filter():
	time_start = request.arg.get('time_start')
	time_end = request.args.get('time_end')
	center_lat = request.args.get('center_lat')
	center_lon = request.args.get('center_lon')
	height = request.args.get('height')
	width = request.args.get('width')
	top_left = [center_lat - height / 2, center_lon - width / 2]
	bottom_right = [center_lat + height / 2, center_lon + height / 2]
	filter_location_query = Reports.query.filter(Reports.latitude >= top_left[0]).filter(Reports.latitude <= bottom_right[0]).filter(Reports.longitude <= top_left[1]).filter(Reports.longitude >= bottom_right[1]).all()
	and_time = filter_location_query.filter(Reports.time >= time_start).filter(Reports.time <= time_end)
	report_list = and_time.all()
	response_reports = []
	for reports in report_list:
		response_reports.append(reports.serialize)
	return jsonify(success=0, reports=response_reports)

def get_reports():
	reports = Reports.query.filter(Reports.time < 1467337800).all()
	return jsonify(success=0, reports=[report.serialize for report in reports])

def route():
	start_lat = request.args.get('start_lat')
	start_lon = request.args.get('start_lon')
	end_lat = request.args.get('end_lat')
	end_lon = request.args.get('end_lon')
	if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
		start_lat = float(start_lat)
		start_lon = float(start_lon)
		end_lat = float(end_lat)
		end_lon = float(end_lon)
		start = Point(start_lat, start_lon)
		end = Point(end_lat, end_lon)
		graph = loaded_graph
		path = []
		try:
			path = graph.shortest_path(start, end)
		except:
			return jsonify(success=1)
		path = [[node.node.get_pt().latitude, node.node.get_pt().longitude] for node in path]
		path[0] = [start_lat, start_lon]
		path[-1] = [end_lat, end_lon]
		return jsonify(success=0, path=path)
	return jsonify(success=1)