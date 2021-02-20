import argparse
import tqdm
import multiprocessing
from datetime import datetime
from tools import *
import pickle
import os

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--stop", type=float, default=0.01, help="Stop fitness value")
    parser.add_argument("-g","--gen", type=int, default=1000, help="Number of max generation")
    parser.add_argument("-s","--size", type=int, default=50, help="Population Size")
    parser.add_argument("--seed", type=int, default=-1, help="Numpy random seed")
    parser.add_argument("-k","--K", type=int, default=10, help="Tournament participation")
    parser.add_argument("-a","--alpha", type=float, default=0.8, help="Crossover probability")
    parser.add_argument("-f","--fitness", type=str, default="ABS", choices=["ABS","MSE","RMSE"], help="Fitness type")
    parser.add_argument("-p","--population", type=str, default="ramped-hh", choices=["ramped-hh","full","grow", "descend-prob"], help="Initial population type")
    parser.add_argument("-d","--depth", type=int, default=7, help="Tree max depth")
    parser.add_argument("-e","--elit", action="store_true", default=False, help="Use Elitism")
    parser.add_argument("-i","--input", type=str, default="datasets/01-SR_div.txt", help="Input dataset file")
    parser.add_argument("-o","--output", type=str, default="results", help="Output results folder")
    parser.add_argument("-c","--cores", type=int, default=-1, help="Parallel Cores. -1 means all cores")
    parser.add_argument("--id", type=str, default="", help="Experiment identifier. Time of execution as default")

    return parser.parse_args()


if __name__ == "__main__":

    ## Parse Args
    args = parseArgs()
    print("######### CONFIG ##########")
    for key, val in args.__dict__.items():
        print("{:>10} -> {}".format(key, val))
    print("###########################")

    ## Get/Set Seed
    seed = args.seed
    if args.seed == -1:
        seed = np.random.randint(0, 100000000)
        print("Using generated seed:", seed)

    np.random.seed(seed)

    exp_id = args.id
    if len(exp_id) == 0:
        exp_id = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    output_path = os.path.join(args.output, exp_id)
    mkdirp(output_path)

    ## Save config
    experiment_data = {}
    experiment_data["args"] = args
    experiment_data["seed"] = seed

    ## Load Dataset
    dataset = np.loadtxt(args.input)
    n_var = dataset.shape[1] - 1 # number of variables

    ## Precompute levels
    levels = getLevels(args.depth)

    ## Setup parallel pool
    cpu = args.cores
    if args.cores == -1:
        cpu = os.cpu_count()
    pool = multiprocessing.Pool(processes=cpu)

    ## Metrics
    best_fit_hist = np.zeros(args.gen)
    mean_fit_hist = np.zeros(args.gen)
    worse_fit_hist = np.zeros(args.gen)
    unique_ind_hist = np.zeros(args.gen)

    total_mutation_branch_hist = np.zeros(args.gen)
    total_mutation_node_hist = np.zeros(args.gen)
    total_crossover_hist = np.zeros(args.gen)

    child_better_mutation_branch_hist = np.zeros(args.gen)
    child_better_mutation_node_hist = np.zeros(args.gen)
    child_better_crossover_hist = np.zeros(args.gen)
    
    mean_fit_mutation_branch_hist = np.zeros(args.gen)
    mean_fit_mutation_node_hist = np.zeros(args.gen)
    mean_fit_crossover_hist = np.zeros(args.gen)

    mean_fit_mutation_branch_child_hist = np.zeros(args.gen)
    mean_fit_mutation_node_child_hist = np.zeros(args.gen)
    mean_fit_crossover_child_hist = np.zeros(args.gen)

    ## Gen first Population
    new_pop = pop = genPop(args.depth, args.size, n_var, pop_type=args.population)
    fit = None

    pbar = tqdm.tqdm(range(args.gen), desc=args.id)
    for generation in pbar:
        exploration = 1 - (generation / args.gen)
        
        pop = new_pop
        last_fit = fit

        pool_args = []
        for ind in pop:
            pool_args.append((ind, dataset, args.fitness))
        fit = pool.map(fitnessParallel, pool_args)

        ## Metrics to compare crossover and mutation improvment!
        if generation > 0:
            mut_node = []
            mut_branch = []
            cross = []
            mut_node_child = []
            mut_branch_child = []
            cross_child = []
            for idx, el in enumerate(evolution_hist):
                if el["type"] == "branch-mutation":
                    parent = el['origin']
                    mut_branch.append(last_fit[parent])
                    mut_branch_child.append(fit[idx])

                    total_mutation_branch_hist[generation] += 1
                    if fit[idx] > last_fit[parent]:
                        child_better_mutation_branch_hist[generation] += 1


                elif el["type"] == "node-mutation":
                    parent = el['origin']
                    mut_node.append(last_fit[parent])
                    mut_node_child.append(fit[idx])

                    total_mutation_node_hist[generation] += 1
                    if fit[idx] > last_fit[parent]:
                        child_better_mutation_node_hist[generation] += 1

                elif el["type"] == "crossover":
                    parent = el['origin']
                    cross.append(last_fit[parent])
                    cross_child.append(fit[idx])

                    total_crossover_hist[generation] += 1
                    if fit[idx] > last_fit[parent]:
                        child_better_crossover_hist[generation] += 1
            
            if len(mut_branch) > 0:
                mean_fit_mutation_branch_hist[generation] = np.mean(mut_branch)
                mean_fit_mutation_branch_child_hist[generation] = np.mean(mut_branch_child)
    
            if len(mut_node) > 0:
                mean_fit_mutation_node_child_hist[generation] = np.mean(mut_node_child)
                mean_fit_mutation_node_hist[generation] = np.mean(mut_node)

            if len(cross) > 0:
                mean_fit_crossover_hist[generation] = np.mean(cross)
                mean_fit_crossover_child_hist[generation] = np.mean(cross_child)

        ##### General Metrics
        best_fit_hist[generation] = sorted(fit)[0]
        worse_fit_hist[generation] = sorted(fit)[-1]
        mean_fit_hist[generation] = np.mean(fit)
        unique_ind_hist[generation] = len(np.unique(pop, axis=0))

        ##### Print Progress
        if generation % 20 == 0:
            best_fit = sorted(fit)[0]
            mean_fit = np.mean(fit)
            tqdm.tqdm.write("Best fit: {} | Mean fit: {} | Unique Indv {}/{}".format(
                best_fit, mean_fit, len(np.unique(pop, axis=0)), args.size
            ))
            pbar.set_description("{} {}".format(args.id, best_fit))

        #### Stop Condition
        if np.min(fit) < args.stop:
            break
        
        #### Selection
        evolution_hist = []
        new_pop = selection(pop, fit, args.depth, n_var, levels, args.elit, args.K, args.alpha, args.size, exploration, evolution_hist)



    indexes = list(range(len(fit)))
    sorted_indexes = [x for _,x in sorted(zip(fit,indexes))]

    experiment_data["best_fit_hist"] = best_fit_hist
    experiment_data["worse_fit_hist"] = worse_fit_hist
    experiment_data["mean_fit_hist"] = mean_fit_hist
    experiment_data["unique_ind_hist"] = unique_ind_hist
    experiment_data["last_generation"] = generation
    experiment_data["last_population"] = pop
    experiment_data["mean_fit_mutation_branch_hist"] = mean_fit_mutation_branch_hist
    experiment_data["mean_fit_mutation_node_hist"] = mean_fit_mutation_node_hist
    experiment_data["mean_fit_crossover_hist"] = mean_fit_crossover_hist
    experiment_data["mean_fit_mutation_branch_child_hist"] = mean_fit_mutation_branch_child_hist
    experiment_data["mean_fit_mutation_node_child_hist"] = mean_fit_mutation_node_child_hist
    experiment_data["mean_fit_crossover_child_hist"] = mean_fit_crossover_child_hist
    experiment_data["total_crossover_hist"] = total_crossover_hist
    experiment_data["total_mutation_branch_hist"] = total_mutation_branch_hist
    experiment_data["total_mutation_node_hist"] = total_mutation_node_hist
    experiment_data["child_better_crossover_hist"] = child_better_crossover_hist
    experiment_data["child_better_mutation_branch_hist"] = child_better_mutation_branch_hist
    experiment_data["child_better_mutation_node_hist"] = child_better_mutation_node_hist


    pickle.dump( experiment_data, open( os.path.join(output_path, "experiment_data.pkl"), "wb" ) )

    # plt.figure()
    # plt.plot(best_fit_hist[:generation])
    # # plt.plot(worse_fit_hist[:generation])
    # # plt.plot(mean_fit_hist[:generation])
    # plt.figure()
    # plt.plot(unique_ind_hist[:generation])

    # print("End in generation", generation)
    # for idx in sorted_indexes[:10]:
    #     print(fit[idx],"-->",pp(pop[idx]))

    # plt.show()