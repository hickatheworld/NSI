from math import sqrt, sin, cos, asin, pi
import pygame
from pygame.locals import *

class Adresse:

    def __init__(self, valeurs):
        self.id = valeurs[0]
        self.numero = int(valeurs[1])
        self.rep = valeurs[2]
        self.nom_voie = valeurs[3]
        self.code_postal = int(valeurs[4])
        self.nom_commune = valeurs[5]
        self.x = float(valeurs[6])
        self.y = float(valeurs[7])
        self.lon = float(valeurs[8])
        self.lat = float(valeurs[9])


    def affiche(self, window, color):
        x = int(0.05331*self.x - 34236)
        y = int(-0.053697*self.y + 368804)
        r = pygame.Rect(x, y, 1, 1)
        pygame.draw.rect(window, color, r)

def question_1(adresses):
    return [adr for adr in adresses if 'Place' in adr.nom_voie]
def question_2(adresses):
    return [adr for adr in adresses if adr.code_postal == 75015 and adr.numero%2==0]

def question_3(adresses):
    return [adr for adr in adresses if 2.3 <= adr.lon <= 2.4 and 48.84 <= adr.lat <= 48.87]

def question_4(adresses):
    voies = {}
    for adr in adresses:
        if adr.nom_voie in voies:
            voies[adr.nom_voie].append(adr)
        else:
            voies[adr.nom_voie] = [adr]
    lens = {k: len(v) for k, v in voies.items()}
    plus_nums = max(lens, key=lens.get)
    return voies[plus_nums]


def question_5(adresses):
    buffon = None
    for a in adresses:
        if a.id == '75115_7089_00016':
            buffon = a
            break
    return [a for a in adresses if distance(buffon, a)<=1]


def distance(a1, a2):
    p1 = a1.lat * pi/180
    p2 = a2.lat * pi/180
    l1 = a1.lon * pi/180
    l2 = a2.lon * pi/180

    d = sin((p2 - p1) / 2)**2 + cos(p1) * cos(p2) * sin((l2 - l1) / 2)**2
    d = sqrt(d)
    d = asin(d)
    d*= 12000
    # d = 12000*asin(sqrt(sin((a2.lat-a1.lat)/2)**2+cos(a1.lat)*cos(a2.lat)*sin((a2.lon-a1.lon)/2)**2))
    return d

# Extraction des données
adresses = []
f = open("adresses-75.csv", encoding="utf-8")
f.readline() # passe l'entête
for line in f:
    entry = line[:-1].split(";")
    adr = Adresse(entry)
    adresses.append(adr)
f.close()

# Affichage des adresses sélectionnées

pygame.init()
window = pygame.display.set_mode((1024, 667))

img = pygame.image.load("paris.png")

liste_adresses = adresses

rafraichir = True
lock = True
while lock:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT :
            lock = False

        if event.type == KEYDOWN :
            if event.key == K_ESCAPE:
                lock = False
            if event.key == K_KP1:
                liste_adresses = question_1(adresses)
            if event.key == K_KP2:
                liste_adresses = question_2(adresses)
            if event.key == K_KP3:
                liste_adresses = question_3(adresses)
            if event.key == K_KP4:
                liste_adresses = question_4(adresses)
            if event.key == K_KP5:
                liste_adresses = question_5(adresses)
            if event.key == K_KP0:
                liste_adresses = adresses
            rafraichir = True

    if rafraichir:
        window.blit(img, (0, 0))
        color = (255, 0, 0)
        for adr in liste_adresses:
            adr.affiche(window, color)
        pygame.display.update()

        rafraichir = False

pygame.quit()


