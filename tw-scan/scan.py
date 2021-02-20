import requests
import argparse
import math
import urllib

def getPlayersDatabase(username):
    player_url = "https://br101.tribalwars.com.br/map/player.txt"
    data = requests.get(player_url).text
    lines = data.split("\n")
    me = None
    players = {}
    for line in lines:
        split = line.split(",")
        if len(split) == 6: 
            idx, name, tribe_id, villages ,pts,rank = split
            players[idx] = [name, tribe_id, int(villages), int(pts), int(rank)]

            if name == username:
                me = idx

    return players, me

def getVillagesDatabase(my_ixd):
    village_url = "https://br101.tribalwars.com.br/map/village.txt"
    data = requests.get(village_url).text

    lines = data.split("\n")

    my_villages = []
    database = []
    for line in lines:
        split = line.split(",")
        if len(split) == 7: 
            village_id, name, x, y, idx, pts, b = split
            name = urllib.parse.unquote_plus(name)
            x = int(x)
            y = int(y)
            pts = int(pts)

            database.append([idx, name, (x, y), pts, village_id, b])

            if my_ixd == idx:
                my_villages.append([idx, name, (x, y), pts, village_id, b])

    return database, my_villages

def getVillagesDatabase(my_ixd):
    village_url = "https://br101.tribalwars.com.br/map/village.txt"
    data = requests.get(village_url).text

    lines = data.split("\n")

    my_villages = []
    database = []
    for line in lines:
        split = line.split(",")
        if len(split) == 7: 
            village_id, name, x, y, idx, pts, b = split
            name = urllib.parse.unquote_plus(name)
            x = int(x)
            y = int(y)
            pts = int(pts)

            database.append([idx, name, (x, y), pts, village_id, b])

            if my_ixd == idx:
                my_villages.append([idx, name, (x, y), pts, village_id, b])

    return database, my_villages

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--me",     type=str, default="subaro98", help="You username")
    parser.add_argument("-r", "--radius", type=int, default=8,         help="Atack radius")
    parser.add_argument("-p", "--points", type=int, default=450,         help="Max points")

    return parser.parse_args()

if __name__ == "__main__":
    args = Parser()

    players, my_idx = getPlayersDatabase(args.me)
    database, my_villages = getVillagesDatabase(my_idx)
    print(my_idx)

    for me in my_villages:
        origin = me[2]
        attack = []
        for village in database:
            idx, name, target, pts, village_id, _ = village
            if idx == "0" or players[idx][1] == players[my_idx][1]: #not in my tribe
                continue
            dist = distance(origin, target)
            if village[0] != me and dist < args.radius and pts <= args.points:
                village.append(dist)
                attack.append(village)

        print("From {}\n".format(me[1]))
        print("dist - [ x , y ] - pts - Name")
        attack = sorted(attack, key= lambda x: x[3])
        for village in attack:
            _, name, target, pts, village_id, _, dist = village
            print("https://br101.tribalwars.com.br/game.php?village={}&screen=info_village&id={}#{};{}"
            .format(me[4], village_id, target[0], target[1]))
            print("{:.1f} - {}|{} - {} - {}".format(dist, target[0], target[1], pts, name))
