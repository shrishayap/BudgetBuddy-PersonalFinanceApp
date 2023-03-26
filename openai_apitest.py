import openai
openai.api_key = "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"
import requests

def parse(user_response):

# Prompt the user for topic
# Use OpenAI API to generate a prompt for DALL-E 2 based on the provided topic
# prompt = f"Only tell me what the item is in the following prompt: {topic}"
#prompt_improv = f"Act as a budgeting advisor. You will be given a question the following prompt: {user_response}"

    item_prompt = f"In the following sentence, what is the item the user is refering to. Only answer with the item, nothing else. Do not answer the question. Your answer should be a single word / item and that is all, no punctuation or special characters: {user_response}"
    price_prompt = f"In the following sentence, what is the price of the item. Only answer with the price, nothing else (no ?, punctuation, special characters, or white spaces). Your answer should be a single number and that is all: {user_response}"

    item_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=item_prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.3,
    )
    item_gen = item_response.choices[0].text.strip()
    category_prompt = f"Which category does {item_gen} fit into. It must be either Education, Food & Drink, Health & Fitness, Recreation, Fashion, Entertainment, Home & Vehicle, Groceries, Travel, or Miscellaneous. Do not print anything else but one of the categories"

    price_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=price_prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    category_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=category_prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    price_gen = price_response.choices[0].text.strip()
    category_gen = category_response.choices[0].text.strip()

    print(item_gen)
    print(price_gen)
    print(category_gen)

    return (item_gen, price_gen, category_gen)

def gpt_improve_response(category):
    improve_prompt = f"Act as a budgeting advisor for me, I'm spending too much money on {category}, tell me what I can do I reduce my spending in this category. Give me 3 insights with no introduction or ending conclusion."

    improve_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=improve_prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.3,
    )
    
    response = improve_response.choices[0].text.strip()
    
    return(response)