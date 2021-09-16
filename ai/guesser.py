"""
     -- Script to read and analyze data from Yann Lecun's MNIST data. --
    Template strings are not being used because the damn school PCs are so 
           neglected that we don't even have an up-to-date Python.
"""

import pygame
from pygame.locals import *
import time

### Data side
IMG_WIDTH = 28
IMG_HEIGHT = 28
K_FACTOR = 10

data = {
    'train_images': [],
    'test_images': [],
    'train_labels': [],
    'test_labels': []
}
files = {
    'train_images': open('train-images.idx3-ubyte', mode='br'),
    'test_images': open('t10k-images.idx3-ubyte', mode='br'),
    'train_labels': open('train-labels.idx1-ubyte', mode='br'),
    'test_labels': open('t10k-labels.idx1-ubyte', mode='br')
}

# Skip metadata
files['train_images'].read(16)
files['test_images'].read(16)
files['train_labels'].read(8)
files['test_labels'].read(8)

DATASETS = ['train_images', 'test_images', 'train_labels', 'test_labels']

def load(dataset, amount):
    """
    Loads data from one of the four available datasets (test/train images/labels)
    `amount` represents the amount of images/labels to load.
    """
    if (dataset not in DATASETS):
        print('Incorrect dataset. Can be: ', ', '.join(DATASETS))
        return
    l1 = []
    for i in range(amount):
        if ('images' in dataset):
            l2 = []
            for j in range(IMG_WIDTH * IMG_HEIGHT):
                b = files[dataset].read(1)
                n = int.from_bytes(b, byteorder='big')
                l2.append(n)
            l1.append(l2)
        else:
            b = files[dataset].read(1)
            n = int.from_bytes(b, byteorder='big')
            l1.append(n)
    data[dataset].extend(l1)

def distance(img1, img2):
    """
    Calculates the distance between two images.
    """
    S = 0
    for i in range(IMG_WIDTH * IMG_HEIGHT):
        S += abs(img1[i] - img2[i])
    return S

def guess(i):
    """
    Guesses the label of a test image using Nearest Neighboor algorithm. 
    Returns whether the guess is correct.
    """
    print('Guessing image n°' + str(i))
    to_guess = data['test_images'][i]
    answer = data['test_labels'][i]
    best_dist = None
    closest = 0
    for j in range(len(data['train_images'])):
        img = data['train_images'][j]
        dist = distance(to_guess, img)
        if (best_dist == None or dist < best_dist):
            closest = j
            best_dist = dist
    guess = data['train_labels'][closest]
    print('Guess:', guess, 'Actual number:', answer, 'Distance:', best_dist)
    return guess == answer

def k_guess(i, k):
    """
    Guesses the label of a test image using K Nearest Neighboors algorithm. 
    """
    to_guess = data['test_images'][i]
    # nn is the list of the k nearest neighboors of our image (`to_guess`)
    # every two element sublist is of the form [index of the neighboor in the train set, distance between our image and this neighboor]
    nn = [[-1, 200000] for _ in range(k)]
    for j in range(len(data['train_images'])):
        img = data['train_images'][j]
        dist = distance(to_guess, img)
        # nn is sorted by the distances of every sublist.
        # Therefore, if dist is smaller than the greatest distance stored in nn, it can replace it.
        if (dist < nn[-1][1]):
            nn[-1] = [j, dist]
            nn.sort(key=lambda l: l[1])
    labels = [] # The labels of the nearest neighboors
    nn_indexes = [] # The indexes of the nearest neighboors
    for i in range(k):
        labels.append(data['train_labels'][nn[i][0]])
        nn_indexes.append(nn[i][0])
    guess = most_frequent(labels)
    return (guess, nn_indexes)

def most_frequent(lst):
    """
    Returns the most frequent value from a list.
    """
    counter = 0
    num = lst[0]
    for i in lst:
        current = lst.count(i)
        if(current > counter):
            counter = current
            num = i
    return num


### Graphics side
pygame.init()
WIN_WIDTH = 600
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('MNIST')


def display_guess(i):
    WIN.fill((0, 0, 0))
    img = data['test_images'][i]
    # -> Displaying Test image
    disp_img(img, 8, (WIN_WIDTH / 2 - 8 * IMG_WIDTH, 60))
    # -> Displaying Title
    text('Image #' + str(i), WIN_WIDTH / 2, 10, 30, 'center')
    # if len(guesses) == i, the user is trying to access an image that has not been guessed yet.
    if (len(guesses) == i):
        # 8 <=> Zoom factor ; 60 <=> Title text ; 10 <=> Margin with image
        text('Guessing...', WIN_WIDTH / 2, IMG_HEIGHT * 8 + 60 + 10, x_origin='center')
        pygame.display.flip()
        g = k_guess(i, K_FACTOR)
        guesses.append(g)
    guess = guesses[i]
    # -> Displaying Neighboors images + labels
    for j in range(K_FACTOR):
        # The width of all the neighboor images side by side.
        full_width = K_FACTOR * 28
        disp_img(data['train_images'][guess[1][j]], 1, (WIN_WIDTH / 2 - full_width / 2 + j * IMG_WIDTH - IMG_WIDTH / 2, IMG_HEIGHT * 8 + 60 + 50))  # 50 <=> Info texts
        text(str(data['train_labels'][guess[1][j]]), WIN_WIDTH / 2 - full_width / 2 + j * IMG_WIDTH - IMG_WIDTH / 2 + IMG_WIDTH, IMG_HEIGHT * 8 + 60 + 50 + IMG_HEIGHT + 5, x_origin='center')  # 5 <=> Margin with neighboor images

    # -> Displaying Info texts
    guessed_num = guess[0]
    expected_num = data['test_labels'][i]
    text('Guessed: ' + str(guessed_num) + ' | Expected: ' + str(expected_num), WIN_WIDTH / 2, IMG_HEIGHT * 8 + 60 + 10, x_origin='center')  # 10 <=> Margin with image
    text(str(K_FACTOR) + ' nearest neighboors:', WIN_WIDTH / 2, IMG_HEIGHT * 8 + 60 + 30, x_origin='center')  # 30 <=> Margin with above text
    pygame.display.flip()


def disp_img(img, zoom, dest):
    x = 0
    y = 0
    for v in img:
        v = 255 - v
        rect(14 * zoom + dest[0] + x * zoom, dest[1] + y * zoom, zoom, zoom, (v, v, v))
        x += 1
        if x == IMG_HEIGHT:
            x = 0
            y += 1


def rect(x, y, w, h, c):
    pygame.draw.rect(WIN, c, pygame.Rect(x, y, w, h))


def text(content, x, y, size=14, x_origin='corner', y_origin='corner'):
    """
    Displays a text on screen.
    """
    font = pygame.font.SysFont('Consolas', size)
    txt = font.render(content, True, (255, 255, 255))
    w = txt.get_width()
    h = txt.get_height()
    dest = [x, y]
    if (x_origin == 'center'):
        dest[0] -= w/2
    if (y_origin == 'center'):
        dest[1] -= h/2
    # Clear area behind text to avoid overlapping.
    pygame.draw.rect(WIN, (0, 0, 0), pygame.Rect(dest[0], dest[1], w, h))
    WIN.blit(txt, dest=tuple(dest))


text('Loading data...', WIN_WIDTH/2, WIN_HEIGHT/2, 60, 'center', 'center')
pygame.display.flip()

start = time.time()
print('Loading data...')
load('train_images', 6000)
load('train_labels', 6000)
load('test_images', 1000)
load('test_labels', 1000)
print('Loaded, took ' + str(time.time() - start) + 's')

guesses = []
index = 0
lock = True
display_guess(0)
while lock:
    for e in pygame.event.get():
        if e.type == QUIT:
            lock = False
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                index += 1
                display_guess(index)
            if e.key == K_LEFT and index > 0:
                index -= 1
                display_guess(index)
pygame.quit()
