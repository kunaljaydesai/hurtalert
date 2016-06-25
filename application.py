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


if __name__ == "__main__":
	application.run(host="0.0.0.0", port=80, debug=True, threaded=True)