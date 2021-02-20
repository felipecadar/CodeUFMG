import networkx as nx
import numpy as np
import graph
from graph import timing
import multiprocessing as mp
import matplotlib.pyplot as plt

def GenerateColony(n:int, init_position:int, alpha:float, beta:float):
    '''
    Generates Ant Colony
    params:
        n : int             -> Number of Ants in the colony
        init_position : int -> Node to initialize the Ants
        alpha : float       -> Importance factor of the trail
        beta : float        -> Importance factor of the edges weights
    '''
    colony = []
    for i in range(n):
        colony.append(Ant(i, init_position, alpha, beta))
     
    return colony

def RunAnt(p):
    '''
        Run one cycle with Ant
        param
            p: [ant, env] -> List with the Ant and the Environment
        return
            a: Ant        -> Ant After the Cycle
    '''
    a, Env= p
    reach_target = False
    #Solution needs to include the target node
    while not reach_target:
        #Choose node
        v = a.ChooseNextNode(Env, 0.1)
        #Validate solution
        if not a.valid:
            break

        #Update distance
        a.total_dist += Env.G[a.curret_node][v]['weight']
        #Move to node
        a.MoveToNode(v)

        #Time to stop ?
        if a.curret_node == Env.TargetNode:
            reach_target = True
    return a

class Ant(object):
    '''
        Ant Class
        Params:
            ant_id:int      -> Ant Identifier
            init_position   -> Node to initialize the Ant
            alpha           -> Importance factor of the trail
            beta            -> Importance factor of the edges weights
    '''
    def __init__(self, ant_id, init_position, alpha, beta):
        self.ant_id = ant_id
        self.init_position = init_position
        self.total_dist = 0
        self.alpha = alpha
        self.beta = beta
        self.valid = True
        self.curret_node = init_position
        self.solution = []
        self.tabu = [init_position]

    def Clear(self):
        ''' 
            Restart Ant
        '''
        self.solution = []
        self.tabu = []
        self.total_dist = 0
        self.valid = True
        self.tabu.append(self.init_position)
        self.curret_node = self.init_position

    def ChooseNextNode(self, Env: graph.Environment, r_error_prob = 0.1):
        ''' 
            Choose Nexto Node
            Params:
                Env: graph.Environment      -> Environment with nodes to choose
                r_error_prob : float [0:1]  -> Probability of random choice, disconsidering trail and weights
            Return:
                c:int -> Choosed Node

        '''
        choices = list(Env.G.neighbors(self.curret_node))

        #Random Error to improve exploration
        rdn = np.random.rand(1)[0]
        if rdn < r_error_prob:
            new_choices = []
            for c in choices:
                if not c in self.tabu:
                    new_choices.append(c) #possible choices
            if len(new_choices) == 0: #validade solution
                self.valid = False
                return -1
            c = np.random.choice(new_choices, 1)[0]
        else: #normal choice process
            probs = [] 
            s = Env.normFactor(self.curret_node, self.alpha, self.beta, self.tabu)

            if(s == 0):
                self.valid = False
                return -1

            #probability distribuition
            for v in choices:
                probs.append(Env.edgeProbability(self.curret_node, v, self.alpha, self.beta, self.tabu)/s)

            #validate solution
            if(sum(probs) == 0):
                self.valid = False
                return -1

            #Choose
            c = np.random.choice(np.array(choices), 1, p=probs)[0]

        #Validate again (just in case...)
        if c in self.tabu:
            self.valid = False

        return c        

    def MoveToNode(self, v):
        '''
            Move Ant to Node
            Param:
                v : int -> Node to move to
        '''
        self.solution.append([self.curret_node, v])  #Add to solution
        self.tabu.append(v)                          #Add to tabu list
        self.curret_node = v                         #Move

    def getGraph(self):
        '''
            Create graph with ants solution
            return:
                g: nx.DiGraph() -> Solution in directed graph
        '''
        g = nx.DiGraph()
        g.add_nodes_from(self.tabu)
        g.add_edges_from(self.solution)

        return g
