from tools import *
import numpy as np



# DFS ###################################################################################
def startSearchDFS(char_map, W):
    queue = findEntries(char_map)
    queue = [{"path": [], "steps_taken": 1, "position": x} for x in queue]
    status, solution = iterativeDFS(char_map, queue, np.zeros(char_map.shape), W)
    return status, solution

def iterativeDFS(char_map, queue, visited, W):
    best_sol = []
    found = False
    while len(queue) > 0:
        state = queue.pop(-1)
        start_point = state["position"]
        path = state["path"]
        steps_taken = state["steps_taken"]

        path.append(start_point)

        info("Enter (%i,%i) %i" % (start_point[0], start_point[1], steps_taken))
        displayPath(char_map, path, 10)
        
        if char_map[start_point] == ord("$"):
            found = True
            if len(best_sol) == 0:
                best_sol = path
            elif len(best_sol) > len(path):
                best_sol = path
            continue

        if char_map[start_point] == ord("#"):
            steps_taken = 0

        if steps_taken == W:
            continue
        
        x, y = start_point
        possible_moves = [(x, y-1),(x-1, y),(x+1, y),(x, y+1)]
        possible_moves = list(filter(lambda p: valid_coord(p, char_map.shape) and p not in path and char_map[p] != ord("*") , possible_moves))
        next_queue = [{"path": path[:], "steps_taken": steps_taken + 1, "position": x} for x in possible_moves]

        queue.extend(next_queue)
    
    return found, best_sol

def iterativeDepthLimitedDFS(char_map, queue, visited, W, max_depth):
    best_sol = []
    found = False
    depth_stop = False
    while len(queue) > 0:
        state = queue.pop(-1)
        start_point = state["position"]
        path = state["path"]
        steps_taken = state["steps_taken"]
        depth = state["depth"]

        path.append(start_point)

        info("Enter (%i,%i) %i" % (start_point[0], start_point[1], steps_taken))
        displayPath(char_map, path, 10)
        
        visited[start_point] = 1

        if char_map[start_point] == ord("$"):
            found = True
            if len(best_sol) == 0:
                best_sol = path
            elif len(best_sol) > len(path):
                best_sol = path
            continue

        if char_map[start_point] == ord("#"):
            steps_taken = 0

        if depth == max_depth:
            depth_stop = True
            continue

        if steps_taken == W:
            continue
        
        x, y = start_point
        possible_moves = [(x, y-1),(x-1, y),(x+1, y),(x, y+1)]
        possible_moves = list(filter(lambda p: valid_coord(p, char_map.shape) and p not in path and char_map[p] != ord("*") , possible_moves))
        next_queue = [{"path": path[:], "steps_taken": steps_taken + 1, "position": x, "depth": depth + 1} for x in possible_moves]

        queue.extend(next_queue)
    
    return found, best_sol, depth_stop

def recursiveDepthLimitedDFS(char_map, start_point, visited, W, steps_taken, path, depth, max_depth):
    info("Enter (%i,%i) %i" % (start_point[0], start_point[1], steps_taken))
    # displayPath(char_map, path, 1)
    visited[start_point] = 1
    if char_map[start_point] == ord("$"):
        return True, False, path[:]

    if char_map[start_point] == ord("#"):
        steps_taken = 0

    if depth == max_depth:
        warning("Max Depth")
        return False, True, []

    if steps_taken == W:
        return False, False, []

    x, y = start_point

    possible_moves = [(x, y-1),(x-1, y),(x+1, y),(x, y+1)]
    possible_moves = list(filter(lambda x: valid_coord(x, char_map.shape) and visited[x] == 0 and char_map[x] != ord("*"), possible_moves))

    reached_max_depth = False
    found = False
    best_solution = []
    for move in possible_moves:
        path.append(move)
        status, depth_stop, solution = recursiveDepthLimitedDFS(char_map, move, visited, W, steps_taken+1, path, depth +1, max_depth)

        if status:
            found = True
            if len(best_solution) == 0 :
                best_solution = solution[:]
            elif len(best_solution) >  len(solution):
                best_solution = solution[:]
            continue

        if depth_stop:
            reached_max_depth = True

        path.remove(move)

    visited[start_point] = 0
    return found, reached_max_depth, best_solution
    
# BSF ###################################################################################

def startSearchBFS(char_map, W):
    queue = findEntries(char_map)
    queue = [{"path": [], "steps_taken": 1, "position": x} for x in queue]
    status, solution = iterativeBFS(char_map, queue, np.zeros(char_map.shape), W)
    return status, solution


def iterativeBFS(char_map, queue, visited, W):
    best_sol = []
    found = False
    while len(queue) > 0:
        state = queue.pop(0)
        start_point = state["position"]
        path = state["path"]
        steps_taken = state["steps_taken"]

        path.append(start_point)

        info("Enter (%i,%i) %i" % (start_point[0], start_point[1], steps_taken))
        displayPath(char_map, path, 10)
        
        visited[start_point] = 1

        if char_map[start_point] == ord("$"):
            found = True
            if len(best_sol) == 0:
                best_sol = path
            elif len(best_sol) > len(path):
                best_sol = path
            continue
        
        if char_map[start_point] == ord("#"):
            steps_taken = 0

        if steps_taken == W:
            continue
        
        x, y = start_point
        possible_moves = [(x, y-1),(x-1, y),(x+1, y),(x, y+1)]
        possible_moves = list(filter(lambda p: valid_coord(p, char_map.shape) and p not in path and char_map[p] != ord("*") , possible_moves))
        next_queue = [{"path": path[:], "steps_taken": steps_taken + 1, "position": x} for x in possible_moves]

        queue.extend(next_queue)
    
    return found, best_sol


# IDS ###################################################################################

def startSearchIDS(char_map, W):
    shape = char_map.shape

    best_sol = []
    max_depth = 2
    run = True


    while run:
        max_depth += 1

        run = False
        visited = np.zeros(shape)
        queue = findEntries(char_map)
        queue = [{"path": [], "steps_taken": 1, "position": x, "depth": 1} for x in queue]

        status, solution, depth_stop = iterativeDepthLimitedDFS(char_map, queue, np.zeros(char_map.shape), W, max_depth)
        if status:
            return status, solution
        elif depth_stop:
            run = True

    return False, None


# A* ####################################################################################

def startSearchAStar(char_map, W):
    queue = findEntries(char_map)
    end = tuple( x[0] for x in np.where(char_map == ord("$")))
    status, solution = iterativeAstar(char_map, queue, W, end)
    return status, solution

def heuristic(start, end):
    return np.sqrt(np.square(start[0] - end[0]) + np.square(start[1] - end[1]))

def iterativeAstar(char_map, queue, W, end):
    G = np.zeros(char_map.shape) - 1
    H = np.zeros(char_map.shape) - 1
    parent = np.zeros([char_map.shape[0], char_map.shape[1], 2], dtype=np.int16)
    open_list = queue[:]
    closed = np.zeros(char_map.shape, dtype=np.int8)
    steps = np.zeros(char_map.shape, dtype=np.int8)
    found = False
    for x in open_list:
        H[x] = heuristic(x, end)
        G[x] = 0
        steps[x] = 1
        parent[x] = -1

    while len(open_list) > 0:
        open_list = sorted(open_list, key=lambda x: H[x] + G[x])
        current = open_list.pop(0)    

        steps_taken = steps[current]
        closed[current] = 1

        info("Enter (%i,%i) %i" % (current[0], current[1], steps_taken))

        displayAstar(char_map, open_list, closed, 100, H, G)

        if char_map[current] == ord("$"): # Found
            found = True
            path = [current]
            tmp = current
            while np.all(parent[tmp] != -1): # Path traceback
                tmp = tuple(parent[tmp])
                path.append(tmp)
            return True, path[::-1]

        if char_map[current] == ord("#"):
            steps_taken = 0

        if steps_taken == W:
            continue
        
        x, y = current
        next_queue = []
        possible_moves = [(x, y-1),(x-1, y),(x+1, y),(x, y+1)]
        possible_moves = list(filter(lambda p: valid_coord(p, char_map.shape) and char_map[p] != ord("*") , possible_moves))

        for neigh in possible_moves:
            if closed[neigh] == 0:
                if G[neigh] == -1:
                    warning("Add neigh [%i, %i]" % neigh)
                    next_queue.append(neigh)

                    steps[neigh] = steps_taken + 1
                    H[neigh] = heuristic(neigh, end)
                    G[neigh] = G[current] + 1
                    parent[neigh] = current

                if G[neigh] > G[current] + 1: # if not closed and new cost is better
                    warning("Update neigh [%i, %i]" % neigh)
                    G[neigh] = G[current] + 1
                    parent[neigh] = current

            if closed[neigh] == 0:
                if steps[neigh] > steps_taken + 1: # if new fuel is better 
                    warning("Update neigh [%i, %i] by steps" % neigh)
                    next_queue.append(neigh)
                    parent[neigh] = current
                    G[neigh] = G[current] + 1
                    steps[neigh] = steps_taken + 1

        open_list.extend(next_queue)
    
    return found, []
