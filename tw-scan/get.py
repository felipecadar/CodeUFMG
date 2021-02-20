import urllib, requests
import time, os
import pathlib
import datetime

here = str(pathlib.Path(__file__).parent.absolute())
print("Getting stats")
print(datetime.datetime.now())

def getAll():
    village_url = "https://br101.tribalwars.com.br/map/village.txt"
    village_data = urllib.parse.unquote_plus(requests.get(village_url).text)
    
    player_url = "https://br101.tribalwars.com.br/map/player.txt"
    player_data = urllib.parse.unquote_plus(requests.get(player_url).text)

    odd_url = "https://br101.tribalwars.com.br/map/kill_def.txt"
    odd_data = urllib.parse.unquote_plus(requests.get(odd_url).text)

    oda_url = "https://br101.tribalwars.com.br/map/kill_att.txt"
    oda_data = urllib.parse.unquote_plus(requests.get(oda_url).text)

    t = str(time.time())
    with open(here + "/tw/villages/" + t + ".txt", "w") as f:
        f.write(village_data)

    with open(here + "/tw/players/" + t + ".txt", "w") as f:
        f.write(player_data)

    with open(here + "/tw/odd/" + t + ".txt", "w") as f:
        f.write(odd_data)

    with open(here + "/tw/oda/" + t + ".txt", "w") as f:
        f.write(oda_data)

if __name__ == "__main__":

    if not os.path.exists(here + "/tw/villages/"):
        os.makedirs(here + "/tw/villages/")

    if not os.path.exists(here + "/tw/players/"):
        os.makedirs(here + "/tw/players/")

    if not os.path.exists(here + "/tw/odd/"):
        os.makedirs(here + "/tw/odd/")

    if not os.path.exists(here + "/tw/oda/"):
        os.makedirs(here + "/tw/oda/")
    
    getAll()