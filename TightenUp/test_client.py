from protocol import *
import numpy as np
import socket
import time

data = np.zeros([10, 10])

delay = 100
var = 0

sock = Connect()
# sock.setblocking(0)
i = 0

while True:
    ans, time = recv(sock)
    if ans is None:
        print(".", end="")
    else:
        print("\n\n", type(ans), time, "\n\n")

    if i == 0:
        send(sock, data, delay, var)

    i = (i + 1) % 1000