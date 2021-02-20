import socket
import random
from protocol import send, recv, Connect, getTime
import argparse
import threading

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
    parser.add_argument("-e", "--episodes",type=int, default=500,    help="Number of episodes")
    parser.add_argument("-s", "--steps"   ,type=int, default=10000,    help="Number of steps p/ episode")
    parser.add_argument("-p", "--port",    type=int, default=5555, help="Socket port")
    parser.add_argument("-m", "--model",   default="ok", help="Model prefix")
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()

    port = args.port

    delay_test = [0, 100, 300]
    # delay_test = [0, 10, 100, 200, 300, 400, 500, 600]
    variance = 0
    
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
    trainer.load_models(args.model)
    controll_ep = 0
    for _ep in range(MAX_EPISODES):
        reset_map = True
        reward_data = {}
        for ep_delay in delay_test:
            rewards = []
            delays = []

            try:
                send(conn, [True, reset_map], 0, 0)
                reset_map = False
                while True:
                    ans, send_time = recv(conn)
                    if type(ans) == type(True) and ans:
                        break
                        #start

                print("Start episode {}".format(_ep))
                while True:
                    ans, send_time = recv(conn)
                    if ans != None:
                        break

                observation, reward, done, simulation_code = ans

                for r in range(MAX_STEPS):
                
                    state = np.float32(observation)
                    action = trainer.get_exploration_action(state)

                    t = send(conn, [action, controll_ep], ep_delay, variance)
                
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

                    delays.append(recv_time - send_time)
                    rewards.append(reward)

                    if done:
                        new_state = None
                    else:
                        new_state = np.float32(new_observation)
                        # push this exp in ram
                        ram.add(state, action, reward, new_state)

                    observation = new_observation

                    if done:
                        break

                    threads.append(t)
                
                controll_ep += 1
                reward_data[str(ep_delay)] = np.mean(rewards)


            except socket.error as e:
                print("SOCKET ERROR\n", e)
                break
            except Exception as e:
                raise
                break

        writer.add_scalars("Mean_Reward", reward_data, _ep)

    send(conn, False, 0, 0)
    conn.close()
