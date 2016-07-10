from flask import request, jsonify
from models import Reports
import datetime


def by_hour():
	list_reports = Reports.query.all()
	hour_map = {}
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time - 7 * 60 * 60).time().hour
		if time in hour_map:
			hour_map[time] = hour_map[time] + 1
		else:
			hour_map[time] = 1
	return jsonify(success=0, hour=hour_map, count=len(list_reports))

def by_dow():
	list_reports = Reports.query.all()
	dow = {}
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time).date().weekday()
		if time in dow:
			dow[time] = dow[time] + 1
		else:
			dow[time] = 1
	return jsonify(success=0, dow=dow, count=len(list_reports))

def by_month():
	list_reports = Reports.query.all()
	month = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0};
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time).date().month -1
		if time in month:
			month[time] = month[time] + 1
		else:
			month[time] = 1
	return jsonify(success=0, month=month, count=len(list_reports))