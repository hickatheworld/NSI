import time

pygame.display.init()
IMG_WIDTH = 28
IMG_HEIGHT = 28

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
    print('Guessing image n°' + str(i))
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
    for i in range(k):
        labels.append(data['train_labels'][nn[i][0]])
    guess = most_frequent(labels)
    print('Guess:', guess, 'Actual number:', answer)
    return guess == answer

def most_frequent(lst):
    counter = 0
    num = lst[0]
    for i in lst:
        current = lst.count(i)
        if(current > counter):
            counter = current
            num = i
    return num


start = time.time()
print('Loading data...')
load('train_images', 6000)
load('train_labels', 6000)
load('test_images', 1000)
load('test_labels', 1000)
print('Loaded, took ' + str(time.time() - start) + 's')
