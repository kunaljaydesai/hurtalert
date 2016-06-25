from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	phone = db.Column(db.BigInteger)

	def __init__(self, name=None, phone=None):
		self.name = name
		self.phone = phone

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name' : self.name,
			'phone' : self.phone,
		}

	def insert_into_db(self):
		user = User.query.filter_by(phone=self.phone).first()
		
		if user is None:
			db.session.add(self)
			db.session.commit()
			return self.serialize
		return user.serialize


class Contacts(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	user_reference = db.Column(db.Integer)
	phone = db.Column(db.BigInteger)

	def __init__(self, user_reference, phone):
		self.user_reference = user_reference
		self.phone = phone

	@property 
	def serialize(self):
		return {
			'id' : self.id,
			'user_reference' : self.user_reference,
			'phone' : self.phone
		}

	def insert_into_db(self):
		contact = Contacts.query.filter_by(user_reference=self.user_reference, phone=self.phone).first()
		if contact is None:
			db.session.add(self)
			db.session.commit()
			return self.serialize
		return contact.serialize

class Reports(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.BigInteger)
	reporter = db.Column(db.Integer)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	type_crime = db.Column(db.String(80))

	def __init__(self, time, reporter, latitude, longitude, type_crime):
		self.time = time
		self.reporter = reporter
		self.latitude = latitude
		self.longitude = longitude
		self.type_crime = type_crime

	@property 
	def serialize(self):
		return {
			'id' : self.id,
			'time' : self.time,
			'reporter' : self.reporter,
			'latitude' : self.latitude,
			'longitude' : self.longitude,
			'type_crime' : self.type_crime
		}

	def insert_into_db(self):
		db.session.add(self)
		db.session.commit()
		return self.serialize


