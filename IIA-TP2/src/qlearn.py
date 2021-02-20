from tools import *
import numpy as np
import pickle

class Env():
    def __init__(self, char_map, W, max_steps = 100):
        self.char_map = char_map

        self.actions = [0, 1, 2, 3]
        self.actions_names = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.actions_movements = [(-1, 0), (+1, 0), (0, -1), (0, 1)]
        self.W = W
        self.steps_since_W = 0
        self.done = None
        self.position = None
        self.reward = None
        self.steps = 0
        self.state = None
        self.max_steps = max_steps

    def reset(self, rand=True, initial=(0, 0)):
        self.done = False
        self.position = initial
        self.reward = None
        self.steps_since_W = 0
        self.steps = 0
        if rand:
            valid = self.validPositions()
            rand_int = np.random.randint(0, len(valid[0]))
            self.position = (valid[0][rand_int], valid[1][rand_int])
        self.state = (self.position[0], self.position[1], self.steps_since_W)

    def validPositions(self):
        return np.where((self.char_map == ord('.')) | (self.char_map == ord('#')))

    def sample_action(self):
        return np.random.randint(0, len(self.actions))

    def step(self, action):
        info = ""
        if self.done:
            print("Match already ended...")
            exit()

        if not (action in self.actions):
            print("Invalid action:", action)
            exit()

        self.position = (self.position[0] + self.actions_movements[action]
                      [0], self.position[1] + self.actions_movements[action][1])
        self.steps += 1

        if self.position[0] < self.char_map.shape[0] and self.position[1] < self.char_map.shape[1] and self.position[0] > 0 and self.position[1] > 0:
            # Go to empty position
            if self.char_map[self.position] == ord("."):
                self.reward = -1
                self.steps_since_W += 1
                info = "empty"

            # Go to location position
            if self.char_map[self.position] == ord("#"):
                self.reward = 1 #self.steps_since_W - 1
                self.steps_since_W = 0
                info = "location"

            # Go to final destination
            if self.char_map[self.position] == ord("$"):
                self.reward = 10
                self.done = True
                self.steps_since_W += 1
                info = "final dest"

            # Go to wall
            if self.char_map[self.position] == ord("*"):
                self.reward = -15
                self.done = True
                info = "wall"

            # Location points limit
            if self.steps_since_W >= self.W:
                self.reward = -10
                self.done = True
                info = "location limit"

        # Out of the map / wall
        else:
            self.reward = -10
            self.done = True
            info = "out of map"

        if self.steps > self.max_steps:
            # self.reward = -10
            self.done = True
            info = "max steps"

        self.state = (self.position[0], self.position[1], self.steps_since_W)

        return self.state, self.reward, self.done, info


class QAgent():
    def __init__(self, actions, char_map, W, learning_rate, discount_factor):
        self.actions = actions
        self.n_actions = len(actions)

        self.char_map = char_map
        self.n_states = char_map.shape

        self.alpha = learning_rate
        self.y = discount_factor

        self.qtable = np.zeros([self.n_states[0], self.n_states[1], W+1, self.n_actions])

    def act(self, state):
        try:
            return np.argmax(self.qtable[state])
        except:
            # Out of map states...
            return -10

    def update(self, state, action, reward, new_state):

        old_value = self.qtable[state][action]
        next_max = self.act(new_state)

        self.qtable[state][action] = old_value + self.alpha * (reward + self.y * next_max - old_value)

    def load(self, fname):
        self.qtable = pickle.load(open(fname, "rb"))

    def save(self, fname):
        pickle.dump(self.qtable, open(fname, "wb"))

if __name__ == "__main__":
    char_map, W = loadMap("maps/input3.txt")
    env = Env(char_map, W)

    env.reset()
    while not env.done:
        action = env.sample_action()
        state, reward, done, info = env.step(action)
        print(state, reward, done, info)
