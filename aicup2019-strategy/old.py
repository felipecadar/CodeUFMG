import model
import numpy as np
# import cv2

class MyStrategy:
    def __init__(self):
        pass

    def gen_map(self, unit, game, display = False):
        level = game.level.tiles
        x_len = len(level)
        y_len = len(level[0])
        map_mat = np.zeros([x_len, y_len])

        for l, line in enumerate(level):
            for c, el in enumerate(line):
                map_mat[l, c] = el

        # if display:
        #     y_len = len(level)
        #     x_len = len(level[0])
        #     img = np.zeros((x_len, y_len, 3))

        #     for l, line in enumerate(level):
        #         for c, el in enumerate(line):
        #             if el == 1:
        #                 img[x_len - c - 1, l] = np.array([0,0,255])
        #             elif el == 2:
        #                 img[x_len - c - 1, l] = np.array([0,255,0])
        #             elif el == 3:
        #                 img[x_len - c - 1, l] = np.array([255,0,0])
        #             elif el == 4:
        #                 img[x_len - c - 1, l] = np.array([255,0,255])

        #     img[x_len - int(unit.position.y) - 1 , int(unit.position.x)] = np.array([255, 255, 255])

        #     img = cv2.resize(img, None, fx=7, fy=7)
        #     cv2.imshow("map", img)
        #     cv2.waitKey(1)

        return map_mat

    def pos2np(self, position):
        return np.array([position.x, position.y])

    def get_action(self, unit, game, debug):
        # Replace this code with your own
        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

        map_mat = self.gen_map(unit, game)
        map_size = map_mat.shape

        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)
        # nearest_weapon = min(
        #     filter(lambda box: isinstance(
        #         box.item, model.Item.Weapon) and box.item.weapon_type == model.WeaponType.ASSAULT_RIFLE, game.loot_boxes),
        #     key=lambda box: distance_sqr(box.position, unit.position),
        #     default=None)
        
        nearest_health_pack = min(
            filter(lambda box: isinstance(
                box.item, model.Item.HealthPack), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)

        enemy = False
        weapon = False
        helth_pack = False
        target_pos = model.Vec2Float(0,0)

        if unit.health <= 40 and nearest_health_pack is not None:
            helth_pack = True
            target_pos = nearest_health_pack.position
        elif unit.weapon is None and nearest_weapon is not None:
            print(nearest_weapon.item.weapon_type)
            weapon = True
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            enemy = True
            target_pos.x = nearest_enemy.position.x
            target_pos.y = nearest_enemy.position.y

        shoot = False
        aim = model.Vec2Double(0, 0)
        if enemy == True:
            shoot = True
            direction = (target_pos.x - unit.position.x)

            if direction >= 0:
                target_pos.x -= 4
            else: 
                target_pos.x += 4

            
            if nearest_enemy is not None:
                aim = model.Vec2Double(
                    nearest_enemy.position.x - unit.position.x,
                    nearest_enemy.position.y - unit.position.y)

            dist = int(distance_sqr(unit.position, aim))
            if dist > 0:
                trace = np.linspace(self.pos2np(unit.position), self.pos2np(nearest_enemy.position), dist, dtype=np.int)
                trace = np.unique(trace, axis=0)

                for el in trace:
                    debug.draw(model.CustomData.Rect(model.Vec2Float((el[0] - 0.1), (el[1] - 0.1)), model.Vec2Float(0.2 , 0.2), model.ColorFloat(0, 0, 255, 1)))
                    if map_mat[el[0], el[1]] == 1:
                        shoot = False
                        break

        debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        debug.draw(model.CustomData.Log("My pos: {}".format(unit.position)))
        debug.draw(model.CustomData.Rect(model.Vec2Float(target_pos.x - 1, target_pos.y -1), model.Vec2Float(2 , 2), model.ColorFloat(0, 0, 256, 0.3)))
        debug.draw(model.CustomData.Rect(model.Vec2Float(nearest_enemy.position.x - 1, nearest_enemy.position.y -1), model.Vec2Float(2 , 2), model.ColorFloat(0, 256, 0, 0.3)))
        
        
        jump = target_pos.y > unit.position.y
        
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        
        if target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        
        return model.UnitAction(
            velocity=(target_pos.x - unit.position.x) * 10,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot=shoot,
            reload=False,
            swap_weapon=False,
            plant_mine=False)
