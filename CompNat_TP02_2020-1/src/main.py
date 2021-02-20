import numpy
import sys, os
import argparse

from utils import *
import ACO
from tqdm import tqdm

def parseArgs():
    parser = argparse.ArgumentParser("Ant Colony Optimization - Longest Path")
    parser.add_argument("-i", "--input",            type=str, default="bases_grafos/entrada1.txt", required=False, help="Input graph" )
    parser.add_argument("-p", "--pop-size",         type=int, default=10,   required=False, help="Number of ants" )
    parser.add_argument("-a", "--alpha",            type=int, default=1,    required=False, help="Pheromone weight" )
    parser.add_argument("-b", "--beta",             type=int, default=2,    required=False, help="Desirability weight" )
    parser.add_argument("-e", "--evaporation",      type=int, default=0.1,  required=False, help="Pheromone evaporation" )
    parser.add_argument("-m", "--max-iterations",   type=int, default=100,  required=False, help="Max Iterations" )
    
    return parser.parse_args()

if __name__ == "__main__":
    
    args = parseArgs()

    g, t = genEnv(args.input)
    # visualize(g, t)

    initial_nodes = getInitalNodes(g)

    best_sol = []
    best_val = 0

    pbar = tqdm(total=len(initial_nodes) * args.max_iterations)

    for idx, initial in enumerate(initial_nodes):
        t = np.ones(g.shape)

        colony = ACO.CreateColony(args.pop_size, initial, args.alpha, args.beta, args.evaporation)
        
        pbar.set_description("%i/%i - Best Sol %i" % (idx+1, len(initial_nodes), best_val))
        for i in range(args.max_iterations):

            solutions = []
            for ant in colony:
                s, v = ant.walk(g, t)

                if v > best_val:
                    best_val = v
                    best_sol = s
                    pbar.set_description("%i/%i - Best Sol %i" % (idx+1, len(initial_nodes), best_val))
            
            # Pheromone evaporation
            t = t * (1-args.evaporation)

            for ant in colony:
                ant.update(t)
                ant.clear()

            t[t < 1] = 1

            pbar.update()