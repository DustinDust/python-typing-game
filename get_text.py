import requests;

def get_text():
    res = requests.get('https://random-data-api.com/api/lorem_ipsum/random_lorem_ipsum')
    return res.json()['very_long_sentence']

get_text()
