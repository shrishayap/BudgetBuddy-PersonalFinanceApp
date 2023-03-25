from flask import Flask, render_template, jsonify, request
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import keys

account_sid = keys.account_sid
auth_token = keys.auth_token

# cred = credentials.Certificate("./budgetbuddy-44202-firebase-adminsdk-q9wk5-1a76e3f3d2.json")
# firebase_admin.initialize_app(cred)

client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Startup',
    from_=keys.twilio_number,
    to=keys.target_number
)

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/')
# def index():
#     if 'user' in session:
#         try:
#             decoded_token = auth.verify_id_token(session['user'])
#             uid = decoded_token['uid']
#             #different page contents based on user
#             return render_template('index.html')
#         except:
#             return redirect('/login')
#     else:
#         return redirect('/login')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         print((email, password))
#         try:
#             #user = auth.get_user_by_email(email)
#             user = auth.sign_in_with_email_and_password(email, password)
#             print("TEST HERE")
#             session['user'] = user['idToken']
#             return redirect('/')
#         except:
#             print("TEST HERE 123")
#             return render_template('login.html', error='Invalid email or password')
#     else:
#         print("TEST HERE 12345")
#         return render_template('login.html')

#get responses with ngrok
@app.route('/sms', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if body.lower() == 'How are my financials?':
        #get current status of user's buckets
        pass
    if body.lower() == 'How can I improve?':
        #get outstanding buckets, and ask Chat how to improve them
        pass
    if body.lower() == 'Can I afford this item?':
        pass
        #parse for store -> get category. Report back that specific category

    return str(resp)

if __name__ == "__main__":
    app.run()