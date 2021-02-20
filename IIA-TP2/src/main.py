import numpy as np
import argparse
import os, uuid

from tools import *
from qlearn import *

from tqdm import tqdm
import pickle


def parseArgs():
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument("-i", "--input", type=str,
                        default="maps/input1.txt", help="Mapa de entrada")

    parser.add_argument("-id", "--id", type=str,
                        default="", help="ID da execução")

    parser.add_argument("-n", "--epochs", type=int,
                        default=10000, help="Epocas de treinamento")

    parser.add_argument("-e", "--exploration", type=float,
                        default=0.5, help="Exploration Factor")
    parser.add_argument("-lr", "--learning-rate", type=float,
                        default=0.1, help="Learning rate")
    parser.add_argument("-y", "--discount-factor", type=float,
                        default=0.7, help="Discount Factor")

    parser.add_argument("-t", "--tqdm-position", type=int,
                        default=1, help="For parallel execution of experiments")

    parser.add_argument("-s", "--silent", action="store_true",
                        default=False, help="For parallel execution of experiments")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()

    input_map_path = args.input
    if not os.path.isfile(input_map_path):
        fail("Fail to open %s" % input_map_path)
        exit()

    char_map, W = loadMap(input_map_path)

    exp_id = args.id
    if exp_id == "":
        exp_id = str(uuid.uuid4())

    logdir = os.path.join("logs", exp_id)
    mkdir_p(logdir)

    exploration = args.exploration
    env = Env(char_map, W, max_steps=100)
    agent = QAgent(env.actions, char_map, W, args.learning_rate, args.discount_factor )

    test_hist = []
    for epoch in tqdm(range(args.epochs), position=args.tqdm_position, leave=False):

        env.reset()
        cumulative_reward = 0

        # Train
        while not env.done:
            if np.random.random_sample() < exploration:
                action = env.sample_action()
            else:
                action = agent.act(env.state)

            old_state = env.state
            new_state, reward, done, info = env.step(action)
            agent.update(old_state, action, reward, new_state)

            cumulative_reward += reward

        # Exploration atualization
        if args.epochs > 200:
            if epoch % int(args.epochs / 200) == 0:
                exploration *= 0.999

        # Test
        if epoch % 100 == 0:
            local_hist = []
            for i in range(10):
                test_cumulative_reward = 0

                env.reset()
                while not env.done:
                    action = agent.act(env.state)
                    _, reward, _, _ = env.step(action)
                    test_cumulative_reward += reward

                local_hist.append(test_cumulative_reward)

            test_hist.append(np.mean(local_hist))

            if not args.silent:
                tqdm.write("Epoch %i of %i - Expl: %f - Last 100 Cumulative Reward Mean: %f" % (epoch, args.epochs, exploration,  np.mean(test_hist[max(-100, -len(test_hist)):])))            


    agent.save(os.path.join(logdir, "qtable.pkl"))
    pickle.dump({"args": args, "metrics":test_hist}, open(os.path.join(logdir, "log.pkl"), 'wb'))
    with open("pi.txt", "w") as outfile:
        for i in range(agent.qtable.shape[0]):
            for j in range(agent.qtable.shape[1]):
                for s in range(agent.qtable.shape[2]):
                    action = agent.act((i, j, s))
                    action_name = env.actions_names[action]
                    action_value = agent.qtable[i,j,s,action]
                    outfile.write("({},{},{}), {}, {:.2f} \n".format(i,j,s,action_name, action_value))

