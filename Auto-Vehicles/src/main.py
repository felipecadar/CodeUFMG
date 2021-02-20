import argparse
import sys
import os
import logging as lg
import time
from dataset_generator import Simulator

# lg.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=lg.DEBUG)

def config(args):
    for k,v in args.__dict__.items():
        lg.info("{}: {}".format(k,v))

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--agents", type=int, help="number of agents recording", default = 1)
    parser.add_argument("-v", "--vehicles", type=int, help="number of random vehicles in the city", default = 30 )
    parser.add_argument("-o", "--output", type=str, help="output path for logs and images", default = "output/")
    parser.add_argument("-t", "--time", type=float, help="time in minutes to run the simulation", default = 0.1)
    parser.add_argument("-q", "--quiet", action="store_true", help="dont print logs")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parser()
    if args.quiet:
        lg.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=lg.INFO)
    else:
        lg.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=lg.DEBUG)
        config(args)

    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    sim = Simulator(output=args.output)

    for i in range(args.agents):
        sim.CreateActor()

    for i in range(args.vehicles):
        sim.CreateDummy()

    try:
        print(int(args.time * 60))
        time.sleep(int(args.time * 60))
    except Exception as e:
        print(sys.exc_info()[0])
        print(e)

    print("Killing simulation...")
    sim.EndSimulation()
    print("End simulation")