import model
import numpy as np
import math

# import cv2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def distance_sqr(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

def toDoubleVec(a):
    return model.Vec2Double(a[0], a[1])

def roundVecUp(a):
    return model.Vec2Double(math.ceil(a.x), math.ceil(a.y))

def doubleVecCopy(vec):
    return model.Vec2Double(vec.x, vec.y)

class Node:
    def __init__(self):
        self.h = None
        self.g = None
        self.parent = None
        self.used = False
        self.sum = math.inf

    def update(self):
        self.sum = self.h + self.g

    def __repr__(self):
        return "h:{}, g:{}, sum:{}, parent:{}, used:{}\n".format(
            self.h, self.g, self.sum, self.parent, self.used
        )

class MyStrategy:
    def __init__(self):
        self.last_action = False
        self.get_out = 0
        self.last_enemy = []
        self.level_mat = None
        self.last_action = None
        self.walkable_map = None
        self.new_target = False
        self.path = []

        #Params
        self.health_limit = 50
        self.enemy_distance = 3

    def gen_map(self, unit, game, display = False):
        level = game.level.tiles
        x_len = len(level)
        y_len = len(level[0])
        level_mat = np.zeros([x_len, y_len])

        for l, line in enumerate(level):
            for c, el in enumerate(line):
                level_mat[l, c] = el

        #Walkable Map
        walkable_map = np.zeros_like(level_mat, dtype=np.uint8)
        
        #Ladder
        walkable_map[level_mat == 3] = 1

        #Wall
        x, y = np.where(level_mat == 1)
        for coord in zip(x, y):
            x1, y1 = coord
            if y1+1 < walkable_map.shape[1]:
                walkable_map[x, y1+1] = 1

        #Plataform
        x, y = np.where(level_mat == 2)
        for coord in zip(x, y):
            x1, y1 = coord
            walkable_map[x1, y1] = 1
            if y1+1 < walkable_map.shape[1]:
                walkable_map[x1, y1+1] = 1
            if y1-1 < walkable_map.shape[1]:
                walkable_map[x1, y1-1] = 1

        #Remove Walls
        walkable_map[level_mat == 1] = 0

        # cv2.imshow("walkable",cv2.resize(walkable_map*255, None, fx=10, fy=10))
        # cv2.waitKey(0)
        #Ignoring Jumppads for now

        return level_mat, walkable_map

    def pos2np(self, position, dtype=None):
        if not dtype is None:
            return np.array([position.x, position.y], dtype=dtype)
        else:
            return np.array([position.x, position.y])
            

    def get_neighborhood(self, cell, walkable_map):
        x = int(cell.x)
        y = int(cell.y)

        probable_neighborhood = [[x-1, y], [x-1, y+1], [x-1, y-1],
                                 [x+1, y], [x+1, y+1], [x+1, y-1],
                                 [x, y+1], [x, y-1]]

        neighborhood = []
        for coord in probable_neighborhood:
            x1, y1 = coord
            x1 = max(0, min(x1, walkable_map.shape[0]-1))
            y1 = max(0, min(y1, walkable_map.shape[0]-1))
            
            if walkable_map[x1, y1]:
                neighborhood.append(coord)

        return neighborhood

    def find_next(self, results):
        now = results[0][0]
        coords = [-1,-1]
        for l in range(len(results)):
            for c in range(len(results[0])):
                if not results[l][c].used and results[l][c].sum < now.sum:
                    now = results[l][c]
                    coords = [l,c]
        res = model.Vec2Double(coords[0], coords[1])
        # print(res)
        return res

    def print_parents(self, results, now_cell):
        print("---------------------------------------------------------------")
        for l in range(len(results)):
            for c in range(len(results[0])):
                if l ==  now_cell.x and c == now_cell.y and results[l][c].parent is not None:
                    print((bcolors.OKGREEN + "[{:2d},{:2d}]" + bcolors.ENDC).format(results[l][c].parent[0], results[l][c].parent[1]), end = "")
                elif results[l][c].parent is not None:
                    print("[{:2d},{:2d}]".format(results[l][c].parent[0], results[l][c].parent[1]), end = "")
                else:
                    print("[     ]", end = "")

            print("")
        print("---------------------------------------------------------------")


    def astar(self, unit, target):
        int_target =  roundVecUp(target)
        
        # Distance from de source to the cell
        def g_cost(cell):
            return distance_sqr(unit.position, cell)

        # Distance from de cell to the target
        def h_cost(cell):
            return distance_sqr(target, cell)

        x_len, y_len = self.walkable_map.shape
        results  = [[Node() for y in range(y_len)] for x in range(x_len)] 
        sums = np.zeros_like(self.walkable_map, dtype=np.float)

        now_cell = roundVecUp(unit.position)
        results[now_cell.x][now_cell.y].used = True

        while True:
            neighborhood = self.get_neighborhood(now_cell, self.walkable_map)

            found = False
            for coord in neighborhood:
                vec = model.Vec2Float(coord[0], coord[1])
                if results[vec.x][vec.y].used == False:
                    results[vec.x][vec.y].parent = [now_cell.x, now_cell.y]
                    results[vec.x][vec.y].g = g_cost(vec)
                    results[vec.x][vec.y].h = h_cost(vec)
                    results[vec.x][vec.y].update()
                    
                    if results[vec.x][vec.y].h <= 0.5:
                        found = True
                        break
        
            if found:
                break

            now_cell = self.find_next(results)
            if now_cell.x == -1:
                break

            results[now_cell.x][now_cell.y].used = True

        path = [[target.x, target.y]]
        if found == False:
            return path

        init_cell = unit.position
    
        while distance_sqr(init_cell, now_cell) >= 1:
            parent = results[now_cell.x][now_cell.y].parent
            if parent is None:
                break
            now_cell = model.Vec2Double(parent[0], parent[1])
            path.append(parent)
        
        return path

    def select_target(self, unit, game):
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)

        nearest_mine = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Mine), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)

        nearest_health_pack = min(
            filter(lambda box: isinstance(
                box.item, model.Item.HealthPack), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)

        target_dict = {}

        target_dict["enemy"] = False
        target_dict["weapon"] = False
        target_dict["helth_pack"] = False
        target_dict["mine"] = False

        target_pos = model.Vec2Float(0,0)

        if unit.health <= self.health_limit and nearest_health_pack is not None:
            target_dict["helth_pack"] = True
            target_pos = nearest_health_pack.position
        elif unit.weapon is None and nearest_weapon is not None:
            target_dict["weapon"] = True
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_dict["enemy"] = True
            target_pos.x = nearest_enemy.position.x
            target_pos.y = nearest_enemy.position.y

        return target_pos, target_dict


    def get_action(self, unit, game, debug):
        # Replace this code with your own
        
        # get map once
        if (self.level_mat is None):
            self.level_mat, self.walkable_map = self.gen_map(unit, game)
            self.map_size = self.level_mat.shape

        # Move to
        final_pos, target_dict = self.select_target(unit, game)
        if target_dict["enemy"]:
            target_pos = doubleVecCopy(final_pos)

            if unit.position.x < target_pos.x:
                target_pos.x -= self.enemy_distance
            else: 
                target_pos.x += self.enemy_distance

            path = self.astar(unit, target_pos)
        else:
            path = self.astar(unit, final_pos)

        # Debug Path
        colors = np.linspace([0,255,0], [255,0,0], len(path))
        for idx, el in enumerate(path):
            debug.draw(model.CustomData.Rect(model.Vec2Float((el[0] - 0.5), (el[1] - 0.5)), model.Vec2Float(1 , 1), model.ColorFloat(colors[idx][0], colors[idx][1], colors[idx][2], 0.5)))

        target_pos = toDoubleVec(path[-1])
        target_pos.y += 0.1

        shoot = False
        aim = model.Vec2Double(0, 0)
        if target_dict["enemy"]:
            shoot = True
            
            aim = model.Vec2Double(
                final_pos.x - unit.position.x,
                final_pos.y - unit.position.y)

            dist = int(distance_sqr(unit.position, aim))
            if dist > 0:
                trace = np.linspace(self.pos2np(unit.position), self.pos2np(final_pos), dist, dtype=np.int)
                trace = np.unique(trace, axis=0)

                for el in trace:
                    debug.draw(model.CustomData.Rect(model.Vec2Float((el[0] - 0.1), (el[1] - 0.1)), model.Vec2Float(0.2 , 0.2), model.ColorFloat(0, 0, 255, 1)))
                    if self.level_mat[el[0], el[1]] == 1:
                        shoot = False
                        break
            
        jump = target_pos.y > unit.position.y

        if target_pos.x < unit.position.x:
            velocity = -10
        else:
            velocity = 10

        self.last_enemy = [e for e in game.units if e.player_id != unit.player_id]

        # print(target_pos, velocity, unit.position, aim)

        ## Debug
        # debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        # debug.draw(model.CustomData.Log("My vel: {}".format(velocity)))
        # debug.draw(model.CustomData.Log("My pos: {}".format(unit.position)))
        debug.draw(model.CustomData.Rect(model.Vec2Float(target_pos.x - 0.5, target_pos.y -0.5), model.Vec2Float(1 , 1), model.ColorFloat(0, 0, 256, 0.3)))

        action = model.UnitAction(
            velocity=velocity,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot=shoot,
            reload=False,
            swap_weapon=False,
            plant_mine=False)
        
        self.last_action = action

        return action

