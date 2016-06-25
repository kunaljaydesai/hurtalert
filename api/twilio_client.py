from requests.auth import HTTPBasicAuth
from twilio.rest import TwilioRestClient

class TwilioClient:

	sid = "ACd6db9e164c72b363209207566973a521"
	secret = "1865e9ace22ad54aa480cf5774ccfc7d"

	@staticmethod
	def send_message_to(to="4087180622"):
		client = TwilioRestClient(TwilioClient.sid, TwilioClient.secret)
		message = client.messages.create(body="text messages are working - kunal", to="9253894466", from_="16507536256")
		return message

	@staticmethod
	def test():
		client = TwilioRestClient(TwilioClient.sid, TwilioClient.secret)
		message = client.messages.create(body="text messages are working - kunal", to="9253894466", from_="16507536256")
		message = client.messages.create(body="text messages are working - kunal", to="9253360419", from_="16507536256")
		message = client.messages.create(body="text messages are working - kunal", to="9259896404", from_="16507536256")
		return message