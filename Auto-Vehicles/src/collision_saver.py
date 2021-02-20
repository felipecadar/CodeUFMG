import os
import random
import numpy as np

class CollisionSaver:
    def __init__(self, v_id, output, spawn_poits):
            output = os.path.abspath(output)
            #collision_list is a list that contains 2-position lists, each of which has:
            #id of the actor responsible for the sensor, id of the actor we hit
            self.collision_list = []
            self.spawn_points = spawn_poits

    def HandleCollision(self, collision):
        now_collision = [collision.actor, collision.other_actor]
        self.collision_list.append(now_collision)
        print("collision saved!")

        while True:
            try:
                #position of actor (actor responsible for the sensor)
                new_positions = random.sample(self.spawn_points, 2)
                collision.actor.set_transform(new_positions[0])

                #position of other_actor (actor we hit)
                collision.other_actor.set_transform(new_positions[1])
                break
            except:
                print("actors reset!")
                pass