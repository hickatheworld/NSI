import pygame
from pygame.locals import *

IMG_WIDTH = 28
IMG_HEIGHT = 28

data = {
    'train_images': [],
    'test_images': [],
    'train_labels': [],
    'test_labels': [],
}
files = {
    'train_images': open('train-images.idx3-ubyte', mode='br'),
    'test_images': open('t10k-images.idx3-ubyte', mode='br'),
    'train_labels': open('train-labels.idx1-ubyte', mode='br'),
    'test_labels': open('t10k-labels.idx1-ubyte', mode='br'),
}

# Skip metadata
files['train_images'].read(16)
files['test_images'].read(16)
files['train_labels'].read(8)
files['train_images'].read(8)

datasets = ['train_images', 'test_images', 'train_labels', 'test_labels']


def load(dataset, amount):
    if (dataset not in datasets):
        print('Incorrect dataset. Can be: ', ', '.join(datasets))
        return
    for k in range(amount):
        l = []
        for i in range(IMG_WIDTH * IMG_HEIGHT):
            b = files[dataset].read(1)
            n = int.from_bytes(b, byteorder='big')
            l.append(n)


