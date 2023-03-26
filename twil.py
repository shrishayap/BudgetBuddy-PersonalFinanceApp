from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import keys
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

# set up your Twilio account credentials
account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

# send a message from your Twilio phone number to your recipient
from_number = keys.twilio_number
to_number = keys.target_number
message = client.messages.create(
    body='Hello, this is a test message from Twilio!',
    from_=from_number,
    to=to_number
)

app = Flask(__name__)
run_with_ngrok(app)

# create a route to handle incoming messages
@app.route('/sms', methods=['POST'])
def receive_sms():
    # retrieve the message body and phone number from the incoming request
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if body == "current":
        resp.message("You're broke")

    return str(resp)

if __name__ == '__main__':
    app.run()
