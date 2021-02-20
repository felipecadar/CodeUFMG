import numpy as np

MAX_WEIGHT = 10

def CreateColony(popsize:int, init:int, alpha:float, beta:float, evaporation:float):
    colony = []
    for i in range(popsize):
        colony.append(Ant(init, alpha, beta, evaporation))

    return colony

class Ant():
    def __init__(self, init:int, alpha:float, beta:float, evaporation:float):
        self.visited = None
        self.solution = []
        self.value = 0

        self.position = init
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation


    def clear(self):
        del self.visited
        del self.solution

        self.value = 0
        self.visited = None
        self.solution = []

    def walk(self, g, t):
        self.visited = np.zeros(len(g))
        self.visited[self.position] = 1
        # self.solution.append(self.position)

        while True:
            neigh = self.getNeigh(g)
            if len(neigh) == 0:
                break
            
            probs = self.edgeProb(neigh, g, t)
            target = np.random.choice(neigh, p=probs)

            self.visited[target] = 1

            self.value += g[self.position, target]
            self.solution.append(target)


            self.position = target     

        # import pdb; pdb.set_trace()

        return self.solution, self.value
        

    def edgeProb(self, neighs, g, t):
        probs = np.zeros(len(neighs))
        norm_sum = 0
        for idx, target in enumerate(neighs):

            Tij = t[self.position, target]
            Nij = g[self.position, target] / MAX_WEIGHT

            _p = np.power(Tij, self.alpha) * np.power(Nij, self.beta)

            probs[idx] = _p
            norm_sum += _p
            
        probs = probs / norm_sum

        return probs

    def getNeigh(self, g):
        n = np.where((g[self.position] > 0) & (self.visited == 0) )[0]
        return n


    def update(self, t):
        for i in range(len(self.solution)-1):
            t[self.solution[i], self.solution[i+1]] +=  (self.value/10)