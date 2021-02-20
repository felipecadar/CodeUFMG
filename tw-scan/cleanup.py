import urllib, requests
import time, os
import pathlib
import datetime
import glob
import ntpath

print("Clean up")
print(datetime.datetime.now())

here = str(pathlib.Path(__file__).parent.absolute())

if os.path.isdir(here + "/tw"):
    for filename in glob.glob(here + "/tw/**/*.txt"):
        #abs((a - datetime.datetime.now()).days)
        head, tail = ntpath.split(filename)
        ts = float(tail.split(".")[0])

        date = datetime.datetime.fromtimestamp(ts)

        if abs((date - datetime.datetime.now).days) > 7:
            print("removing {}".format(filename))
            os.remove(os.path.abspath(filename))