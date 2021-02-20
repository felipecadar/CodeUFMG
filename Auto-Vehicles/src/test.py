import carla
import random

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()

blueprint_library = world.get_blueprint_library()

tesla_bp = blueprint_library.find("vehicle.tesla.model3")
all_vehicles = blueprint_library.filter("vehicle.*")

camera_semantic_segmentation_bp = blueprint_library.find('sensor.camera.semantic_segmentation')
camera_rgb_bp = blueprint_library.find('sensor.camera.rgb')
camera_depth_bp = blueprint_library.find('sensor.camera.depth')

spawn_points = world.get_map().get_spawn_points()

transform = carla.Transform(carla.Location(x=230, y=195, z=40), carla.Rotation(yaw=180))

spaw_points = random.sample(spawn_points, 41)
my_actor = world.spawn_actor(tesla_bp, spaw_points[0])
my_actor.set_autopilot(True)
camera_rgb = world.spawn_actor(camera_rgb_bp, carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=.5)), attach_to=my_actor)
camera_rgb.listen(lambda image: image.save_to_disk('output/{}.png'.format(image.timestamp)))
# camera_rgb.listen(lambda image: print(image.frame))

actors_list = []
for sp in spaw_points[1:]:
    actors_list.append(world.spawn_actor(random.choice(all_vehicles), sp))
    actors_list[-1].set_autopilot(True)

input()



def kill():
    my_actor.destroy()
    for actor in actors_list:
        actor.destroy()

kill()