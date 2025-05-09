import re
import requests

def use_calculator(query):
    try:
        expr = re.findall(r'[\d\.\+\-\*\/\(\)\s]+', query)[0]
        return f"Result: {eval(expr)}"
    except:
        return "Invalid calculation."

def use_dictionary(query):
    term = query.lower().split("define")[-1].strip()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    res = requests.get(url)
    if res.status_code == 200:
        meaning = res.json()[0]['meanings'][0]['definitions'][0]['definition']
        return f"{term}: {meaning}"
    return "Definition not found."
