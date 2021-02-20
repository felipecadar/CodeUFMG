import model
import math
import numpy as np
# entity_properties:
# size
# build_score
# destroy_score
# can_move
# population_provide
# population_use
# max_health
# cost
# sight_range
# resource_per_health
# build
# attack
# repair


UNITS = [model.EntityType.BUILDER_UNIT,
         model.EntityType.RANGED_UNIT, model.EntityType.MELEE_UNIT]
TURRETS = [model.EntityType.TURRET]
BASES = [model.EntityType.BUILDER_BASE,
         model.EntityType.RANGED_BASE, model.EntityType.MELEE_BASE]
RESOURCES = [model.EntityType.RESOURCE]
WALLS = [model.EntityType.WALL]
HOUSES = [model.EntityType.HOUSE]


def dist(p1, p2):
    return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))


def getClosest(postiton, entities, ignore_index=[]):
    best_idx = 0
    best_dist = dist(postiton, entities[0].position)
    for idx, e in enumerate(entities):
        d = dist(postiton, e.position)
        if d < best_dist:
            best_dist = d
            best_idx = idx

    return best_idx


def printProps(entity_properties):
    for i in model.EntityType:
        props = entity_properties[i]
        print(i)
        print("size:", props.size)
        print("build_score:", props.build_score)
        print("destroy_score:", props.destroy_score)
        print("can_move:", props.can_move)
        print("population_provide:", props.population_provide)
        print("population_use:", props.population_use)
        print("max_health:", props.max_health)
        print("cost:", props.cost)
        print("sight_range:", props.sight_range)
        print("resource_per_health:", props.resource_per_health)
        if props.build:
            print("build:")
            print("--> options:", props.build.options)
            print("--> init_health:", props.build.init_health)
        else:
            print("build:", props.build)

        if props.attack:
            print("attack:")
            print("--> attack_range:", props.attack.attack_range)
            print("--> damage:", props.attack.damage)
            print("--> collect_resource:", props.attack.collect_resource)
        else:
            print("attack:", props.attack)

        if props.repair:
            print("repair:")
            print("--> valid_targets:", props.repair.valid_targets)
            print("--> power:", props.repair.power)
        else:
            print("repair:", props.repair)


def findSpace(ocup_map, e_size, empty, key_location):
    def valid(position):
        c = 80 - position.x
        l = position.y
        return np.sum(ocup_map[l:l+e_size, c-e_size:c]) == 0

    if key_location.x == 0:
        x_step = 1
    else:
        x_step = -1
    if key_location.y == 0:
        y_step = 1
    else:
        y_step = -1

    x = key_location.x
    y = key_location.y
    while True:
        new_loc = model.Vec2Int(x, y)
        if valid(new_loc):
            new_loc.x += e_size
            return new_loc

        x += x_step
        if x > 30:
            x = 0
            y += y_step
    print("FAIL TO FIND VALID POSITION")
    return None
    # spaces = []
    # for e in empty:
    #     if valid(e):
    #         spaces.append([e, dist(e, key_location)])

    # spaces = sorted(spaces, key=lambda item: item[1])
    # return spaces[0][0]
