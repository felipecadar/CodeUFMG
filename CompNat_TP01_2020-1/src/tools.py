import numpy as np

use_evaluate_bin = False
try:
    from evaluate_module import evaluate as evaluate_bin
    use_evaluate_bin = True
    print("Using cpp fitness computation")
except:
    use_evaluate_bin = False


# np.random.seed(7891)

MAX_VAL = 10000

nodes_dict = {
    # op_id: [op_str, n_inputs]

    # Ints
    0:["0", 0],
    1:["1", 0],
    2:["2", 0],
    3:["3", 0],
    4:["4", 0],
    5:["5", 0],
    6:["6", 0],
    7:["7", 0],
    8:["8", 0],
    9:["9", 0],
    
    # Basic Ops
    10:["+", 2],
    11:["-", 2],
    12:["/", 2],
    13:["*", 2],

    # Complex Ops
    # 14:["^", 2],
    15:["^2", 1],
    # 16:["e^", 1],
    17:["log_e", 1],
    
    # Consts
    17:["e", 0],
    18:["pi", 0],

    # Placeholder
    99:["", 0],

    #Variables >= 100
}

child_0 = [key for key in nodes_dict.keys() if nodes_dict[key][1] == 0]
child_1 = [key for key in nodes_dict.keys() if nodes_dict[key][1] == 1]
child_2 = [key for key in nodes_dict.keys() if nodes_dict[key][1] == 2]

terminal = child_0
terminal_choice = [key for key in nodes_dict.keys() if nodes_dict[key][1] == 0 and key != 99]
not_terminal =  [key for key in nodes_dict.keys() if nodes_dict[key][1] > 0]

# print(terminal)
# print(terminal_choice)
# print(not_terminal)

def chunkIt(seq, num):
    out = [[] for i in range(num)]
    for idx, el in enumerate(seq):
        out[idx%num].append(el)
    return out


def clear(arr):
    def _clear(arr, i, log):
        if arr[i] in terminal:
            log[i] = 1
        elif arr[i] >= 100:
            log[i] = 1
        else:
            log[i] = 1
            str1 = _clear(arr, (i*2) + 1, log)
            str2 = _clear(arr, (i*2) + 2, log)
    
    log = np.zeros_like(arr)
    _clear(arr, 0, log)

    arr[log == 0] = -1

def check(arr, i=0):
    if(arr[i] < 0):
        print("ERRO")
        print(arr)
        exit()

    if arr[i] in terminal:
        return True
    elif arr[i] >= 100:
        return True 
    else:
        op = nodes_dict[arr[i]][0]
        str1 = check(arr, (i*2) + 1)
        str2 = check(arr, (i*2) + 2)
        return True

def pp(arr, i=0, var=[]):
    """Pretty Print tree.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    var:    list            -> Variables 
    """
    if(arr[i] < 0):
        print("ERRO")
        print(arr)
        exit()

    if arr[i] in terminal:
        if arr[i] < 10:
            return "{}".format(float(arr[i])/float(10.0))    
        else:
            return "{}".format(nodes_dict[arr[i]][0])    

        # return "{}".format(float(arr[i]))    
    elif arr[i] >= 100:
        # return "X_{}({})".format(arr[i] - 100, var[arr[i] - 100])    
        return "X{}".format(arr[i] - 100)    
    else:
        op = nodes_dict[arr[i]][0]
        str1 = pp(arr, (i*2) + 1, var)
        str2 = pp(arr, (i*2) + 2, var)
        return "({} {} {})".format(str1, op, str2)

# def getLevels(arr):
#     def _getLevel(arr, arr_level, level=0, i=0):
#         arr_level[i] = level
#         if arr[i] >= 10:
#             _getLevel(arr, arr_level, level + 1, (i*2)+1)
#             _getLevel(arr, arr_level, level + 1, (i*2)+2)

#     arr_level = np.zeros_like(arr)
#     _getLevel(arr, arr_level)
    
#     return arr_level

def getLevels(max_level):
    l = np.power(2, max_level) - 1
    def _getLevel(arr_level, level=0, i=0):
        arr_level[i] = level
        if i*2 + 2 > l:
            pass
        else:
            _getLevel(arr_level, level + 1, (i*2)+1)
            _getLevel(arr_level, level + 1, (i*2)+2)

    arr_level = np.zeros(l)
    _getLevel(arr_level)
    
    return arr_level


def getBelowLevels(arr):
    # print("-------------------------------------")
    def _getBelowLevel(arr, arr_level, i=0):
        # print(i, arr[i])


        if arr[i] in not_terminal:

            bellow_c1 = _getBelowLevel(arr, arr_level, (i*2)+1)
            bellow_c2 = _getBelowLevel(arr, arr_level, (i*2)+2)
            
            bellow = max(bellow_c1, bellow_c2) + 1

            arr_level[i] = bellow
            return bellow
        else:
            arr_level[i] = 0
            return 0

    arr_level = np.zeros_like(arr) - 1
    _getBelowLevel(arr, arr_level)
    
    return arr_level



def evaluate(arr, i=0, var=[]):
    """Evaluate tree with variables.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    var:    list            -> Variables 
    """
    l = arr.size

    if arr[i] in terminal:
        if arr[i] == 17: ## e
            return np.e
        if arr[i] == 18: ## pi
            return np.pi
        if arr[i] == 99:
            return np.pi
        elif arr[i] < 10: ## const
            # return float(arr[i])
            return float(arr[i])/float(10.0)
        else:
            print("Unkown node", arr[i])
            exit()
    
    elif arr[i] >= 100: ## variable
        return var[arr[i] - 100] 
    else:
        c1 = evaluate(arr, (i*2)+1, var)
        c2 = evaluate(arr, (i*2)+2, var)


        # print(c1, c2)

        if arr[i] == 10:
            return c1 + c2

        elif arr[i] == 11:
            return c1 - c2

        elif arr[i] == 12: # Protected Div
            if c2 == 0:
                # return 1
                return c1 / 0.000001
            return  c1 / c2

        elif arr[i] == 13:
            return c1 * c2

        elif arr[i] == 14:
            return np.power(c1, c2)

        elif arr[i] == 15:
            return np.power(c2, 2)

        elif arr[i] == 16:
            return np.exp(c2)
        
        elif arr[i] == 17:
            return np.log(c2)




def initGenomeFull(arr, i=0, max_level=None, n_var=0):
    """Populate tree with full lenth random genome.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    max_level:  int (default:None)  -> Max level
    n_number:   int (default:0) -> Number of variables 
    """
    if max_level is None:
        l = arr.size
    else:
        l = np.power(2, max_level) - 1

    if i*2 + 2 > l:
        if np.random.randint(0,2) and n_var > 0:
            arr[i] = np.random.randint(100, 100 + n_var) # Use variable
        else:
            arr[i] = np.random.choice(terminal_choice) # Use constant
    else :      # Use nonterminal
        new_el = np.random.choice(not_terminal)
        arr[i] = new_el

        if new_el in child_2:
            initGenomeFull(arr, (i*2)+1, max_level=max_level, n_var=n_var)
            initGenomeFull(arr, (i*2)+2, max_level=max_level, n_var=n_var)
        elif new_el in child_1:
            arr[(i*2)+1] = 99
            initGenomeFull(arr, (i*2)+2, max_level=max_level, n_var=n_var)


def initGenomeRand(arr, i=0, max_level=None, n_var=0):
    """Populate tree with random genome.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    max_level:  int (default:None)  -> Max level
    n_number:   int (default:0) -> Number of variables 
    """
    if max_level is None:
        l = arr.size
    else:
        l = np.power(2, max_level) - 1

    if i*2 + 2 > l:
        arr[i] =  np.random.choice(terminal_choice)
    else :
        if np.random.randint(0,2) and i > 0: # use terminal
            if np.random.randint(0,2) and n_var > 0:
                arr[i] = np.random.randint(100, 100 + n_var) # Use varible
            else:
                arr[i] = np.random.choice(terminal_choice) # Use constant
        else:                      # use nonterminal
            new_el = np.random.randint(10, 14)
            arr[i] = new_el
            initGenomeRand(arr, (i*2)+1, max_level=max_level, n_var=n_var)
            initGenomeRand(arr, (i*2)+2, max_level=max_level, n_var=n_var)

def initGenomeDescendProb(arr, i=0, max_level=None, n_var=0):
    """Populate tree with random genome.

    arr:    np.array        -> Genome 
    i:      int (default:0) -> Start index 
    max_level:  int (default:None)  -> Max level
    n_number:   int (default:0) -> Number of variables 
    """
    if max_level is None:
        l = arr.size
    else:
        l = np.power(2, max_level) - 1

    if i*2 + 2 > l:
        arr[i] =  np.random.choice(terminal_choice)
    else :
        prob = (l-i) / l
        if np.random.random_sample() > prob:
            if np.random.randint(0,2) and n_var > 0:
                arr[i] = np.random.randint(100, 100 + n_var)  # Use variables
            else:
                arr[i] = np.random.choice(terminal_choice)     # Use constant
        else:                      # use nonterminal
            new_el = np.random.randint(10, 14)
            arr[i] = new_el
            initGenomeDescendProb(arr, (i*2)+1, max_level=max_level, n_var=n_var)
            initGenomeDescendProb(arr, (i*2)+2, max_level=max_level, n_var=n_var)

def genPop(max_level, pop_size, n_var, pop_type = "ramped-hh"):
    n_el = np.power(2, max_level) - 1

    if pop_type == "descend-prob":
        pop = [np.zeros(n_el, dtype=np.int8)-1 for i in range(pop_size)]
        for ind in pop:
            initGenomeDescendProb(ind, n_var=n_var)
            check(ind)

    if pop_type == "full":
        pop = [np.zeros(n_el, dtype=np.int8)-1 for i in range(pop_size)]
        for ind in pop:
            initGenomeFull(ind, n_var=n_var)
            check(ind)
    
    elif pop_type == "grow":
        pop = [np.zeros(n_el, dtype=np.int8)-1 for i in range(pop_size)]
        for ind in pop:
            initGenomeRand(ind, n_var=n_var)
            check(ind)
    
    elif pop_type == "ramped-hh":
        idx_pops = list(range(int(pop_size/2)))
        sizes = list(range(2, max_level+1))

        pop_grow = [np.zeros(n_el, dtype=np.int8)-1 for i in idx_pops]
        pop_full = [np.zeros(n_el, dtype=np.int8)-1 for i in idx_pops]
        # import pdb; pdb.set_trace()
        for size_idx, chunk in enumerate(chunkIt(idx_pops, len(sizes))):
            for i in chunk:
                initGenomeRand(pop_grow[i], max_level=sizes[size_idx], n_var=n_var)
                initGenomeFull(pop_full[i], max_level=sizes[size_idx], n_var=n_var)
                check(pop_grow[i])
                check(pop_full[i])

        pop = []
        pop.extend(pop_grow)
        pop.extend(pop_full)

    return np.array(pop)

# def genIndexChildremMat(max_level):
#     def _populateMat(mat, i, n_el):
#         if i*2 + 2 > n_el: #terminal
#             mat[i, i] = 1
#         else:
#             mat[i, i] = 1
#             mat[i, (i*2)+1] = 1
#             mat[i, (i*2)+2] = 1

#             _populateMat(mat, (i*2)+1, n_el)
#             _populateMat(mat, (i*2)+2, n_el)

#             c2_nonzero = np.nonzero(mat[(i*2)+2])
#             c1_nonzero = np.nonzero(mat[(i*2)+1])


#             mat[i][c1_nonzero] = mat[(i*2)+1][c1_nonzero]
#             mat[i][c2_nonzero] = mat[(i*2)+2][c2_nonzero]

#     n_el = np.power(2, max_level) - 1
#     mat = np.zeros([n_el, n_el])
#     _populateMat(mat, 0, n_el)
#     return mat


def paste(arr1, i, arr2, j):
    arr1[i] = arr2[j]
    if arr2[j] in not_terminal:
        paste(arr1, (i*2)+1, arr2, (j*2)+1)
        paste(arr1, (i*2)+2, arr2, (j*2)+2)


# def clear(arr):
    # for i in range(1, arr.size)[::-1]:
    #     if arr[i] >= 0:
    #         if i % 2 == 1:
    #             father = arr[int((i - 1) / 2)]
    #         else:
    #             father = arr[int((i - 2) / 2)]

    #         if not (father in not_terminal):
    #             arr[i] = -1

def branchMutation(arr, n_var, levels, max_level):
    mutation_point = np.random.choice((arr >= 0).nonzero()[0])
    mutation_point_level = levels[mutation_point]

    subtree = np.zeros_like(arr) - 1
    initGenomeDescendProb(subtree, max_level=max_level-mutation_point_level, n_var=n_var)

    paste(arr, mutation_point, subtree, 0)
    clear(arr)


def nodeMutation(arr, n_var):
    mutation_point = np.random.choice((arr >= 0).nonzero()[0])

    if arr[mutation_point] in child_0 or arr[mutation_point] >= 100: ## terminal node
        if np.random.randint(0, 2): ## select between variables and consts
            arr[mutation_point] = np.random.choice(child_0)  ## select new const
        else:
            arr[mutation_point] = np.random.randint(0,n_var) + 100  ## select new variable
    # elif arr[mutation_point] in child_1:                     ## not terminal - 1side op
    #     arr[mutation_point] = np.random.choice(child_1)       ## select new - 1side op
    elif arr[mutation_point] in child_2:                       ## not terminal - 2side op
        arr[mutation_point] = np.random.choice(child_2)    ## select new 2side op

def crossover(arr1, arr2, max_level, levels):
    # check(arr1)
    bellow1 = getBelowLevels(arr1)
    bellow2 = getBelowLevels(arr2)

    possible_p1 = (arr1 >= 0)
    possible_p1[0] = False # Remove root from candidates

    p1 = np.random.choice(possible_p1.nonzero()[0]) ## select branch from arr1

    depth_p1 = levels[p1] 
    bellow_p1 = bellow1[p1]

    possible_from_arr2 = (bellow2 + depth_p1 < max_level)  ## select branchs from arr1 that do not exceds the max depth on eather three
    possible_from_arr1 = (levels + bellow_p1 < max_level)  ## select branchs from arr1 that do not exceds the max depth on eather three
    possible_p2 = (possible_from_arr1 & possible_from_arr2) & (arr2 >= 0)
    possible_p2[0] = False # Remove root from candidates

    if len(possible_p2) == 0:
        print("Crossover Error!")

    p2 = np.random.choice(possible_p2.nonzero()[0])

    tmp1 = arr1.copy()

    paste(arr1, p1, arr2, p2)
    paste(arr2, p2, tmp1, p1)

    del tmp1

    clear(arr1)
    clear(arr2)

def fitnessParallel(args):
    ind, data, loss_type = args
    return fitness(ind, data, loss_type)

def fitness(ind, data, loss_type="MSE"):
    y_pred = []
    x = data[:,:-1]
    y = data[:,-1]
    for sample in x:
        if use_evaluate_bin:
            y_pred.append(evaluate_bin(ind, 0, sample, terminal))
        else:
            y_pred.append(evaluate(ind, var=sample))

    if loss_type == "ABS":
        return np.sum(np.abs(y_pred - y))
    elif loss_type == "MSE":
        return np.mean(np.power(y_pred - y, 2))
    elif loss_type == "RMSE":
        return np.sqrt(np.sum(np.power(y_pred - y, 2)))
        
def all_pred(ind, data):
    y_pred = []
    x = data[:,:-1]
    y = data[:,-1]
    for sample in x:
        if use_evaluate_bin:
            y_pred.append(evaluate_bin(ind, 0, sample, terminal))
        else:
            y_pred.append(evaluate(ind, var=sample))

    return y_pred

def selection(pop, fit, max_level, n_var, levels, elit=False, K=2, alpha=0.8, pop_size=50, exploration=0.9, evolution_hist=[]):
    indexes = list(range(len(fit)))

    new_pop = []

    if elit:
        sorted_indexes = [x for _,x in sorted(zip(fit,indexes))]
        new_pop.append(pop[sorted_indexes[0]].copy()) # keep best
        evolution_hist.append({"type":"elit", "origin":sorted_indexes[0]})

    while len(new_pop) < pop_size:

        remain = pop_size - len(new_pop)

        ind_tourn = np.random.choice(indexes, size=K)
        fit_tourn = [fit[i] for i in ind_tourn]

        sorted_indexes = [x for _,x in sorted(zip(fit_tourn,ind_tourn))]

        if remain >= 2:
            ## crossover or mutation
            if np.random.random_sample() < alpha:
                # Crossover
                ind_1 = pop[sorted_indexes[0]].copy()
                ind_2 = pop[sorted_indexes[1]].copy()

                crossover(ind_1, ind_2, max_level, levels)

                new_pop.append(ind_1)
                new_pop.append(ind_2)
        
                evolution_hist.append({"type":"crossover", "origin":sorted_indexes[0]})
                evolution_hist.append({"type":"crossover", "origin":sorted_indexes[1]})

            else:
                # Mutation
                ind_1 = pop[sorted_indexes[0]].copy()

                if np.random.random_sample() < exploration:
                    branchMutation(ind_1, n_var, levels, max_level)
                    evolution_hist.append({"type":"branch-mutation", "origin":sorted_indexes[0]})
                else:
                    nodeMutation(ind_1, n_var)
                    evolution_hist.append({"type":"node-mutation", "origin":sorted_indexes[0]})

                new_pop.append(ind_1)
        else:
            # Mutation
            ind_1 = pop[sorted_indexes[0]].copy()

            if np.random.random_sample() < exploration:
                branchMutation(ind_1, n_var, levels, max_level)
                evolution_hist.append({"type":"branch-mutation", "origin":sorted_indexes[0]})
            else:
                nodeMutation(ind_1, n_var)
                evolution_hist.append({"type":"node-mutation", "origin":sorted_indexes[0]})

            new_pop.append(ind_1)

    return np.array(new_pop)    