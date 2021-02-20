from protocol import *
import numpy as np
import socket

data = np.zeros([12])

delay = 10
var = 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5555
server = getIP()

try:
    sock.bind((server, port))
    sock.listen(1)
    print("Wainting...")
except socket.error as e:
    str(e)

conn, addr = sock.accept()
conn.setblocking(0)
i = 0

delays = []

while True:
    ans, time = recv(conn)
    if ans is None:
        print(".", end="")
    else:
        print("\n\n", type(ans), time, "\n\n")

    if i == 0:
        send(conn, data, delay, var)

    i = (i + 1) % 1000