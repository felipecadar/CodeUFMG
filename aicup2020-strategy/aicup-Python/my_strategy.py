import model
import math
import numpy as np
# import cv2
from utils import *


class MyStrategy:
    def get_action(self, player_view, debug_interface):

        POP_LIM = 10
        BUILD_COLLECT_RATE = 0.2

        # fog_of_war = player_view.fog_of_war # False
        # max_tick_count = player_view.max_tick_count
        # max_pathfind_nodes = player_view.max_pathfind_nodes
        # current_tick = player_view.current_tick
        # players = player_view.players

        my_id = player_view.my_id
        map_size = player_view.map_size # 80
        entity_properties = player_view.entity_properties
        entities = player_view.entities

        # print(my_id)
        if my_id == 1:
            key_location = model.Vec2Int(map_size,map_size)
        if my_id == 2:
            key_location = model.Vec2Int(0,0)
        if my_id == 3:
            key_location = model.Vec2Int(0,map_size)
        if my_id == 4:
            key_location = model.Vec2Int(map_size,0)

        actions = {}

        ## Gen ocupation map
        ocup_map = np.zeros([player_view.map_size, player_view.map_size], dtype=np.uint8)        
        for e in entities: 
            if e.entity_type not in UNITS:
                e_size = entity_properties[e.entity_type].size
                c = 80 - e.position.x
                l = e.position.y
                ocup_map[l:l+e_size, c-e_size:c] = 255

        # cv2.imshow("a", cv2.resize(ocup_map, (800,800), interpolation=cv2.INTER_NEAREST))
        # cv2.waitKey(1)

        ## Get empty locations
        _zeros = np.where(ocup_map == 0)
        l_pos = list(_zeros[0])
        c_pos = list(_zeros[1])
        empty = [model.Vec2Int(80 - c, l) for l,c in  zip(l_pos, c_pos)]

        ## Get Resources
        resources = sorted(list(filter(lambda e: e.entity_type == model.EntityType.RESOURCE, entities)), key=lambda e: e.id)

        ## All my entities
        my_entities = sorted(list(filter(lambda e: e.player_id == player_view.my_id, entities)), key=lambda e: e.id)

        # ## Get Key Location
        # key_location = None
        # for e in my_entities:
        #     if e.entity_type == model.EntityType.BUILDER_BASE:
        #         key_location = e.position
        #         break
        #     elif e.entity_type in BASES:
        #         key_location = e.position

        ## Separate my units
        entities_dict = {}
        for i in model.EntityType:
            entities_dict[i] = list(filter(lambda e: e.entity_type == i, my_entities))

        ## Extract Population Info
        used_population = 0
        max_population = 0
        for e in my_entities: used_population += entity_properties[e.entity_type].population_use
        for e in my_entities: max_population += entity_properties[e.entity_type].population_provide

        print("Pop: {}/{}".format(used_population, max_population))

        # Send builders to colect resources
        used_resources = []
        n_builders = len(entities_dict[model.EntityType.BUILDER_UNIT])
        for idx, e in enumerate(entities_dict[model.EntityType.BUILDER_UNIT]):
            props = entity_properties[e.entity_type]

            move_action = None
            build_action = None
            attack_action = None
            repair_action = None
            # (idx <= n_builders * BUILD_COLLECT_RATE)
            if idx == 0 and n_builders > 5:
                loc = findSpace(ocup_map, entity_properties[model.EntityType.HOUSE].size, empty, key_location)
                d = dist(loc, e.position)
                print("Loc",loc, "Dist", d)
                if  d <= 0.01:
                    build_action = model.BuildAction(model.EntityType.HOUSE, model.Vec2Int(loc.x - entity_properties[model.EntityType.HOUSE].size, loc.y))
                else: 
                    move_action = model.MoveAction( loc , find_closest_position=True, break_through=True)
                    # attack_action = model.AttackAction(None, model.AutoAttack(1, RESOURCES))
            else:
                ## Select Resource cell            
                res_idx = getClosest(e.position, resources, used_resources)
                used_resources.append(res_idx)

                ## Move to and atack cell            
                attack_action = model.AttackAction(resources[res_idx].id, None)
                move_action = model.MoveAction( resources[res_idx].position, find_closest_position=True, break_through=False)

            actions[e.id] = model.EntityAction(move_action, build_action, attack_action, repair_action)

        # Make new builders
        for e in entities_dict[model.EntityType.BUILDER_BASE]:
            props = entity_properties[e.entity_type]

            move_action = None
            build_action = None
            attack_action = None
            repair_action = None
            
            build_action = model.BuildAction(props.build.options[0], model.Vec2Int(e.position.x + props.size, e.position.y + props.size -1 ))
            actions[e.id] = model.EntityAction(move_action, build_action, attack_action, repair_action)

        return model.Action(actions)


    def debug_update(self, player_view, debug_interface):
        debug_interface.send(model.DebugCommand.Clear())
        state = debug_interface.get_state()

        # print(state.mouse_pos_world)