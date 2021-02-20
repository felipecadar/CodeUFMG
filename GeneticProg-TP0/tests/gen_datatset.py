import numpy as np
  
test_size = 2000
train_size = 20
name = 'synth_dumb_1'

def func(x):
    return x[0] + x[1] - x[2]

x_train = np.random.randint(0,10,  (train_size, 3))
y_train = [func(x) for x in x_train]

dataset = open(name + '.csv', 'w')

for i in range(train_size):
    dataset.write(str(x_train[i,0]) + ',' + str(x_train[i,1]) + ',' + str(x_train[i,2]) + ',' + str(y_train[i]) + '\n')