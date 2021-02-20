import requests

BASE_URL = "https://api.cartolafc.globo.com"

def atletas():
    json = requests.get("%s/atletas/mercado" % BASE_URL).json()
    return json["atletas"]

def clubes():
    json = requests.get("%s/atletas/mercado" % BASE_URL).json()
    res = {int(k):i for (k,i) in json["clubes"].items()}    
    return res

def posicoes():
    json = requests.get("%s/atletas/mercado" % BASE_URL).json()
    res = {int(k):i["nome"] for (k,i) in json["posicoes"].items()}    
    return res

def status():
    json = requests.get("%s/atletas/mercado" % BASE_URL).json()
    res = {int(k):i["nome"] for (k,i) in json["status"].items()}    
    return res

def save(filename):
    res = requests.get("%s/atletas/mercado" % BASE_URL)
    with open(filename, "w") as f:
        f.write(res.text)
