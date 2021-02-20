import socket
import pickle
import time
import gc
import threading
import random
import errno
import select

HEADERSIZE = 10

def getTime():
    millis= int(round(time.time() * 1000))
    return ("{:015d}".format(millis))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
        return IP


def sendWithDelay(conn, msg, delay):
    try:
        time.sleep(delay/1000)
        sent = conn.send(msg, socket.MSG_WAITALL)
    except socket.error as e:
        if e.errno == errno.ECONNRESET:
            print("Server Finish Simulation")
        elif e.errno != errno.EPIPE:
            # Not a broken pipe
            raise

def send(conn, var, delay, variance):
    d = {"time": getTime(), "data":var}
    msg = pickle.dumps(d)
    # print("[SEND] BEFORE HEADER size: {}".format(len(msg)), end= " ----> ")
    msg = bytes("{:>{}}".format(len(msg), HEADERSIZE), "utf-8") + msg
    # print("[SEND] Sending size: {}".format(len(msg)), end= " ----> ")

    delay += random.uniform(-variance, variance)

    t = threading.Thread(target=sendWithDelay, args=(conn, msg, delay))
    t.start()
    return t

def recv(sock):

    read_sockets, _, _ = select.select([sock], [], [], 0.001)
    for conn in read_sockets:
        full_msg = b''

        try:
            msg = conn.recv(HEADERSIZE)
            if len(msg) == 0:
                return None, None
        except:
                return None, None

        msg_len = int(msg)
        while msg_len > 0: 
            msg = conn.recv(msg_len)
            msg_len -= len(msg)
            full_msg += msg

        d = pickle.loads(full_msg, fix_imports=False)
        return d["data"], int(d["time"])

    return None, None

def Connect(ip = "localhost", port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setblocking(0)
    if ip == "localhost":
        ip = getIP()

    addr = (ip, port)

    while True:
        try:
            client.connect(addr)
            break
        except:
            print("Fail to Connect " + addr[0] + " " + str(addr[1]))
            time.sleep(0.5)

    return client