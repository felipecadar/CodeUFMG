import carla
import random
import time
from video_saver import VideoSaver
from collision_saver import CollisionSaver

class Simulator:
    def __init__(self, host = "localhost", port = 2000, output="output/"):
        self.actors = []
        self.auto = []

        self.output = output

        self.client = carla.Client(host, port)
        self.client.set_timeout(10.0)

        self.world = self.client.get_world()

        self.blueprint_library = self.world.get_blueprint_library()
        self.spawn_points = self.world.get_map().get_spawn_points()

        self.video_savers = []


        self.sensors = []

    def ConfigureCamera(self, blueprint, frame_width, frame_height, fps=10, fov=110):
        frame_width = str(frame_width)
        frame_height = str(frame_height)
        tic = str(1/fps)
        fov = str(fov)
        blueprint.set_attribute('image_size_x', frame_width)
        blueprint.set_attribute('image_size_y', frame_height)
        blueprint.set_attribute('fov', fov)
        # Set the time in seconds between sensor captures
        blueprint.set_attribute('sensor_tick', tic)  

    def CreateDummy(self, autopilot=True):
        car_bp = random.choice(self.blueprint_library.filter("vehicle.*"))
        position = random.choice(self.spawn_points)

        while True:
            try:
                my_actor = self.world.spawn_actor(car_bp, position)
                position = random.choice(self.spawn_points)
                break
            except:
                time.sleep(0.5)
                pass

        #collision sensor
        collision_sensor_bp = self.blueprint_library.find('sensor.other.collision')
        #collision sensor requires no configuration
        #

        #collision handler
        collision_saver = CollisionSaver("dummy", self.output, self.spawn_points)

        transform_collision_sensor = carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=0))
        collision_sensor = self.world.spawn_actor(collision_sensor_bp, transform_collision_sensor, attach_to=my_actor)
        collision_sensor.listen(lambda collision: collision_saver.HandleCollision(collision))

        my_actor.set_autopilot(autopilot)
        self.auto.append(my_actor)
        self.sensors.append(collision_sensor)

        return my_actor

    def CreateActor(self, autopilot = True, position = None, frame_size=(640, 480), fps=10):
        if not position:
            position = random.sample(self.spawn_points, 1)[0]

        #collision sensor
        collision_sensor_bp = self.blueprint_library.find('sensor.other.collision')
        #collision sensor requires no configuration
        #

        #cameras
        camera_rgb_bp = self.blueprint_library.find('sensor.camera.rgb')
        camera_depth_bp = self.blueprint_library.find('sensor.camera.depth')      
        camera_semantic_segmentation_bp = self.blueprint_library.find('sensor.camera.semantic_segmentation')

        self.ConfigureCamera(camera_rgb_bp, 640, 480, 10, 90)
        self.ConfigureCamera(camera_depth_bp, 640, 480, 10, 90)
        self.ConfigureCamera(camera_semantic_segmentation_bp, 640, 480, 10, 90)

        #car
        tesla_bp = self.blueprint_library.find("vehicle.tesla.model3")

        #camera handler
        v_id = "actor_" + str(len(self.actors))
        video_saver = VideoSaver(v_id, self.output, frame_size[0], frame_size[1])

        #collision handler
        collision_saver = CollisionSaver(v_id, self.output, self.spawn_points)

        while True:
            try:
                my_actor = self.world.spawn_actor(tesla_bp, position)
                break
            except:
                time.sleep(0.5)
                pass

        
        #Configure Actor
        my_actor.set_autopilot(autopilot)
        camera_rgb = self.world.spawn_actor(camera_rgb_bp, carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=.5)), attach_to=my_actor)
        camera_rgb.listen(lambda image: video_saver.SaveFrameRGB(image))

        camera_depth = self.world.spawn_actor(camera_depth_bp, carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=.5)), attach_to=my_actor)
        camera_depth.listen(lambda image: video_saver.SaveFrameDepth(image))

        camera_semantic_segmentation = self.world.spawn_actor(camera_semantic_segmentation_bp, carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=.5)), attach_to=my_actor)
        camera_semantic_segmentation.listen(lambda image: video_saver.SaveFrameSegmentation(image))

        #transformation function specific to collision sensor (provides easier position testing)
        transform_collision_sensor = carla.Transform(carla.Location(x=my_actor.bounding_box.extent.x, y=0, z=0))
        collision_sensor = self.world.spawn_actor(collision_sensor_bp, transform_collision_sensor, attach_to=my_actor)
        collision_sensor.listen(lambda collision: collision_saver.HandleCollision(collision))

        self.actors.append(my_actor)
        self.video_savers.append(video_saver)
        self.sensors.append(camera_depth)
        self.sensors.append(camera_rgb)
        self.sensors.append(camera_semantic_segmentation)
        self.sensors.append(collision_sensor)

        return my_actor

    def EndSimulation(self):

        print("Stoping all recordings...", end="")
        for c in self.video_savers:
            c.stopAll()
        print("Done!")

        print("Stoping all sensors...", end="")
        for a in self.sensors:
            a.destroy()
        print("Done!")

        print("Killing all actors...", end="")
        for a in self.actors:
            a.destroy()

        for a in self.auto:
            a.destroy()
        print("Done!")