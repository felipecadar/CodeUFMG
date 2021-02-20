#!/usr/bin/env python3
import pygame
import threading
from env import TrackEnv
import numpy as np

class HumanControll:
    def __init__(self, speed = 1):
        self.joyX = 0
        self.joyY = 0
        self.speed = speed
        self.thread = threading.Thread(target=self.startController, args=())
        self.thread.start()
        
        self.done = False
        self.t = TrackEnv(sensor_limit=30)

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

    def stop(self):
        self.thread.join()

    def start(self):
        done = False
        while self.t.render() and not self.done:
            action = [self.joyX, self.joyY]
            observation, reward, self.done = self.t.step(action)
            print("Reward: {:.5f} | Done: {} | Progress {}".format(reward, done, self.t.getProgress()))

        self.done = True
        self.stop()

if __name__ == "__main__":
    h = HumanControll(speed = 5)
    h.start()