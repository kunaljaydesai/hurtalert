from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Contacts, Reports, db
from api.twilio_client import TwilioClient
import datetime

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:crimeapp@crime.cnfegalrlacy.us-west-2.rds.amazonaws.com/crime'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(application)


unharmful = ["BURGLARY COMMERCIAL", "BURGLARY RESIDENTIAL", "BURGLARY AUTO", "MUNICIPAL CODE", "DISTURBANCE", "DOMESTIC VIOLENCE", "FRAUD/FORGERY", "IDENTIFY THEFT", "ALCOHOL OFFENSE", "VEHICLE STOLEN", "2ND RESPONSE", "DISTURBANCE - NOISE", "VEHICLE RECOVERED", "VANDALISM", "ARSON"]
harmful = [""]

@application.before_first_request
def create_tables():
	db.create_all()

@application.route("/")
def index():
	return render_template('home.html')

@application.route("/newuser")
def new_user():
	name = request.args.get('name')
	phone = request.args.get('phone')
	user = User(name, phone)
	return jsonify(user=user.insert_into_db())

@application.route("/addcontact")
def addcontact():
	user_reference = request.args.get('user_ref')
	phone = request.args.get('phone')
	contact = Contacts(user_reference, phone)
	return jsonify(contact=contact.insert_into_db())

@application.route("/add_contact")
def add_contact():
	return render_template('add_contact.html')

@application.route('/get_contacts')
def get_contacts():
	list_contacts = Contacts.query.all()
	return jsonify([contact.serialize for contact in list_contacts])

@application.route("/addreport")
def add_report():
	time = request.args.get('time')
	reporter = 3
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	type_report = request.args.get('type')
	report = Reports(time, reporter, latitude, longitude, type_report)
	return jsonify(report=report.insert_into_db())

@application.route('/emergency')
def emergency():
	user = request.args.get('id')
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	type_report = request.args.get('type')
	time = request.args.get('time')
	list_contacts = Contacts.query.filter_by(user_reference=3).all()
	phone_numbers = [contact.phone for contact in list_contacts]
	urgent_user = User.query.filter_by(id=3).first()
	for number in phone_numbers:
		print(number)
		if latitude is not None and longitude is not None and int(latitude) != -1 and int(longitude) != -1:
			print(TwilioClient.send_message_to(urgent_user, latitude=latitude, longitude=longitude, to=str(number)))
		else:
			print(TwilioClient.send_message_to(urgent_user, to=str(number)))
	#report = Reports(time, 3, latitude, longitude, type_report)
	return jsonify(report=0)

@application.route('/filter')
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
	return jsonify(reports=response_reports)

@application.route('/safest_route')
def safest_route():
	return render_template('safest_route.html')

@application.route('/crime_rates_by_hour')
def by_hour():
	list_reports = Reports.query.all()
	hour_map = {}
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time - 7 * 60 * 60).time().hour
		if time in hour_map:
			hour_map[time] = hour_map[time] + 1
		else:
			hour_map[time] = 1
	return jsonify(hour=hour_map, count=len(list_reports))

@application.route('/crime_rates_by_dow')
def by_dow():
	list_reports = Reports.query.all()
	dow = {}
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time).date().weekday()
		if time in dow:
			dow[time] = dow[time] + 1
		else:
			dow[time] = 1
	return jsonify(dow=dow, count=len(list_reports))

@application.route('/crime_rates_by_month')
def by_month():
	list_reports = Reports.query.all()
	month = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0};
	for report in list_reports:
		time = datetime.datetime.fromtimestamp(report.time).date().month -1
		if time in month:
			month[time] = month[time] + 1
		else:
			month[time] = 1
	return jsonify(month=month, count=len(list_reports))


@application.route('/sameer')
def sameer():
	point1 = {
		'latitude' : 33.1,
		'longitude' : -122.4
	}
	list_points = [point1, point1, point1]
	return jsonify(points=list_points)

@application.route('/get_reports')
def get_reports():
	reports = Reports.query.filter(Reports.time < 1467337800).all()
	return jsonify(reports=[report.serialize for report in reports])

@application.route('/bounding_boxes')
def bounding_box():
	lat_step = (37.9049 - 37.4636) / 30
	lon_step = (122.319 - 122.164) / 30 
	current_box = {
		'top_left' : {
			'latitude' : 37.9049,
			'longitude' : -122.319,
		},
		'bottom_right' : {
			'latitude' : 37.9049 - lat_step,
			'longitude' : -122.319 + lon_step,
		},
	}
	bounding_boxes = []
	current_box['count'] = Reports.query.filter(Reports.latitude <=current_box['top_left']['latitude']).filter(Reports.latitude >= current_box['bottom_right']['latitude']).filter(Reports.longitude >= current_box['top_left']['longitude']).filter(Reports.longitude <= current_box['bottom_right']['longitude']).count()
	if current_box['count'] > 50:
		bounding_boxes.append(current_box)
	current_longitude = current_box['top_left']['longitude']
	current_latitude = current_box['top_left']['latitude']
	while current_longitude <= -122.164:
		while current_latitude >= 37.4636:
			top_left_long = current_box['top_left']['longitude']
			top_left_lat = current_box['top_left']['latitude']
			bottom_right_long = current_box['bottom_right']['longitude']
			bottom_right_lat = current_box['bottom_right']['latitude']
			current_box = {
				'top_left' : {
					'latitude' : top_left_lat - lat_step,
					'longitude' : top_left_long,
				},
				'bottom_right' : {
					'latitude' : bottom_right_lat - lat_step,
					'longitude' : bottom_right_long,
				},
			}
			current_box['count'] = Reports.query.filter(Reports.latitude <=current_box['top_left']['latitude']).filter(Reports.latitude >= current_box['bottom_right']['latitude']).filter(Reports.longitude >= current_box['top_left']['longitude']).filter(Reports.longitude <= current_box['bottom_right']['longitude']).count()
			if current_box['count'] > 50:
				bounding_boxes.append(current_box)
			current_latitude = current_box['top_left']['latitude']
		current_longitude = current_longitude + lon_step
		current_latitude = 37.9049
		current_box = {
			'top_left' : {
				'latitude' : current_latitude,
				'longitude' : current_longitude,
			},
			'bottom_right' : {
				'latitude' : current_latitude - lat_step,
				'longitude' : current_longitude + lon_step,
			}
		}
		current_box['count'] = Reports.query.filter(Reports.latitude <=current_box['top_left']['latitude']).filter(Reports.latitude >= current_box['bottom_right']['latitude']).filter(Reports.longitude >= current_box['top_left']['longitude']).filter(Reports.longitude <= current_box['bottom_right']['longitude']).count()
		if current_box['count'] > 50:
			bounding_boxes.append(current_box)
	return jsonify(bounding_boxes=bounding_boxes)


if __name__ == "__main__":
	application.run(host="0.0.0.0", port=81, debug=True)