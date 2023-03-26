import requests
import json
import keys


def get_public_token(client_id, secret):
    url = "https://sandbox.plaid.com/sandbox/public_token/create"
    headers = {
    'Content-Type': 'application/json'
    }
    payload = json.dumps({
    "client_id": client_id,
    "secret": secret,
    "institution_id": "ins_20",
    "initial_products": [
        "auth"
    ],
    "options": {
        "webhook": "https://www.genericwebhookurl.com/webhook"
    }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    public_token = response.json()['public_token']
    return public_token

def get_access_token(client_id, secret, public_token):
    url = "https://sandbox.plaid.com/item/public_token/exchange"

    payload = json.dumps({
    "client_id": client_id,
    "secret": secret,
    "public_token": public_token
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = response.json()['access_token']
    return access_token

def get_transactions(client_id, secret, access_token, start_date, end_date):
    url = "https://sandbox.plaid.com/transactions/get"
    payload = json.dumps({
    "client_id": client_id,
    "secret": secret,
    "access_token": access_token,
    "start_date": start_date,
    "end_date": end_date
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    transaction_history = response.json()

    cc_account_ids = []
    for acc in transaction_history["accounts"]:
        if acc["subtype"] == "credit card":
            cc_account_ids.append(acc["account_id"])

    transactions = []
    for transaction in transaction_history["transactions"]:
        if transaction["account_id"] in cc_account_ids:
            transactions.append(transaction)

    return transactions

def map_transactions(transactions):
    hashmap = { "Recreation": 0,
                "Education": 0,
                "Food And Drink": 0,
                "Health And Fitness": 0,
                "Fashion And Beauty": 0,
                "Entertainment": 0,
                "Home And Vehicle": 0,
                "Grocery": 0,
                "Miscellaneous": 0,
                "Travel": 0}
    recreation = set(["Recreation"])
    education = set(["Education"])
    food_and_drink = set(["Food and Drink"])
    health_and_fitness = set(["Healthcare", "Pharmacies", "Glasses and Optometrist", "Sporting Goods"])
    fashion_beauty = set(["Personal Care", "Beauty Products", "Jewelry and Watches", "Department Stores",
                        "Clothing and Accessories", "Outlet", "Shopping Centers and Malls"])
    entertainment = set(["Entertainment", "Music, Video and DVD", "Bookstores", "Toys", "Musical Instruments"])
    home_and_vehicle = set(["Arts and Crafts", "Automotive", "Bicycles", "Office Supplies", "Lawn and Garden",
                            "Furniture and Home Decor", "Hardware Store", "Photos and Frames", "Home Improvement",
                            "Automotive"])
    grocery = set(["Supermarkets and Groceries"])
    travel = set(["Travel"])


    for transaction in transactions:

        catogories = transaction["category"]

        if "Payment" in catogories:
            continue

        hit = False

        for cat in catogories:
            if cat in recreation:
                hashmap["Recreation"] += transaction["amount"]
                hit = True
                break
            elif cat in education:
                hashmap["Education"] += transaction["amount"]
                hit = True
                break
            elif cat in food_and_drink:
                hashmap["Food And Drink"] += transaction["amount"]
                hit = True
                break
            elif cat in health_and_fitness:
                hashmap["Health And Fitness"] += transaction["amount"]
                hit = True
                break
            elif cat in fashion_beauty:
                hashmap["Fashion And Beauty"] += transaction["amount"]
                hit = True
                break
            elif cat in entertainment:
                hashmap["Entertainment"] += transaction["amount"]
                hit = True
                break
            elif cat in home_and_vehicle:
                hashmap["Home And Vehicle"] += transaction["amount"]
                hit = True
                break
            elif cat in grocery:
                hashmap["Grocery"] += transaction["amount"]
                hit = True
                break
            elif cat in travel:
                hashmap["Travel"] += transaction["amount"]
                hit = True
                break
        
        if not hit:
            hashmap["Miscellaneous"] += transaction["amount"]


    return hashmap

def get_transactional_map(client_id, secret, access_token, start_date, end_date):
    transactions = get_transactions(client_id, secret, access_token, start_date, end_date)
    return map_transactions(transactions)

if __name__ == "__main__":
    client_id = keys.client_id
    secret = keys.secret
    access_token = keys.access_token
    print(get_transactional_map(client_id, secret, access_token, "2021-01-01", "2022-01-01"))










