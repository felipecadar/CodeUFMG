import os
from GeneticTools.Structs import Tree, Operators
from GeneticTools.Tools import *
import gc, sys
import pickle
import time
import numpy as np
import multiprocessing as mp
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genetic Algorithm')
    parser.add_argument("-p", "--popsize",      help="population size",         default=50,     type=int )
    parser.add_argument("-k", "--tournament",   help="tournament size",         default=7,      type=int )
    parser.add_argument("-g", "--generations",  help="max generations",         default=1000,   type=int )
    parser.add_argument("-m", "--mutation",     help="mutation prob",           default=0.9,    type=float )
    parser.add_argument("-c", "--cores",        help="used processors",         default=4,      type=int )
    parser.add_argument("-d", "--dataset",      help="dataset file",            default="datasets/synth1/synth1-train.csv", type=str )
    parser.add_argument("-lg", "--log",         help="log folder",              default="log/", type=str )
    parser.add_argument("-md", "--max_depth",   help="Depth limit",             default=6,      type=int )
    parser.add_argument("-id", "--id",          help="Experiment id",           default=0,      type=int )
    parser.add_argument("-t", "--threshold",    help="Solution Threshold",      default=0.001,    type=float )
    parser.add_argument('-el',                  help="Use Elitism",             action='store_true')

    args = parser.parse_args()

    print(vars(args))
    print(Operators().printOps())


    tournament_size = args.tournament
    log = args.log
    threshold = args.threshold
    popsize = args.popsize
    dataset = args.dataset
    mutation = args.mutation
    generations = args.generations
    max_level = args.max_depth
    cores = args.cores
    values = np.genfromtxt(dataset, delimiter=',')
    Ymean = np.mean(values[:,-1])
    var_size = values.shape[1] -1 
    mean_error = np.sum((values[:,-1] - Ymean)**2)
    elitism = args.el
    exp_id = args.id

    if not os.path.exists(log):
        os.makedirs(log)

    filename = "{}/id_{}__p_{}__k_{}__g_{}__m_{}__c_{}__d_{}__md_{}__t_{}__el_{}.txt".format(log, exp_id, popsize, tournament_size,
    generations, mutation, cores, dataset.split('/')[-1].split('.')[0] ,max_level, threshold, elitism)

    #Initial Population
    Pop = RandomPop(popsize, dataset, var_size, max_level)
    pool = mp.Pool(processes=cores)

    fits = []
    params = [[g, values, mean_error] for g in Pop]
    fits = pool.map(getFitness, params)

    total_fits = []
    total_fits.append(fits)
    interval = 1

    time_to_exploit = 0.30
    iter_to_exploit = int(time_to_exploit * generations)

    for generation in range(generations):

        # if generation % iter_to_exploit == 0 and generation > 0:
        #     print("Starting Exploitation")
        #     mutation = 1 - mutation
        #     tournament_size = int(0.5 * popsize)
        #     elitism = True

        if generation % interval == 0:
            print("GEN {} Min fit {}, Max Fit {}, Popsize {}".format(generation, min(fits), max(fits), len(Pop)))

        if min(fits) <= threshold:
            print("FOUND THE SOLUTION HUEHEUHEUEH")
            solutions = [[Pop[i], fits[i]] for i in range(popsize) ]
            top = [x[0] for x in sorted(solutions, key=lambda  x:x[1])][:2]
            for g in top:
                print("--")
                g.printTree()

            pickle.dump(top , open( filename+'.p', "wb" ) )
            sys.exit()


        new_pop = []
        
        total = 0
        while total < popsize:
            if total == popsize - 1:
                selec = Tournament(Pop,tournament_size, fits, 1)
                new_pop.append([Mutate(selec[0]), selec])
                total += 1
            else:
                rand = np.random.rand()
                if rand <= mutation:
                    selec = Tournament(Pop,tournament_size, fits, 1)
                    new_pop.append([Mutate(selec[0]), selec])
                    total += 1
                else:
                    selec = Tournament(Pop,tournament_size, fits, 2)
                    C, D = Crossover(selec[0], selec[1])
                    new_pop.append([C, selec])
                    new_pop.append([D, selec])
                    total += 2
        
        params = [[g, values, mean_error] for g in [ x for x,_ in new_pop ]    ]
        new_fits = []
        new_fits = pool.map(getFitness, params)

        if elitism:
            new_new_pop = []
            for i in range(popsize):
                new = new_pop[i][0]
                old = new_pop[i][1]

                if len(old) == 1:
                    if new_fits[i] < fits[Pop.index(old[0])]:
                        new_new_pop.append(new)
                    else:
                        new_new_pop.append(old[0])
                else:
                    if fits[Pop.index(old[0])] < fits[Pop.index(old[1])]:
                        best_father = old[0]
                        best_fit = fits[Pop.index(old[0])]
                    else:
                        best_father = old[1]
                        best_fit = fits[Pop.index(old[1])]

                    if new_fits[i] < best_fit:
                        new_new_pop.append(new)
                    else:
                        new_new_pop.append(best_father)

            Pop = new_new_pop[:]
            fits = new_fits[:]
            total_fits.append(fits)

        else:
            Pop = [ g for g,_ in new_pop]

            fits = new_fits[:]
            total_fits.append(fits)

        if generation % 100 == 0:
            # print("Saving generation {} logs".format(generation))
            Log(total_fits, filename)

    Log(total_fits, filename)
    print("END")
    solutions = [[Pop[i], fits[i]] for i in range(popsize) ]
    top = [x[0] for x in sorted(solutions, key=lambda  x:x[1])][:2]
    pickle.dump(top , open( filename+'.p', "wb" ) )
    sys.exit()
