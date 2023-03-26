from flask import Flask, render_template, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from charts import *
import get_financial_data as gfd
import keys
import gpt
import decision
import json
import plotly
import os
import time


account_sid = keys.account_sid
auth_token = keys.auth_token

client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Hey! I\'m your BudgetBuddy. How can I help you?\nType 1 to view your budget\'s current status\nType 2 for budget improvements\n or ask if you can afford an item (mention item name and price)',
    from_=keys.twilio_number,
    to=keys.target_number
)

app = Flask(__name__, static_url_path='/static')
run_with_ngrok(app)

budget_map = {}
spend_map = gfd.get_transactional_map()
improve_str = ""

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/allocate')
def allocate():
    return render_template('budget-allocation.html')

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    try:
        os.remove("templates/barchart.html")
    except:
        pass
    try:
        os.remove("templates/piechart.html")
    except:
        pass
    data = request.get_data().decode("utf-8")
    data = json.loads(data)
    for bucket in data:
        budget_map[bucket] = float(data[bucket])
    bar = barchart(budget_map, spend_map)
    pie = piechart(budget_map, spend_map)
    with open("templates/barchart.html", "w") as file:
        file.write(bar)
        file.close()
    with open("templates/piechart.html", "w") as file:
        file.write(pie)
        file.close()
    improve_str = decision.how_improve(budget_map)
    return render_template("index.html")

@app.route('/barchart.html', methods=['GET', 'POST'])
def barchart_endpoint():
    return render_template("barchart.html")

@app.route('/piechart.html', methods=['GET', 'POST'])
def piechart_endpoint():
    return render_template("piechart.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    improve_str = decision.how_improve(budget_map)
    return render_template("index.html")

@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")

#get responses with ngrok
@app.route('/sms', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if body == '1':
        #Get current financial status
        resp.message(decision.financial_status(budget_map))
    elif body == '2':
        #Ask GPT to improve my habits
        print("Got 2")
        improvement_response = decision.how_improve(budget_map)
        resp.message(improvement_response)
    else:
        item, price, category = gpt.parse(body)   #(item, price, category)
        try:
            resp.message(decision.affordable(category, price, budget_map))
        except Exception as e:
            print(e)
            resp.message("Please enter a valid message")

    return str(resp)

if __name__ == "__main__":
    app.run()
