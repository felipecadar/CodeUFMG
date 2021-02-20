import argparse
import math
import glob, os
import datetime
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as md


def makeOD(fname):
    database = {}
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            lines = f.readlines()
            for line in lines:
                split = line.replace("\n","").split(",")
                if len(split) == 3:
                    ranking, idx, od = split
                    database[idx] = od

    return database
        
def Make_DB(username):
    files = sorted(glob.glob("tw/players/*"))[::-1]
    Player_DB = {}
    for fname in files:
        with open(fname, "r") as f:
            timestamp = float(fname.split("/")[-1].replace(".txt", ""))

            odd = makeOD(fname.replace("players", "odd"))
            oda = makeOD(fname.replace("players", "oda"))

            lines = f.readlines()
            me = None
            for line in lines:
                split = line.replace("\n", "").split(",")
                if len(split) == 6:
                    idx, name, tribe_id, villages ,pts,rank = split
                    
                    if fname == files[0]:
                        Player_DB[idx] = {}
                        Player_DB[idx]["name"] = None
                        Player_DB[idx]["tribe_id"] = []
                        Player_DB[idx]["villages"] = []
                        Player_DB[idx]["villages_ids"] = []
                        Player_DB[idx]["pts"] = []
                        Player_DB[idx]["rank"] = []
                        Player_DB[idx]["odd"] = []
                        Player_DB[idx]["oda"] = []

                    if not (idx in Player_DB):
                        continue

                    Player_DB[idx]["name"] = name
                    Player_DB[idx]["tribe_id"].append([tribe_id, timestamp])
                    Player_DB[idx]["villages"].append([int(villages), timestamp])
                    Player_DB[idx]["pts"].append([int(pts), timestamp])
                    Player_DB[idx]["rank"].append([int(rank), timestamp])

                    if idx in odd:
                        Player_DB[idx]["odd"].append([int(odd[idx]), timestamp])

                    if idx in oda:
                        Player_DB[idx]["oda"].append([int(oda[idx]), timestamp])

                    if name == username:
                        me = idx

    files = sorted(glob.glob("tw/villages/*"))[::-1]
    Villages_DB = {}
    my_villages = []
    for fname in files:
        with open(fname, "r") as f:
            timestamp = float(fname.split("/")[-1].replace(".txt", ""))

            lines = f.readlines()
            for line in lines:
                split = line.split(",")
                if len(split) == 7: 
                    village_id, name, x, y, idx, pts, b = split
                    if idx == '0':
                        continue
                    
                    if fname == files[0]:
                        Villages_DB[village_id] = {}
                        Villages_DB[village_id]["name"] = name
                        Villages_DB[village_id]["position"] = [int(x), int(y)]
                        Villages_DB[village_id]["owner"] = idx
                        Villages_DB[village_id]["pts"] = []

                        if idx == me:
                            my_villages.append(village_id)
                        
                        Player_DB[idx]["villages_ids"].append(village_id)

                    if not (village_id in Villages_DB):
                        continue

                    Villages_DB[village_id]["pts"].append([int(pts), timestamp])

    return me, my_villages, Villages_DB, Player_DB

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def VillagesNear(Villages_DB, center_village, radius):
    r = []
    origin = Villages_DB[center_village]["position"]

    for key in Villages_DB.keys():
        dst =  Villages_DB[key]["position"]

        if distance(origin, dst) <= radius and key != center_village:
            r.append(key)
    return r

def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--me",     type=str, default="subaro98", help="You username")
    parser.add_argument("-r", "--radius", type=int, default=3,          help="Atack radius")

    return parser.parse_args()

if __name__ == "__main__":
    args = Parser()

    me, my_villages, Villages_DB, Player_DB = Make_DB(args.me)
    for my_village in my_villages:
        near = VillagesNear(Villages_DB, my_village, args.radius)
        
        plt.figure(figsize=(12,6))
        plt.subplots_adjust(bottom=0.2)
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%d-%m-%Y %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)

        show = False
        for target in near:

            player = Villages_DB[target]["owner"]
            if Player_DB[player]["pts"][-1][0] < 1000:
                continue

            pos = Villages_DB[target]["position"]
            odd = [  data[0]  for data in Player_DB[player]["odd"]]

            if len(np.unique(odd)) == 1:
                continue

            if len(odd) > 0:
                show = True
                timeline = [ float(data[1]) for data in Player_DB[player]["odd"]]
                dates=[datetime.datetime.fromtimestamp(ts) for ts in timeline]

                datenums=md.date2num(dates)
                plt.plot(datenums, odd, label=Villages_DB[target]["name"])
                plt.scatter(datenums, odd)

                print("{} - https://br101.tribalwars.com.br/game.php?village={}&screen=info_village&id={}#{};{}"
                .format(Villages_DB[target]["name"], my_village, target, pos[0], pos[1]))
        
        if show:
            plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
            plt.title("ODD variation - Radius {}".format(args.radius))
            plt.tight_layout()
            plt.savefig("{}.png".format(Player_DB[me]["name"]))
            plt.show()
        else:
            print("U Safe!")



