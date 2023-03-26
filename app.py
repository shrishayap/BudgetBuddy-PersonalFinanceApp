from flask import Flask, render_template, jsonify, request
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import keys
import openai_apitest

account_sid = keys.account_sid
auth_token = keys.auth_token

# cred = credentials.Certificate("./budgetbuddy-44202-firebase-adminsdk-q9wk5-1a76e3f3d2.json")
# firebase_admin.initialize_app(cred)

client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Hey! I\'m your BudgetBuddy. How can I help you?\nType 1 to view your budget\'s current status\nType 2 to see if you can afford an item\nType 3 for budget improvements\n',
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

    gpt_response_tuple = openai_apitest.parse(body) #(item, price, category)

    item = gpt_response_tuple[0]
    price = gpt_response_tuple[1]
    category = gpt_response_tuple[2]

    if body == '1':
        #Ask GPT to see if user can afford the item
        #Send the okay/NI/bad
        pass
    elif body == '2':
        #get outstanding buckets, and ask Chat how to improve them
        pass
    elif body == '3':
        #Ask GPT to improve my habits
        improvement_response = openai_apitest.gpt_improve_response(category)
        resp.message(improvement_response)
    else:
        resp.message("Invalid Input. Please reply with 1, 2, or 3")

    return str(resp)

if __name__ == "__main__":
    app.run()