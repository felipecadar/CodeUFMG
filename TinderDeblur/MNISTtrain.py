import argparse
import os
# Ignore warnings
import warnings

import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
from torch.autograd import Variable
from torch.nn import functional as F
from torchvision.utils import save_image
from torch.utils.tensorboard import SummaryWriter

from blur import GaussianSmoothing
from models import *
from utils import *

from tqdm import tqdm

warnings.filterwarnings("ignore")

os.makedirs("images", exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--n_epochs", type=int, default=200, help="number of epochs of training")
parser.add_argument("--batch_size", type=int, default=64, help="size of the batches")
parser.add_argument("--lr", type=float, default=0.0002, help="adam: learning rate")
parser.add_argument("--b1", type=float, default=0.5, help="adam: decay of first order momentum of gradient")
parser.add_argument("--b2", type=float, default=0.999, help="adam: decay of first order momentum of gradient")
parser.add_argument("--n_cpu", type=int, default=8, help="number of cpu threads to use during batch generation")
parser.add_argument("--latent_dim", type=int, default=100, help="dimensionality of the latent space")
parser.add_argument("--img_size", type=int, default=32, help="size of each image dimension")
parser.add_argument("--channels", type=int, default=1, help="number of image channels")
parser.add_argument("--sample_interval", type=int, default=400, help="interval between image sampling")
opt = parser.parse_args()
print(opt)

cuda = True if torch.cuda.is_available() else False
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using {}".format(device))

batch_size_train = 18

transform = torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Normalize((0.1307,), (0.3081,))
                               ])

train_set =  torchvision.datasets.MNIST('./data/', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_set ,batch_size=batch_size_train, shuffle=True)


#Display Example Images
data_iter = iter(train_loader)
images, labels = data_iter.next()
gauss = GaussianSmoothing(1, 5, 4)
pad_images = F.pad(images, (2, 2, 2, 2), mode='reflect')
blur_images4 = gauss(pad_images)
# both = torch.cat((images, blur_images4))
# imshow(torchvision.utils.make_grid(both))

adversarial_loss = torch.nn.BCELoss()

# Initialize generator and discriminator
generator = GeneratorUNet(input_channels=1, output_channels=1)
discriminator = Discriminator(images.shape)


generator.to(device)
discriminator.to(device)
adversarial_loss.to(device)
gauss.to(device)

# Initialize weights
generator.apply(weights_init_normal)
discriminator.apply(weights_init_normal)

#Tensorboard

tb = SummaryWriter()

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

# ----------
#  Training
# ----------

for epoch in range(opt.n_epochs):
    d_losses = np.zeros(len(train_loader))
    g_losses = np.zeros(len(train_loader))
    for i, (imgs, _) in tqdm(enumerate(train_loader), total=len(train_loader)):

        # Adversarial ground truths
        valid = Variable(Tensor(imgs.shape[0], 1).fill_(1.0), requires_grad=False)
        fake = Variable(Tensor(imgs.shape[0], 1).fill_(0.0), requires_grad=False)

        # Configure input
        real_imgs = Variable(imgs.type(Tensor))

        # -----------------
        #  Train Generator
        # -----------------

        optimizer_G.zero_grad()

        # Sample noise as generator input
        blur_images = gauss(F.pad(real_imgs, (2, 2, 2, 2), mode='reflect'))
        z = blur_images

        # Generate a batch of images
        gen_imgs = generator(z)

        # Loss measures generator's ability to fool the discriminator
        g_loss = adversarial_loss(discriminator(gen_imgs), valid)

        g_loss.backward()
        optimizer_G.step()

        g_losses[i] = g_loss
        # ---------------------
        #  Train Discriminator
        # ---------------------

        optimizer_D.zero_grad()

        # Measure discriminator's ability to classify real from generated samples
        real_loss = adversarial_loss(discriminator(real_imgs), valid)
        fake_loss = adversarial_loss(discriminator(gen_imgs.detach()), fake)
        d_loss = (real_loss + fake_loss) / 2

        d_loss.backward()
        optimizer_D.step()

        d_losses[i] = d_loss

        if i % 100 == 0:
            tqdm.write(
                "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
                % (epoch, opt.n_epochs, i, len(train_loader), d_loss.item(), g_loss.item())
            )

        batches_done = epoch * len(train_loader) + i
        if batches_done % opt.sample_interval == 0:
            save_image(gen_imgs.data[:25], "images/%d.png" % batches_done, nrow=5, normalize=True)

        tb.add_scalar("Discriminator Loss", d_loss, (epoch * len(train_loader)) + i)
        tb.add_scalar("Generator Loss", g_loss, (epoch * len(train_loader)) + i)



tb.close()
