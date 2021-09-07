import pygame
from pygame.locals import *


# Data
index = 0  # Currently displayed image index

file = open('train-images.idx3-ubyte', mode='br')
file.read(4)  # Skip magic number
IMAGES_AMOUNT = int.from_bytes(file.read(4), byteorder='big')

IMG_HEIGHT = int.from_bytes(file.read(4), byteorder='big')
IMG_WIDTH = int.from_bytes(file.read(4), byteorder='big')

# Cached images
cache = []

# Display
# The zoom factor to display the images
zoom = 8
WIN_SIZE = 400
FONT_SIZE = 16
pygame.init()
win = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption('MNIST reader')

font = pygame.font.SysFont('Consolas', FONT_SIZE)


def disp(n):
    win.fill((0, 0, 0))
    global cache
    # Loads a new image if this index has not been reached yet
    if (n >= len(cache)):
        l = []
        for i in range(IMG_WIDTH):
            l.append([])
            for j in range(IMG_HEIGHT):
                b = file.read(1)
                l[i].append(int.from_bytes(b, byteorder='big'))
        cache.append(l)

    bytes = cache[n]
    # Displays the image
    for i in range(len(bytes)):
        for j in range(len(bytes[i])):
            v = bytes[i][j]
            pygame.draw.rect(win, (v, v, v), pygame.Rect(
                j*zoom, i * zoom + 16, zoom, zoom))
    count_text = font.render(
        f'IMG {n + 1}/{IMAGES_AMOUNT}', True, (255, 255, 255))
    size_text = font.render(
        f'Base size:{IMG_WIDTH}x{IMG_HEIGHT} | Scaled to: {IMG_WIDTH * zoom}x{IMG_HEIGHT * zoom} (x{zoom})', True, (255, 255, 255))
    win.blit(count_text, dest=(0, 0))
    win.blit(size_text, dest=(0, IMG_HEIGHT * zoom + FONT_SIZE))
    pygame.display.flip()


disp(0)
lock = True
while lock:
    events = pygame.event.get()
    for e in events:
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                index += 1
                disp(index)
            if e.key == K_LEFT:
                index = max(index - 1, 0)
                disp(index)
            if e.key == K_UP:
                zoom += 1
                disp(index)
            if e.key == K_DOWN:
                zoom = max(zoom - 1, 1)
                disp(index)
        if e.type == QUIT:
            lock = False


pygame.quit()
