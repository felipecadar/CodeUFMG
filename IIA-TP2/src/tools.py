import os
import numpy as np


import errno
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

############################## Debug ##############################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
####################################################################



############################ Map Tools #############################
def loadMap(filename):
    with open(filename, "r") as f:
        line = f.readline()
        l, c, W = map(lambda x: int(x), line.strip().split(" "))

        lines = f.readlines()
        c, l = 0, 0

        for line in lines:
            if len(line) > 0:
                c = len(line.strip())
                l += 1

        ord_map = np.empty([l,c], dtype=np.int8)
        for i, line in enumerate(lines):
            if len(line) > 0:
                ord_map[i] = list(map(lambda x: ord(x), list(line.strip())))
            else:
                ord_map[i] = ord("*")
    return ord_map, W

def displayMap(char_map, save_path = ""):
    from matplotlib import pyplot as plt
    l,c = char_map.shape
    alpha = 0.5
    red = np.array([255, 0, 0], dtype=np.uint8)
    img = np.zeros([l,c, 3], dtype=np.uint8)
    img[char_map == ord('.')] = (0,0,255)
    img[char_map == ord('#')] = (0,255,255)
    img[char_map == ord('$')] = (255,255,255)

    if save_path == "":
        plt.imshow(img)
        plt.show()
