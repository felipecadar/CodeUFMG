import socket
import random
from protocol import send, recv, Connect, getTime
import argparse
import threading
import matplotlib.pyplot as plt

import sys
sys.path.append("PyTorch-ActorCriticRL/") 

import numpy as np
import torch
from torch.autograd import Variable
import os
import psutil
import gc

import train
import buffer

from torch.utils.tensorboard import SummaryWriter


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--episodes",type=int, default=5000,    help="time delay to send messages in miliseconds")
    parser.add_argument("-s", "--steps"   ,type=int, default=10000,    help="time delay to send messages in miliseconds")
    parser.add_argument("-d", "--delay",   type=int, default=0,    help="time delay to send messages in miliseconds")
    parser.add_argument("-v", "--variance",type=int, default=0,    help="variance to time delay [-variance, +variance]")
    parser.add_argument("-p", "--port",    type=int, default=5555, help="Socket port")
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()

    variance = args.variance
    delay = args.delay
    port = args.port

    delay_hist = []

    conn = Connect()       
    simulation_code = -1
    threads = []

    MAX_EPISODES = args.episodes
    MAX_STEPS = args.steps
    MAX_BUFFER = 1000
    # MAX_BUFFER = 1000000
    MAX_TOTAL_REWARD = 10000
    S_DIM = 2
    A_DIM = 2
    A_MAX = 2

    log = open("log.txt", "w")

    print(' State Dimensions :- ', S_DIM)
    print(' Action Dimensions :- ', A_DIM)
    print(' Action Max :- ', A_MAX)

    writer = SummaryWriter(flush_secs=1)


    ram = buffer.MemoryBuffer(MAX_BUFFER)
    trainer = train.Trainer(S_DIM, A_DIM, A_MAX, ram)
    # trainer.load_models(1000)

    for _ep in range(MAX_EPISODES):
        rewards = []
        observation = [0] * S_DIM
        new_observation = [0] * S_DIM
        try:
            send(conn, [True, True], 0, 0)
            while True:
                ans, send_time = recv(conn)
                if type(ans) == type(True) and ans:
                    break
                    #start

            while True:
                ans, send_time = recv(conn)
                if ans != None:
                    break

            print("Start episode {}".format(_ep))
            observation, reward, done, simulation_code = ans

            for r in range(MAX_STEPS):
            
                state = np.float32(observation)
                # action = trainer.get_exploration_action(state)
                if _ep%5 == 0:
                    # validate every 5th episode
                    action = trainer.get_exploitation_action(state)
                else:
                    # get action based on observation, use exploration policy here
                    action = trainer.get_exploration_action(state)

                # print(action)

                t = send(conn, [action, _ep], delay, variance)
            
                ans, send_time = recv(conn)
                if ans is None:
                    continue

                new_observation, reward, done, simulation_code = ans

                if simulation_code == 1:
                    # EVERYTHING IS FINE
                    pass
                elif simulation_code == 2:
                    # NOT FINE NOT FINE YOU DIED
                    break


                recv_time = int(getTime())
                print("Reward: {:3.5f} | Epoch: {:3d} | Delay: {:4d} | Threads: {} | Done: {} |".format(reward, _ep, (recv_time - send_time), threading.active_count(), done))
                delay_hist.append(recv_time - send_time)

                rewards.append(reward)

                if done:
                    new_state = None
                else:
                    new_state = np.float32(new_observation)
                    # push this exp in ram
                    ram.add(state, action, reward, new_state)
                
                observation = new_observation

                # perform optimization
                trainer.optimize()
                if done:
                    break
                

                threads.append(t)

            if _ep%500 == 0:
                trainer.save_models(_ep)
            
            log.write("Ep: {} | Mean Reward: {}\n".format(_ep, np.mean(rewards)))
            writer.add_scalar("Mean Reward", np.mean(rewards), _ep)

        except socket.error as e:
            print("SOCKET ERROR\n", e)
            break
        except Exception as e:
            raise
            break

    send(conn, False, 0, 0)
    conn.close()


    plt.hist(delay_hist)
    plt.show()
