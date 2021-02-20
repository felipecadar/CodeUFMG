import sys
import socket
import numpy as np
from protocol import getIP, recv, send, getTime
from env import TrackEnv
import argparse
import threading
import select
import matplotlib.pyplot as plt

if __name__ == "__main__":

    def getArgs():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--size",         type=int,   default=600,    help="Image Size")
        parser.add_argument("-i", "--irregularity", type=float, default=0.8,    help="track irregularity")
        parser.add_argument("-sk", "--spikeyness",  type=float, default=0.25,   help="track spikeyness")
        parser.add_argument("-n", "--nvert",        type=int,   default=8,      help="track vertices")
        parser.add_argument("-sl", "--sensor-limit",type=int,   default=60,     help="sensor limit in pixels")
        parser.add_argument("-d", "--delay",        type=int,   default=0,      help="time delay to send messages in miliseconds")
        parser.add_argument("-v", "--variance",     type=int,   default=0,      help="variance to time delay [-variance, +variance]")
        parser.add_argument("-p", "--port",         type=int,   default=5555,   help="Socket port")
        parser.add_argument("-e", "--epoch",        type=int,   default=2,      help="Epoch")

        args = parser.parse_args()
        return args

    args = getArgs()

    variance = args.variance
    delay = args.delay
    sensor_limit = args.sensor_limit
    nvert = args.nvert
    spikeyness = args.spikeyness
    irregularity = args.irregularity
    size = args.size
    epoch = args.epoch

    port = args.port
    server = getIP()
 
    env = TrackEnv(size, irregularity, spikeyness, nvert, sensor_limit)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
        s.listen(1)
    except socket.error as e:
        str(e)

    print("Waiting for a connection, Server Started at {}:{}".format(server, port))

    conn, addr = s.accept()
    print("Connected to:", addr)
    s.setblocking(0)
    threads = []
    delay_hist = []
    simulation_done = False
    MAX_STEPS = 1000
    i = 0
    while True:
        try:
            while True:
                ans, send_time = recv(conn)
                if not (ans is None) and type(ans) == type([]) and type(ans[0]) == type(True):
                    break

            print("AAAAAAAAAAAAA")
            print(ans)
            run = ans[0]
            reset_map = ans[1]

            if not run:
                break

            send(conn, True, 0, 0)

            steps = 0
            done = False
            simulation_code = 1
            observation, reward, done = env.reset(reset_map)
            print("Ep: {}".format(i))

            while env.render() and not done:
                if steps <= MAX_STEPS:
                    t = send(conn, [observation, reward, done, simulation_code], delay, variance)
                    threads.append(t)

                    ans, send_time = recv(conn)
                    if ans is None:
                        continue

                    action, ans_epoch = ans

                    if ans_epoch != i:
                        continue

                    observation, reward, done = env.step(action)
                    steps += 1

                    print("Steps: {:4d} | Reward: {:3.5f} | Delay: {:3d}ms | Threads: {} | Done: {}".format(steps, reward, int(getTime()) - send_time, threading.active_count(), done))
                    delay_hist.append(int(getTime()) - send_time)

            simulation_code = 2
            t = send(conn, [None, None, done, simulation_code], 0, 0)
            i += 1
        
        except socket.error as e:
            print(e)
            break
        except Exception as e:
            print(e)
            raise e
            break

    print("Lost connection")
    s.shutdown(1)
    conn.close()
    running = False

    for t in threads:
        t.join()


    plt.hist(delay_hist)
    plt.show()