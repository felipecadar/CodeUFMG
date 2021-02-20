#!/usr/bin/env python3
import pygame
import threading
import numpy as np
import socket
import random
from protocol import send, recv, Connect, getTime
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",    type=int, default=5555, help="Socket port")
    return parser.parse_args()

class HumanControll:
    def __init__(self, speed = 1):
        self.joyX = 0
        self.joyY = 0
        self.joyD = 0
        self.speed = speed
        self.thread = threading.Thread(target=self.startController, args=())
        self.thread.start()
        
        self.done = False

    def startController(self):
        # Initialize pygame for joystick support
        pygame.display.init()
        pygame.joystick.init()
        controller = pygame.joystick.Joystick(0)
        controller.init()
        i = 0        
        while True and not self.done:
            # Get next pygame event
            pygame.event.pump()
            self.joyX = int(np.rint(controller.get_axis(0) * self.speed))
            self.joyY = int(np.rint(controller.get_axis(1) * self.speed))
            self.joyD = controller.get_axis(3)

    def stop(self):
        self.thread.join()

    def start(self, conn):
        done = False
        diff = 0
        observation, reward = 0,0
        try:
            while not done:
                delay = (self.joyD + 1) * 500
                variance = 0
                action = [self.joyX, self.joyY]
                sent = send(conn, action, delay, variance)
                ans, send_time = recv(conn)

                if not (ans is None):
                    observation, reward, done = ans
                    recv_time = int(getTime())
                    diff = recv_time - send_time
                    print("Reward: {:.5f} | Done: {} | Delay {:3d}ms".format(reward, done, diff))

            self.stop()
            
        except socket.error as e:
            print("SOCKET ERROR\n", e)
        except Exception as e:
            print(e)
            

if __name__ == "__main__":
    h = HumanControll(speed = 5)
    args = getArgs()
    port = args.port

    conn = Connect(port=port)      

    h.start(conn)

    