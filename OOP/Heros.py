from random import randint

class Heros:

    def __init__(self, nom, pv, res, dmax):
        print("Création du héros "+nom)
        self.nom = nom
        self.points_de_vie = pv
        self.resistance = res
        self.degats_max = dmax
        self.vies = 3

    def est_en_vie(self):
        return self.points_de_vie>0

    def attaque(self, autre):
        r = randint(1, 10)
        if self.est_en_vie():
            if r == 5:
                print(self.nom, 'lance son attaque spéciale')
                degats = self.degats_max
            else:
                degats = randint(1, self.degats_max)
            autre.subit_attaque(self, degats)
            
    def subit_attaque(self, autre, degats):
        if degats>self.resistance:
            self.points_de_vie -= degats
            print(self.nom+" perd "+str(degats)+" points de vie")
        else:
            print(autre.nom+" a raté son attaque contre "+self.nom)
        if not self.est_en_vie():
            print(autre.nom+" a tué "+self.nom)
            self.ressuscite()
    
    def ressuscite(self):
        if self.vies > 1:
            self.vies-=1
            self.points_de_vie = 100
            print(self.nom, 'a ressuscité.')
        else:
            print(self.nom, 'n\'a pas pu ressusciter.')
        
#scenario

achille = Heros("Achille", 100, 10, 30)
hector = Heros("Hector", 100, 15, 25)
paris = Heros('Paris', 100, 25, 100)

while achille.points_de_vie > 20 and hector.points_de_vie > 20:
    achille.attaque(hector)
    hector.attaque(achille)
print('Combat terminé.')
print('Achille a', achille.points_de_vie, 'points de vie')
print('Hector a', hector.points_de_vie, 'points de vie')

while achille.est_en_vie():
    paris.attaque(achille)