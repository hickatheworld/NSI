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

datasets = ['train_images', 'test_images', 'train_labels', 'test_labels']


def load(dataset, amount):
    if (dataset not in datasets):
        print('Incorrect dataset. Can be: ', ', '.join(datasets))
        return
    l1 = []
    for k in range(amount):
        if ('images' in dataset):
            l2 = []
            for i in range(IMG_WIDTH * IMG_HEIGHT):
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
    S = 0
    for i in range(IMG_WIDTH * IMG_HEIGHT):
        S += abs(img1[i] - img2[i])
    return S

def guess(i):
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
    to_guess = data['test_images'][i]
    answer = data['test_labels'][i]
    nn = [[-1, 200000] for i in range(k)]
    for j in range(len(data['train_images'])):
        img = data['train_images'][j]
        dist = distance(to_guess, img)
        if (dist < nn[-1][1]):
            nn[-1] = [j, dist]
            nn.sort(key= lambda l: l[1])
    labels = []
    nn_indexes=[]
    for i in range(k):
        labels.append(data['train_labels'][nn[i][0]])
        nn_indexes.append(nn[i][0])
    guess = most_frequent(labels)
    return (guess, nn_indexes)

def most_frequent(lst):
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
win = pygame.display.set_mode((800, 600))
big_font = pygame.font.SysFont('Consolas', 50)
small_font = pygame.font.SysFont('Consolas', 14)

def display_guess(i):
    global guesses
    win.fill((0,0,0))
    img = data['test_images'][i]
    disp(img, 4, (0,0))
    if (len(guesses) == i):
        txt = small_font.render('Guessing...', True, (255, 255, 255))
        win.blit(txt, dest=(0, IMG_HEIGHT * 4 + 10))
        pygame.display.flip()
        g = k_guess(i, K_FACTOR)
        guesses.append(g)
    num = data['test_labels'][i]
    guess = guesses[i]
    pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0,IMG_HEIGHT * 4 + 10, 800, 14))
    txt = small_font.render('Guessed: ' + str(guess[0]) + ' | Actual number: ' + str(num), True, (255, 255, 255))
    win.blit(txt, dest=(0, IMG_HEIGHT * 4 + 10))
    for i in range(K_FACTOR):
        txt = small_font.render(str(K_FACTOR) + ' nearest neighboors:', True, (255, 255, 255))
        win.blit(txt, dest=(0, IMG_HEIGHT * 4 + 30))
        disp(data['train_images'][guess[1][i]], 1, (i*IMG_WIDTH, IMG_HEIGHT * 4 + 50))
    pygame.display.flip()

def disp(img, zoom, dest):
    x = 0
    y = 0
    for v in img:
        v = 255 - v
        pygame.draw.rect(win, (v, v, v), pygame.Rect(14 * zoom + dest[0] + x * zoom, dest[1] + y * zoom, zoom, zoom))
        x += 1
        if x == IMG_HEIGHT:
            x = 0
            y += 1


loading_text = big_font.render('Loading images...', True, (255, 255, 255))
win.blit(loading_text, dest=(0, 0))
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
                index+=1
                display_guess(index)
            if e.key == K_LEFT and index > 0:
                index-=1
                display_guess(index)
pygame.quit()
