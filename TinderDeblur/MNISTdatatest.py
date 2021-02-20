import torch
import torch.nn as nn
from torch.nn import functional as F
import torchvision

import matplotlib.pyplot as plt
import numpy as np
from blur import GaussianSmoothing

from utils import *

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


batch_size_train = 16
transform = torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Normalize((0.1307,), (0.3081,))
                               ])

train_set =  torchvision.datasets.MNIST('./data/', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_set ,batch_size=batch_size_train, shuffle=True)

data_iter = iter(train_loader)
images, labels = data_iter.next()

# gauss4 = GaussianSmoothing(1, 5, 4)

# pad_images = F.pad(images, (2, 2, 2, 2), mode='reflect')

# blur_images4 = gauss4(pad_images)

# both = torch.cat((images, blur_images4))
# imshow(torchvision.utils.make_grid(both))

in_channels = images.shape[1]
uconv = nn.ConvTranspose2d(in_channels, 64, 6, stride=2)

out = uconv(images)
print(out.shape)
