from flask import request, jsonify
from models import User, Contacts
from views.api.twilio_client import TwilioClient

def add_user():
	name = request.args.get('name')
	phone = request.args.get('phone')
	user = User(name, phone)
	return jsonify(success=0, user=user.insert_into_db())

def add_contact():
	user_reference = request.args.get('user_ref')
	phone = request.args.get('phone')
	contact = Contacts(user_reference, phone)
	return jsonify(success=0, contact=contact.insert_into_db())

def get_contacts():
	list_contacts = Contacts.query.all()
	return jsonify(success=0, contacts=[contact.serialize for contact in list_contacts])

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
		if latitude is not None and longitude is not None and float(latitude) != -1 and float(longitude) != -1:
			print(TwilioClient.send_message_to(urgent_user, latitude=latitude, longitude=longitude, to=str(number)))
		else:
			print(TwilioClient.send_message_to(urgent_user, to=str(number)))
	return jsonify(success=0, report=0)