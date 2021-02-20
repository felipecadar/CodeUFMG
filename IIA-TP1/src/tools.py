import os
import numpy as np


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

def shoudPrint(level):
    s = True
    if "TP_DEBUG" in os.environ:
        if level > int(os.environ.get("TP_DEBUG")):
            s = False
    return s

def warning(text):
    if shoudPrint(1):
        print(bcolors.WARNING + text + bcolors.ENDC)
    
def info(text):
    if shoudPrint(2):
        print(bcolors.OKBLUE + text + bcolors.ENDC)
    
def confirm(text):
    if shoudPrint(3):
        print(bcolors.OKGREEN + text + bcolors.ENDC)

def fail(text):
    if shoudPrint(0):
        print(bcolors.FAIL + text + bcolors.ENDC)

####################################################################

############################ Map Tools #############################
def findEntries(char_map):
    start_points = []
    for i in range(char_map.shape[0]):
        for j in [0, char_map.shape[1] - 1]:
            if char_map[i, j] == ord("#") or char_map[i, j] == ord("."):
                start_points.append((i, j))

    for i in [0, char_map.shape[0] - 1]:
        for j in range(char_map.shape[1]):
            if char_map[i, j] == ord("#") or char_map[i, j] == ord("."):
                start_points.append((i, j))
    return start_points

def valid_coord(p, s):
    return p[0] >= 0 and p[1] >= 0 and p[0] < s[0] and p[1] < s[1]

def loadMap(filename):
    with open(filename, "r") as f:
        line = f.readline()
        l, c, W = map(lambda x: int(x), line.strip().split(" "))
        info("Loading map [%i, %i] W= %i" % (l,c,W))

        ord_map = np.empty([l,c], dtype=np.int8)
        for i in range(l):
            line = f.readline()
            if len(line) > 0:
                ord_map[i] = list(map(lambda x: ord(x), list(line.strip())))
            else:
                ord_map[i] = ord("*")
    return ord_map, W

def displayMap(char_map, save_path = ""):
    if shoudPrint(4):
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


def displayPath(char_map, path, interval, save_path = ""):
    if shoudPrint(4):
        import cv2
        l,c = char_map.shape
        alpha = 0.8
        red = np.array([255, 0, 0], dtype=np.uint8)
        img = np.zeros([l,c, 3], dtype=np.uint8)
        img[char_map == ord('.')] = (0,0,255)
        img[char_map == ord('#')] = (0,255,255)
        img[char_map == ord('$')] = (255,255,255)
        for move in path:
            img[move[0], move[1]] = (img[move[0], move[1]] * (1-alpha)) + (red * alpha)
        if len(path)>0:
            img[path[-1]] = red

        if save_path == "":
            img = img[:, :, ::-1]
            img = cv2.resize(img, None, fx=50, fy=50, interpolation=cv2.INTER_NEAREST)
            cv2.imshow("path", img)
            cv2.waitKey(interval)
        return img

def displayAstar(char_map, open_list, closed, interval, H, G):
    if shoudPrint(4):
        import cv2
        l,c = char_map.shape
        alpha = 0.8
        red = np.array([255, 0, 0], dtype=np.uint8)

        img = np.zeros([l,c, 3], dtype=np.uint8)
        img[char_map == ord('.')] = (255,255,255)
        img[char_map == ord('#')] = (140,140,140)
        img[char_map == ord('$')] = (0,255,0)

        img[closed == 1] = (0,0,255)

        for move in open_list:
            img[move] = (255, 0, 0)


        # img = img[:, :, ::-1]
        img = cv2.resize(img, None, fx=50, fy=50, interpolation=cv2.INTER_NEAREST)

        i_delta = img.shape[0] / char_map.shape[0]
        j_delta = img.shape[1] / char_map.shape[1]
        for i in range(char_map.shape[0]):
            for j in range(char_map.shape[1]):
                cv2.putText(img, "H %.1f" % H[i,j]            , (int(j * j_delta) + 10, int(i * i_delta) + 10), 0, 0.3, (0,0,0) )            
                cv2.putText(img, "F %.1f" % (G[i,j] + H[i,j]) , (int(j * j_delta) + 10, int(i * i_delta) + 25), 0, 0.3, (0,0,0) )            
                cv2.putText(img, "G %.1f" % G[i,j]            , (int(j * j_delta) + 10, int(i * i_delta) + 40), 0, 0.3, (0,0,0) )            

        cv2.imshow("path", img)
        cv2.waitKey(interval)