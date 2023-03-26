import get_financial_data as gfd
import openai
import requests
import keys
import gpt

client_id = keys.client_id
secret = keys.secret
access_token = keys.access_token
start_date = "2021-01-01"
end_date = "2022-01-01"

budget_map = { "Recreation": 100,
            "Education": 10,
            "Food And Drink": 200,
            "Health And Fitness": 20,
            "Fashion And Beauty": 10,
            "Entertainment": 0,
            "Home And Vehicle": 100,
            "Grocery": 300,
            "Miscellaneous": 0,
            "Travel": 400}

def affordable(category, price):
    price = float(price)
    transactional_map = gfd.get_transactional_map(client_id, secret, access_token, start_date, end_date)

    budget = budget_map[category]
    current_spending = transactional_map[category]

    afford = (budget - current_spending) >= price
    over_under = "UNDER" if afford else "OVER"
    decision = "CAN" if afford else "CANNOT"

    return f"You have spent ${current_spending} / ${budget} on {category}. Making this purchase puts your monthly spending at {round(current_spending + price, 2)}, (putting you {over_under}). You {decision} afford this purchase."

def how_improve():
    print("Started improve")
    transactional_map = gfd.get_transactional_map(client_id, secret, access_token, start_date, end_date)
    print("Got transactional map")
    over = {}

    for category in transactional_map:
        if (transactional_map[category] > budget_map[category]):
            over[category] = gpt.gpt_improve_response(category)

    print("Got over categories")
    print(f"Category count: {len(transactional_map.keys())}")
    print(f"Over count: {len(over.keys())}")

    ret_str = ""

    for key in over:
        print("HERE")
        ret_str += f"{key}\n{over[key]}\n\n"

    print("created ret str")

    return ret_str

def financial_status():

    transactional_map = gfd.get_transactional_map(client_id, secret, access_token, start_date, end_date)
    
    cat_over_counter = 0

    for category in transactional_map:
        if (transactional_map[category] > budget_map[category]):
            cat_over_counter += 1
        

    status = ""
    if cat_over_counter == 0:
        status = "GOOD"
    elif 0 < cat_over_counter < 5:
        status = "OKAY"
    else:
        status = "BAD"


    ret_str = f"{status} ({cat_over_counter}/10 categories over budget)"
    return ret_str

if __name__ == "__main__":
    how_improve()