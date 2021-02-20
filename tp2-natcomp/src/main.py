#Python Libs
import os, sys, time
import multiprocessing as mp
import argparse, gc, pickle
import matplotlib.pyplot as plt

#My Libs
import ant, graph

#3-thrd Libs
import networkx as nx
from tqdm import tqdm

def free_list(a):
    del a[:]
    del a

def chunks(l, n):
    new = []
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        new.append( l[i:i + n] )
    return new

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_repetition(log_dir, exp_id):
    i = 0
    while os.path.isfile('{}/expid_{}_rep_{}.txt'.format(log_dir, exp_id, i)):
        i += 1
    return i

def printParams(dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta, rep):
    print('''
    Dataset: {}
    Exp Id: {}-{} Cores: {} Log Dir: {}
    Pop Size: {} Clycles:{} Trail Persistence: {} Trail Reguraltor: {}
    Alpha: {} Beta: {} Initial Trail: {}
    '''.format(dataset, exp_id, rep, cores, log_dir, popsize, cycles, p, q, alpha, beta, initial_trail))

def main():
    parser = argparse.ArgumentParser(description='Ant Colony Optimization')
    parser.add_argument("-p", "--popsize",      help="Population size",         default=1000,     type=int )
    parser.add_argument("-c", "--cycles",       help="Max cycles",              default=200,     type=int )
    parser.add_argument("-n", "--ncores",       help="Cores to run parallel",   default=12,     type=int )
    parser.add_argument("-d", "--dataset",      help="Dataset file",            default="datasets/graph2.txt", type=str )
    parser.add_argument("-lg", "--log",         help="Log folder",              default="log/",type=str )
    parser.add_argument("-id", "--id",          help="Experiment id",           default=2,     type=int )
    parser.add_argument("-q", "--q",            help="Trail Regulator",         default=1,   type=float )
    parser.add_argument("-prstnc", "--persistence",  help="Trail persistence",  default=0.9,   type=float )
    parser.add_argument("-i", "--initial-trail",help="Initial trail",           default=10,   type=float )
    parser.add_argument("-a", "--alpha",        help="Trail Importance",        default=2,     type=float )
    parser.add_argument("-b", "--beta",         help="Visibility Importance",   default=2,     type=float )
    parser.add_argument("-pk", "--pickle-args", help="Pickle File with params [dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta]",   default=' ',   type=str )
    parser.add_argument('-f', '--figs',         help="Save Figures and generate GIF",    action='store_true')

    args = parser.parse_args()

    pk_args = args.pickle_args

    if(os.path.isfile(pk_args)):
        dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta = pickle.load( open( pk_args, "rb" ) )
    else:
        dataset = args.dataset
        popsize = args.popsize
        cycles = args.cycles
        log_dir = args.log
        exp_id = args.id
        p = args.persistence
        initial_trail = args.initial_trail
        q = args.q
        cores = args.ncores
        alpha = args.alpha
        beta = args.beta

    figs = args.figs

    results = []
    rep = check_repetition(log_dir, exp_id)

    ensure_dir(log_dir)
    if figs: ensure_dir('figs/')
    logfile = open('{}/expid_{}_rep_{}.txt'.format(log_dir, exp_id, rep), 'w')

    #Create Environment and Colony
    Env = graph.Environment(dataset, q, p, initial_trail)
    colony = ant.GenerateColony(popsize, 1, alpha, beta)

    #Init Pool
    pool = mp.Pool(cores)

    printParams(dataset, popsize, cycles, log_dir, exp_id, p, initial_trail, q, cores, alpha, beta, rep)
    
    if figs:
        pos = nx.spring_layout(Env.G)
        graph.PlotGraph(Env.G, pos, 0)

    best_solution = []
    max_dist = 0
    for c in tqdm(range(cycles)):

        #Prepare params for parallel processing
        params = [[a, Env] for a in colony]
        free_list(colony) #free space

        #Compute solutions
        colony = pool.map(ant.RunAnt, params)

        #Update trails
        Env.UpdateTrail(colony)

        #Log results
        partial_res = []
        for a in colony:
            if max_dist < a.total_dist:
                max_dist = a.total_dist
                best_solution = a.solution
            partial_res.append(a.total_dist)
        
        results.append(partial_res)

        if figs:
            graph.PlotGraph(Env.G, pos, c+1)

        tqdm.write("Max: {}".format(max_dist))

        #Clear solutions
        for a in colony:
            a.Clear()

    nx.write_edgelist(Env.G,'{}/solution_expid_{}_rep{}.txt'.format(log_dir, exp_id, rep),data=['trail','weight'])

    logfile.write("{}\n".format(best_solution))
    for r in results:
        logfile.write("{}".format(r)[1:-1]+"\n")

    if figs: #gen gif
        os.system("convert -delay 20 -loop 0 figs/*.png result.gif")

if __name__ == '__main__':
    main()
