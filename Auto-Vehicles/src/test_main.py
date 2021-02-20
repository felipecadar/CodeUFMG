import argparse
import sys
import os
import random
import logging as lg
import time
from dataset_generator import Simulator

# lg.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=lg.DEBUG)

if __name__ == "__main__":
    sim = Simulator(output="tmp")

    agent = sim.CreateActor(False)
    dummy = sim.CreateDummy(False)

    position1 = sim.spawn_points[0]
    position1.rotation.yaw = 0

    position2 = sim.spawn_points[0]
    position2.location.x += 7

    agent.set_transform(position1)
    dummy.set_transform(position2)

    try:
        time.sleep(30)
    except Exception as e:
        print(sys.exc_info()[0])
        print(e)

    print("Killing simulation...")
    sim.EndSimulation()
    print("End simulation")