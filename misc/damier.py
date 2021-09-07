import pygame
import time
from random import randint
from pygame.locals import *

pygame.display.init()

WIN_SIZE=600

win = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))

settings = {
    'lock': True,
    'invert': False,
    'square_size': 50,
    'foreground': (0, 0, 0),
    'background': (255, 255, 255),
    'var': 0
}

def random_color():
    """
    Génère un tuple de couleur RVB
    """
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def change_colors():
    """
    Change les tuples des couleurs de premier plan/arrière-plan par des couleurs aléatoires
    """
    settings['foreground'] = random_color()
    settings['background'] = random_color()


def handle_events():
    events = pygame.event.get()
    """
    Prend en charge les différents événements de la queue
    """
    for e in events:
        if e.type == QUIT: # Ferme la fenêtre
            settings['lock']=False
        if e.type == KEYDOWN and e.key == pygame.K_SPACE: # Inverse les couleurs du damier
            settings['invert']=True
        if e.type == KEYUP and e.key == pygame.K_SPACE: # Met fin à l'inversion des couleurs du damier
            settings['invert']=False
        if e.type == KEYDOWN and e.key == pygame.K_RIGHT: # Augmente la taille des cases
            settings['square_size']+=10
        if e.type == KEYDOWN and e.key == pygame.K_LEFT: # Réduit la taille des cases
            if (settings['square_size'] > 10):
                settings['square_size']-=10
        if e.type == KEYDOWN and e.key == pygame.K_ESCAPE: # Réinitialise la tailled des cases
            settings['square_size'] = 50
        if e.type == KEYDOWN and e.key == pygame.K_f: # Change les couleurs du damier
            change_colors()


while settings['lock']:
    handle_events()
    # Efface le contenu de la fenêtre
    clear_color = (settings['foreground'] if settings['invert'] else settings['background'])
    pygame.draw.rect(win, clear_color, pygame.Rect(0,0, WIN_SIZE, WIN_SIZE))
    settings['var']-=0.2
    if (abs(settings['var']) >= settings['square_size']):
        settings['var'] = 0
    for i in range(WIN_SIZE // settings['square_size'] + 2):
        for j in range(WIN_SIZE // settings['square_size'] + 2):
            # Passe une case sur deux
            if ((i%2==0 and j%2==0) or (i%2!=0 and j%2!=0)): continue
            square_color = (settings['background'] if settings['invert'] else settings['foreground'])
            pygame.draw.rect(win, square_color, pygame.Rect(i*settings['square_size'] + settings['var'], j*settings['square_size'] + settings['var'], settings['square_size'], settings['square_size']))
    pygame.display.flip()
pygame.quit()
