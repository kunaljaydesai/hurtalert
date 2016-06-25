from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Contacts, Reports, db

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:crimeapp@crime.cnfegalrlacy.us-west-2.rds.amazonaws.com/crime'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(application)

@application.before_first_request
def create_tables():
	db.create_all()

@application.route("/")
def index():
	return 'test'

@application.route("/newuser")
def new_user():
	name = request.args.get('name')
	phone = request.args.get('phone')
	user = User(name, phone)
	return jsonify(user=user.insert_into_db())

@application.route("/addcontact")
def add_contact():
	user_reference = request.args.get('user_ref')
	phone = request.args.get('phone')
	contact = Contacts(user_reference, phone)
	return jsonify(contact=contact.insert_into_db())

@application.route("/addreport")
def add_report():
	time = request.args.get('time')
	reporter = request.args.get('reporter')
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
	list_contacts = Contacts.query.filter_by(user_reference=user).all()
	phone_numbers = [contact['phone'] for contact in list_contacts]
	for number in phone_numers:
		TwilioClient.send_message_to(number)
	report = Reports(time, user, latitude, longitude, type_report)
	return jsonify(report=report.insert_into_db())

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

@application.route('/sameer')
def sameer():
	point1 = {
		'latitude' : 33.1,
		'longitude' : -122.4
	}
	list_points = [point1, point1, point1]
	return jsonify(points=list_points)

if __name__ == "__main__":
	application.run(host="0.0.0.0", port=80, debug=True, threaded=True)