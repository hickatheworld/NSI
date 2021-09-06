import pygame
import time
from random import randint
from pygame.locals import *

pygame.display.init()

WIN_SIZE=600

win = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))

lock=True
isPressed=False
square_size=50
background = (0, 0, 0)
foreground = (255, 255, 255)

def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

while lock:
    events = pygame.event.get()
    for e in events:
        if e.type == QUIT:
            lock=False
        if e.type == KEYDOWN and e.key == pygame.K_SPACE:
            isPressed=True
        if e.type == KEYUP and e.key == pygame.K_SPACE:
            isPressed=False
        if e.type == KEYDOWN and e.key == pygame.K_RIGHT:
            square_size+=10
        if e.type == KEYDOWN and e.key == pygame.K_LEFT:
            if (square_size > 10):
                square_size-=10
        if e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
            square_size = 50
        if e.type == KEYDOWN and e.key == pygame.K_r:
            foreground = random_color()
            background = random_color()
        pygame.draw.rect(win, (foreground if isPressed else background), pygame.Rect(0,0, WIN_SIZE, WIN_SIZE))
    for i in range(WIN_SIZE // square_size +1):
        for j in range(WIN_SIZE // square_size + 1):
            if ((i%2==0 and j%2==0) or (i%2!=0 and j%2!=0)): continue
            pygame.draw.rect(win, (background if isPressed else foreground), pygame.Rect(i*square_size, j*square_size, square_size, square_size))
        pygame.display.flip()
pygame.quit()
