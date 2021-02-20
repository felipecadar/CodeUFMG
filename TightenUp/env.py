from track_generator import generatePolygon
import cv2
import numpy as np
import pdb
import random

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    # v1_u = unit_vector(v1)
    # v2_u = unit_vector(v2)
    
    # if np.all(v1_u == v2_u):
    #     return 0

    # return np.degrees(np.arccos(np.dot(v1_u, v2_u)))
    # # return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    dot = v1[0]*v2[0] + v1[1]*v2[1]      # dot product
    det = v1[0]*v2[1] - v1[1]*v2[0]      # determinant
    angle = np.arctan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return np.degrees(angle)

OBSERVATION_SPACE = 10
PENALTY = -300
    
class TrackEnv:

    MAX_TOTAL_REWARD = 360
    OBSERVATION_SPACE = 2
    ACTION_SPACE = 2

    def __init__(self, size=600, irregularity=0.8, spikeyness=0.25, numVerts=8, sensor_limit = 60):
        
        #Env definitions
        self.episode_step = 0

        # Map Definitions
        self.size = size
        self.radius = size / 4
        self.irregularity = irregularity
        self.spikeyness = spikeyness
        self.numVerts = numVerts
        self.center = (int(self.size/2), int(self.size/2))
        self.speed = 1
        self.total_progress = 0
        self.goal_point = 1
        self.last_dist = 0

        while True:
            # Map Image
            self.map, self.points = self.genMap(self.radius, self.irregularity, self.spikeyness, self.numVerts)
            self.start = self.points[0]
            self.render_img = cv2.cvtColor(self.map, cv2.COLOR_GRAY2BGR)
            # Agent
            self.X = self.start[0]
            self.Y = self.start[1]
            self.done = False
            if self.map[self.X, self.Y] == 255:
                break

        self.direction = (0,0)
        self.last_pos = (self.X, self.Y)
        self.sensor_limit = sensor_limit

        self.available_acitons = list(range(0,9))
        self.actions = {0 :( 0,-1),
                        1 :( 1,-1),
                        2 :( 1, 0),
                        3 :( 1, 1),
                        4 :( 0, 1),
                        5 :(-1, 1),
                        6 :(-1, 0),
                        7 :(-1,-1),
                        8 :( 0, 0)}

    def genMap(self, radius, irregularity, spikeyness, numVerts):
        points = generatePolygon(self.center[0], self.center[1], radius, irregularity, spikeyness, numVerts)
        points.append(points[0])
    
        img = np.zeros((self.size, self.size), dtype=np.uint8)
        for i in range(numVerts):
            cv2.line(img, points[i], points[i+1], 255, 50)
            
        return img, points

    def render(self):
        
        cv2.circle(self.render_img, (self.X ,self.Y), 4, (0,0,255), -1)
        sensor, points = self.getState()
        render_img_sensor = self.renderSensor(points, self.render_img)
        cv2.circle(render_img_sensor, self.points[self.goal_point-1], 3, (255, 255, 0), -1)
        cv2.circle(render_img_sensor, self.points[self.goal_point], 3, (0, 255, 0), -1)

        orientation = self.getOrientation()
        cv2.line(render_img_sensor, (self.X, self.Y), (self.X + orientation[0], self.Y - orientation[1]), (0,255,255), 2)


        cv2.imshow("track", render_img_sensor)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return False
        return True

    def move(self, dX=None, dY=None):
        if dX == None:
            dX += random.randint(-1,2)
            
        if dY == None:
            dY = random.randint(-1,2)

        dX *= self.speed
        dY *= self.speed

        self.last_pos = (self.X, self.Y)
        self.direction = (dX, dY)
        self.X += int(np.rint(dX))
        self.Y += int(np.rint(dY))

        return (self.X, self.Y), self.direction

    def getState(self):
        pos = np.array((self.X, self.Y))
        sensor = np.zeros([8], dtype=int)
        points = np.zeros([8,2],dtype=int)

        sensor_distribution = [np.array((0,-1)),
                               np.array((1,-1)),
                               np.array((1,0)),
                               np.array((1,1)),
                               np.array((0,1)),
                               np.array((-1,1)),
                               np.array((-1,0)),
                               np.array((-1,-1))]

        # for i in range(len(sensor_distribution)):
        #     sensor_distribution[i] = self.rotateVec(sensor_distribution[i])

        for i, s in enumerate(sensor_distribution):
            j = 0
            new_pos = pos.copy()
            while j < self.sensor_limit:
                new_pos = new_pos + s
                if self.map[int(new_pos[1]), int(new_pos[0])] == 0:
                    break
                
                points[i] = new_pos
                sensor[i] = j

                j += 1

        return sensor, points

    def getProgress(self, start=False):
        # v1 = self.toCartesian([self.size/2, 0])
        v1 = self.toCartesian(self.last_pos)
        if start:
            v1 = self.toCartesian(self.start)
            
        v2 = self.toCartesian([self.X, self.Y])
        degrees = angle_between(v2, v1)
        self.total_progress += degrees
        return self.total_progress, degrees

    def getOrientation(self):
        p1 = self.toCartesian([self.X, self.Y])
        p2 = self.toCartesian(self.points[self.goal_point])
        return [p2[0] - p1[0], p2[1] - p1[1]]

    def distance(self, p1, p2):
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    def toCartesian(self, p1):
        cartesianx = p1[0] - self.size / 2
        cartesiany = -p1[1] + self.size / 2
        return np.array((cartesianx, cartesiany), dtype=np.int)

    def renderSensor(self, sensor, img):
        new = img.copy()
        colors = [(255, 0, 0), (0, 255, 0)]
        for idx, s in enumerate(sensor):
            p1 = (self.X, self.Y)
            p2 = (s[0], s[1])
            if idx == 2:
                new = cv2.line(new, p1, p2, (0,0,255), 1 )
                new = cv2.circle(new, p2, 3, (0,0,255), -1 )
            else:
                new = cv2.line(new, p1, p2, colors[idx%2], 1 )
                new = cv2.circle(new, p2, 3, colors[idx%2], -1 )

        return new
    
    def checkGame(self):
        if self.map[self.Y, self.X] == 255:
            return False
        
        return True

    def reset(self, reset_map=True):
        while True:
            # Map Image
            if reset_map:
                self.map, self.points = self.genMap(self.radius, self.irregularity, self.spikeyness, self.numVerts)
    
            self.start = self.points[0]
            self.render_img = cv2.cvtColor(self.map, cv2.COLOR_GRAY2BGR)
            # Agent
            self.X = self.start[0]
            self.Y = self.start[1]

            if self.map[self.X, self.Y] == 255:
                break

        self.direction = (0,0)
        self.last_pos = (self.X, self.Y)
        self.done = False
        self.total_progress = 0
        self.goal_point = 1
        self.last_dist = 0
        
        observation, _ = self.getState()
        goal_dist = [self.X - self.points[self.goal_point][0], self.Y - self.points[self.goal_point][1]]
        # observation = np.hstack([np.array(goal_dist), observation])
        # observation = np.hstack([np.array(goal_dist), observation, np.array(self.direction)])
        observation = np.array(goal_dist)
        reward = 0

        return observation, reward, False

    def rotateVec(self, direction):
        b = angle_between((0, -1), self.direction)
        # direction = self.toCartesian(direction)
        x = np.cos(b)*direction[0] - np.sin(b)*direction[1]
        y = np.sin(b)*direction[0] + np.cos(b)*direction[1]
        return np.array([y, x])

    def step(self, action):
        if type(action) is int and action in self.available_acitons:
            self.episode_step += 1
            self.move(dX = self.actions[action][0], dY = self.actions[action][1])
        elif (type(action) is list or type(action) is np.ndarray) and len(action) == 2:
            self.episode_step += 1
            self.move(dX = action[0], dY = action[1])
        elif action is None:
            self.episode_step += 1
            self.move(dX = 0, dY = 0)
        else:
            print("Action {} not available".format(action))
            return None, None, None
        
        progress, degrees = self.getProgress()
        observation, _ = self.getState()
        min_sensor = np.min(observation)
        goal_dist = [self.X - self.points[self.goal_point][0], self.Y - self.points[self.goal_point][1]]
        # observation = np.hstack([np.array(goal_dist), observation, np.array(self.direction)])
        # observation = np.hstack([ observation,np.array(self.getOrientation())])
        observation = np.array(goal_dist)
        done = self.checkGame()

        dist = self.distance([self.X, self.Y], self.points[self.goal_point])

        if dist < self.last_dist:
            reward = 0
            for i in range(0, self.goal_point - 1):
                reward += self.distance(self.points[i], self.points[i+1])

            reward += self.distance(self.points[self.goal_point-1], self.points[self.goal_point]) - dist
            reward += (min_sensor * 5)
        else: 
            reward = -dist

        if dist <= 20:
            self.goal_point += 1
            self.goal_point = self.goal_point % len(self.points)

        if self.goal_point == 0:
            reward = 10000
            done = True
        elif done:
            reward = -300

        self.last_dist = dist

        # print("{} {} {} {}".format(self.goal_point, len(self.points), self.distance(self.points[self.goal_point], self.points[self.goal_point + 1]), self.distance([self.X, self.Y], self.points[self.goal_point])))

        return observation, reward, done
        

if __name__ == "__main__":
    t = TrackEnv(sensor_limit=30)
    for i in range(10):
        done = False
        print("Ep: {}".format(i))
        while t.render() and not done:
            action = int(input())
            observation, reward, done = t.step(action)
            print("Reward: {:.5f} | Done: {}".format(reward, done))
            
        t.reset()