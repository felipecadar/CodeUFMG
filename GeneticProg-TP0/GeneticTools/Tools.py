from GeneticTools.Structs import Tree, Operators
import numpy as np
# from itertools import izip
from multiprocessing import Process, Pipe
import time
import random

def Log(logs, filename):
    logFile = open(filename, 'w')
    for i in range(len(logs)):
        logFile.write("-->GEN {}\n".format(i))
        for j in range(len(logs[i])-1):
            logFile.write("{},".format(logs[i][j]))

        logFile.write("{}\n".format(logs[i][-1]))


def getFitness(params):
    root, values, mean_error = params
    error = 0
    for test in values:
        x = test[0:-1]
        y = test[-1]

        res = getResult(root, x)
        error += (y - res)**2

    fitness = np.sqrt(error/mean_error)
    return fitness

def getResult(root, variables):
    if type(root.data) in (float, int):     #Consts
        return root.data
    elif type(root.data) == str:            #Variable
        return variables[int(root.data)]
    else:                                   #Function
        res = []
        for ch in root.children:            
            res.append(getResult(ch, variables))
        return root.data(res)

def RandTree(node=None, var_size=2, max_level=6):
    if node == None:
        node = Tree(0, var_size=var_size, max_level=max_level)
    var = node.possible_variables
    if max_level == node.level:  # level is terminal
        node.setData(var[np.random.randint(0, len(var))])
    elif 0 == node.level:
        data = Operators().randOp()
        node.setData(data)
        for ch in node.children:
            RandTree(ch, var_size, max_level)
    else:
        choice = np.random.randint(0, 3)
        if choice == 0:  # operation
            data = Operators().randOp()
        elif choice == 1:  # variable #end tree
            data = var[np.random.randint(0, len(var))]
        else:              # const
            data = np.random.rand()

        node.setData(data)

        for ch in node.children:
            RandTree(ch, var_size, max_level)

    return node

def Mutate(A):
    B = CopyTree(A)
    node = SelectRandomNode(B)
    father = node.father
    
    for ch in father.children:
        if ch.id == node.id:
            father.children.remove(ch)
            break

    max_depth = B.max_level - node.level
    
    new_node = RandTree(var_size=B.var_size, max_level=max_depth)
    new_node.father = father
    new_node.max_level = B.max_level
    # new_node.correct_levels(node.level)
    
    father.children.append(new_node)
    
    # print("NEW bMAX={} mMax={}".format(B.max_level, new_node.max_level))
    # new_node.printTreeComplete()
    # print("B")
    # B.printTreeComplete()
    # print("END")

    B.correct_levels(0)
    return B

def Crossover(A, B):

    AcrossB = CopyTree(A)
    # start_time = time.time()
    BcrossA = CopyTree(B)
    # print("--- %s seconds ---" % (time.time() - start_time))

    randA = SelectRandomNode(AcrossB)

    randB = SelectRandomNode(BcrossA, max_depth=A.max_level - randA.level, max_level = A.max_level - randA.getDepth())

    FatherA = randA.father
    FatherB = randB.father

    for ch in FatherA.children:
        if ch.id == randA.id:
            FatherA.children.remove(ch)
            break
            
    for ch in FatherB.children:
        if ch.id == randB.id:
            FatherB.children.remove(ch)
            break

    FatherA.children.append(randB)
    FatherB.children.append(randA)

    AcrossB.correct_levels(0)
    BcrossA.correct_levels(0)
    

    return [AcrossB, BcrossA]

def CopyTree(src=Tree(0), dst=None):
    if dst == None:
        dst = Tree(0, var_size=src.var_size, max_level=src.max_level)

    data = src.data
    dst.setData(data)

    for s_ch, d_ch in zip(src.children, dst.children):
        CopyTree(s_ch, d_ch)

    return dst

def SelectRandomNode(root, max_depth=None, max_level=None, include_root=False):
    all_nodes = root.getAllChildren()
    if include_root == False:
        all_nodes = all_nodes[1:]
    
    if not max_depth == None:
        filtered = []
        for node in all_nodes:
            if node.getDepth() <= max_depth and node.level <= max_level:
                filtered.append(node)

        if len(filtered) == 0:
            root.printTreeComplete()
            raise ValueError('Filter in Selecting random node could not select any node',
                            'max_depth ', max_depth, 'max_level', max_level, 'all nodes len', len(all_nodes))

        selected = filtered[np.random.randint(0, len(filtered))]
    else:
        if len(all_nodes) == 0:
            root.printTree()
            raise ValueError("Can not select nodes")
        selected =  all_nodes[np.random.randint(0, len(all_nodes))]

    return selected

def Tournament(Genes, k, fits, max_select = 2):

    idx = random.sample(list(range(len(Genes))), k)
    
    Selected = [[Genes[i], fits[i]] for i in idx ]

    sort = [x for x in sorted(Selected, key=lambda  x:x[1])]

    return [r for r,_ in sort[:max_select]]

def RandomPop(k, dataset, var_size, max_level):
    pop = []
    for _ in range(k):
        g = RandTree(var_size=var_size, max_level=max_level)
        pop.append(g)

    return pop
