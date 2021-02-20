
import torch.nn as nn
import torch.nn.functional as F
import torch

from collections import OrderedDict
DEBUG = False


def weights_init_normal(m):
    classname = m.__class__.__name__
    if classname.find("Conv") != -1:
        torch.nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find("BatchNorm2d") != -1:
        torch.nn.init.normal_(m.weight.data, 1.0, 0.02)
        torch.nn.init.constant_(m.bias.data, 0.0)

class DebugLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        print("[DEGUB]: X.shape={}".format(list(x.shape)))
        return x


class Flatten(nn.Module):
    def forward(self, x):
        x = x.view(x.size()[0], -1)
        return x

def ConvBlock(input_channels, output_channels, kernel, stride, relu=True, norm=True, debug=True):
    block = [nn.Conv2d(input_channels, output_channels, kernel, stride=stride)]
    if relu:
        block.append(nn.ReLU())
    if norm:
        block.append(nn.BatchNorm2d(output_channels))
    if debug:
        block.append(DebugLayer())

    return block

def UConvBlock(input_channels, output_channels, kernel, stride, relu=True, norm=True, debug=True):
    block = [nn.ConvTranspose2d(input_channels, output_channels, kernel, stride=stride)]
    if relu:
        block.append(nn.ReLU())
    if norm:
        block.append(nn.BatchNorm2d(output_channels))
    if debug:
        block.append(DebugLayer())

    return block

class GeneratorUNet(nn.Module):
    def __init__(self, input_channels=3, output_channels=3):
        super(GeneratorUNet, self).__init__()

        model_list = []

        model_list.extend(UConvBlock(input_channels, 64, 6, 2, debug=DEBUG))
        model_list.extend(ConvBlock(64, 64, 5, 1, debug=DEBUG))
        model_list.extend(UConvBlock(64, 64, 6, 2, debug=DEBUG))
        model_list.extend(ConvBlock(64, 64, 5, 1, debug=DEBUG))
        model_list.extend(ConvBlock(64, 128, 5, 1, debug=DEBUG))
        model_list.extend(ConvBlock(128, 256, 5, 1, debug=DEBUG))
        model_list.extend(ConvBlock(256, 256, 1, 1, debug=DEBUG))
        model_list.extend(ConvBlock(256, 128, 5, 1, debug=DEBUG))
        model_list.extend(ConvBlock(128, 64, 5, 2, debug=DEBUG))
        model_list.extend(ConvBlock(64, 32, 5, 1, debug=DEBUG))
        model_list.extend(ConvBlock(32, 32, 7, 1, debug=DEBUG))
        model_list.extend(ConvBlock(32, 32, 7, 1, debug=DEBUG))
        model_list.append(nn.Conv2d(32, output_channels, 5, stride=1))
        model_list.append(nn.Tanh())
        
        self.model = nn.Sequential(*model_list)
    
    def forward(self, x):
        return self.model(x)


class Discriminator(nn.Module):
    def __init__(self, img_shape):
        super(Discriminator, self).__init__()

        img_size = img_shape[3]
        in_channels = img_shape[1]

        def discriminator_block(in_filters, out_filters, bn=True):
            block = [nn.Conv2d(in_filters, out_filters, 3, 2, 1), nn.LeakyReLU(0.2, inplace=True), nn.Dropout2d(0.25)]
            if bn:
                block.append(nn.BatchNorm2d(out_filters, 0.8))
            return block

        self.model = nn.Sequential(
            *discriminator_block(in_channels, 16, bn=False),
            *discriminator_block(16, 32),
            *discriminator_block(32, 64),
            *discriminator_block(64, 128),
        )

        # The height and width of downsampled image
        ds_size = img_size // 2 ** 4
        ds_size = 2
        self.adv_layer = nn.Sequential(nn.Linear(128 * ds_size ** 2, 1), nn.Sigmoid())

    def forward(self, img):
        out = self.model(img)
        # print(out.shape)
        out = out.view(out.shape[0], -1)
        # print(out.shape)
        validity = self.adv_layer(out)

        return validity


if __name__ == "__main__":

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using {}".format(device))

    x = torch.rand([2, 1, 28, 28]).to(device)
    g = GeneratorUNet(input_channels=1, output_channels=1).to(device)
    d = Discriminator(x.shape).to(device)
    
    print("Initial X", list(x.shape))
    out = g(x)
    print("Generator Out", list(out.shape))
    out = d(x)
    print("Discriminator Out", list(out.shape))
