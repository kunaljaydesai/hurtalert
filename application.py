from flask import Flask, request, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User, Contacts, Reports, Intersection, db
from views.api.twilio_client import TwilioClient
from views.api import path, user, data
from views.view import render
import requests

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:crimeapp@crime.cnfegalrlacy.us-west-2.rds.amazonaws.com/crime'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(application)


unharmful = ["BURGLARY COMMERCIAL", "BURGLARY RESIDENTIAL", "BURGLARY AUTO", "MUNICIPAL CODE", "DISTURBANCE", "DOMESTIC VIOLENCE", "FRAUD/FORGERY", "IDENTIFY THEFT", "ALCOHOL OFFENSE", "VEHICLE STOLEN", "2ND RESPONSE", "DISTURBANCE - NOISE", "VEHICLE RECOVERED", "VANDALISM", "ARSON"]
harmful = [""]


@application.before_first_request
def create_tables():
	db.create_all()

#front end
application.add_url_rule('/', view_func=render.index)
application.add_url_rule('/home', view_func=render.home)
application.add_url_rule('/heat_map', view_func=render.heat_map)
application.add_url_rule('/add_contact', view_func=render.addcontact)
application.add_url_rule('/safest_route', view_func=render.safest_route)

###API

#path
application.add_url_rule('/api/path/add_intersection', view_func=path.add_intersection)
application.add_url_rule('/api/path/add_report', view_func=path.add_report)
application.add_url_rule('/api/path/filter', view_func=path.filter)
application.add_url_rule('/api/path/get_reports', view_func=path.get_reports)
application.add_url_rule('/api/path/route', view_func=path.route)

#user
application.add_url_rule('/api/user/add_user', view_func=user.add_user)
application.add_url_rule('/api/user/add_contact', view_func=user.add_contact)
application.add_url_rule('/api/user/get_contacts', view_func=user.get_contacts)
application.add_url_rule('/api/user/emergency', view_func=user.emergency)

#data
application.add_url_rule('/api/data/crime_by_hour', view_func=data.by_hour)
application.add_url_rule('/api/data/crime_by_dow', view_func=data.by_dow)
application.add_url_rule('/api/data/crime_by_month', view_func=data.by_month)

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
	return jsonify(success=0, bounding_boxes=bounding_boxes)

@application.route('/get_sr')
def sr():
	start = request.args.get('start')
	end = request.args.get('end')
	return redirect("/get_map?start=" + start.replace(' ', '+') + "&end=" + end.replace(' ', '+'))

@application.route('/get_map')
def get_map():
	start_location = request.args.get('start')
	end_location = request.args.get('end')
	full_address = start_location.rstrip() + ' Berkeley, CA'
	print("start address: " + full_address)
	json_data = requests.get("https://geocoder.cit.api.here.com/6.2/geocode.json?searchtext=" + full_address + "&app_id=LLeNnIbdeXe9EqgoTLFX&app_code=v76nZNtTzZ4sVSLXQE9pQg&gen=8").json()
	start_lon = json_data['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
	start_lat = json_data['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
	full_address = end_location.rstrip() + ' Berkeley, CA'
	print("end address: " + full_address)
	json_data = requests.get("https://geocoder.cit.api.here.com/6.2/geocode.json?searchtext=" + full_address + "&app_id=LLeNnIbdeXe9EqgoTLFX&app_code=v76nZNtTzZ4sVSLXQE9pQg&gen=8").json()
	end_lon = json_data['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
	end_lat = json_data['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
	str_bounding_box = '&avoidareas='
	#json_data = requests.get("http://crimeapp-dev.us-west-1.elasticbeanstalk.com/bounding_boxes").json()
	bounding_boxes = [
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.31383333333333
            },
            'count': 84,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.319
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.3035
            },
            'count': 67,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.30866666666667
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.29833333333333
            },
            'count': 124,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.3035
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.29833333333333
            },
            'count': 350,
                'top_left': {
                    'latitude': 37.875479999999996,
                    'longitude': -122.3035
                }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.29316666666666
            },
            'count': 174,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.29833333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.29316666666666
            },
            'count': 306,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.29833333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.288
            },
            'count': 71,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.29316666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.288
            },
            'count': 282,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.29316666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.288
            },
            'count': 246,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.29316666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.89019,
                'longitude': -122.28283333333333
            },
            'count': 51,
            'top_left': {
                'latitude': 37.9049,
                'longitude': -122.288
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.28283333333333
            },
            'count': 159,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.288
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.28283333333333
            },
            'count': 136,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.288
            }
        },
        {
            'bottom_right': {
                'latitude': 37.89019,
                'longitude': -122.27766666666666
            },
            'count': 74,
            'top_left': {
                'latitude': 37.9049,
                'longitude': -122.28283333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.27766666666666
            },
            'count': 102,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.28283333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.27766666666666
            },
            'count': 197,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.28283333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.27766666666666
            },
            'count': 269,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.28283333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.2725
            },
            'count': 127,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.27766666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.2725
            },
            'count': 421,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.27766666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.2725
            },
            'count': 304,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.27766666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.89019,
                'longitude': -122.26733333333333
            },
            'count': 81,
            'top_left': {
                'latitude': 37.9049,
                'longitude': -122.2725
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.26733333333333
            },
            'count': 231,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.2725
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.26733333333333
            },
            'count': 1161,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.2725
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.26733333333333
            },
            'count': 428,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.2725
            }
        },
        {
            'bottom_right': {
                'latitude': 37.89019,
                'longitude': -122.26216666666666
            },
            'count': 62,
            'top_left': {
                'latitude': 37.9049,
                'longitude': -122.26733333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.26216666666666
            },
            'count': 138,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.26733333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.26216666666666
            },
            'count': 378,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.26733333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.26216666666666
            },
            'count': 171,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.26733333333333
            }
        },
        {
            'bottom_right': {
                'latitude': 37.875479999999996,
                'longitude': -122.25699999999999
            },
            'count': 65,
            'top_left': {
                'latitude': 37.89019,
                'longitude': -122.26216666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.25699999999999
            },
            'count': 539,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.26216666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.25699999999999
            },
            'count': 163,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.26216666666666
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.25183333333332
            },
            'count': 272,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.25699999999999
            }
        },
        {
            'bottom_right': {
                'latitude': 37.846059999999994,
                'longitude': -122.25183333333332
            },
            'count': 184,
            'top_left': {
                'latitude': 37.860769999999995,
                'longitude': -122.25699999999999
            }
        },
        {
            'bottom_right': {
                'latitude': 37.860769999999995,
                'longitude': -122.24666666666666
            },
            'count': 130,
            'top_left': {
                'latitude': 37.875479999999996,
                'longitude': -122.25183333333332
            }
        }
    ]
	for box in bounding_boxes:
	    if box['count'] >= 500:
	        top_left_latitude = box['top_left']['latitude']
	        top_left_longitude = box['top_left']['longitude']
	        bottom_right_latitude = box['bottom_right']['latitude']
	        bottom_right_longitude = box['bottom_right']['longitude']
	        str_bounding_box += str(top_left_latitude) + ',' + str(top_left_longitude) + ';'+ str(bottom_right_latitude) + ',' + str(bottom_right_longitude) + '!'
	str_bounding_box = str_bounding_box[:len(str_bounding_box) - 1]
	json_data2 = requests.get("https://route.api.here.com/routing/7.2/calculateroute.json?app_id=LLeNnIbdeXe9EqgoTLFX&app_code=v76nZNtTzZ4sVSLXQE9pQg&waypoint0=geo!" + str(start_lat) + "," + str(start_lon) + "&waypoint1=geo!" + str(end_lat) + "," + str(end_lon) + "&mode=fastest;pedestrian" + str_bounding_box).json()
	moves = json_data2['response']['route'][0]['leg'][0]['maneuver']
	waypoints_data = []
	for move in moves:
	    waypoints_data.append([move['position']['latitude'], move['position']['longitude']])
	return render_template('map.html', waypoints=waypoints_data, start_lat=start_lat,start_lng=start_lon, end_lat=end_lat, end_lng=end_lon)

if __name__ == "__main__":
	application.run(host="0.0.0.0", port=80, debug=True)