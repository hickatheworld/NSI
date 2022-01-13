class Liste :

    def __init__(self):
        """ Liste()
            renvoie une liste vide """
        self.val = None
        self.queue = None

    def __repr__(self):
        """ repr(self) -> str
            renvoie une représentation de la liste """
        if self.est_vide():
            return "*"
        return repr(self.val)+" -> "+repr(self.queue)

    def est_vide(self):
        """ self.est_vide() -> bool
            renvoie True si la liste est vide, False sinon """
        return self.val == None

    def taille(self):
        """ self.taille() -> int
            renvoie le nombre de maillons de la liste """
        print(self.est_vide())
        if self.est_vide():
            return 0
        return 1 + self.queue.taille()

    def copy(self, c=None):
        if self.est_vide():
            return Liste()
        c = Liste()
        c.val = self.val
        c.queue = self.queue.copy()
        return c

    def ajoute_debut(self, val):
        """ self.ajoute_debut(obj) -> None
            ajoute un nouveau maillon au début de la liste """
        nl = self.copy()
        self.val = val
        self.queue = nl


    def ajoute_fin(self, val):
        """ self.ajoute_fin(obj) -> None
            ajoute un nouveau maillon à la fin de la liste """
        if self.est_vide():
            self.val = val
            self.queue = Liste()
            return
        self.queue.ajoute_fin(val)

    def dernier(self):
        if self.queue.val == None:
            return self.val
        return self.queue.dernier()

    def ajoute_apres(self, val, n, deb = 0):
        """ self.ajoute_apres(obj) -> None
            ajoute un nouveau maillon après le n-ième maillon """
        assert self.queue != None
        if deb == n:
            self.queue.ajoute_debut(val)
            return
        self.queue.ajoute_apres(val, n, deb+1)



    def supprime_premier(self):
        """ self.supprime_premier() -> Maillon
            supprime et renvoie le premier maillon de la liste """
        pass


    def supprime_dernier(self):
        """ self.supprime_dernier() -> Maillon
            supprime et renvoie le dernier maillon de la liste """
        pass

    def supprime_apres(self, n, deb = None):
        """ self.supprime_dernier() -> Maillon
            supprime et renvoie le n-ième maillon de la liste """
        pass

    def concatene(self, lst):
        """ self.concatene(Liste) -> None
            ajoute les éléments de lst à la fin de la liste """
        pass

    def renverse(self):
        """ self.renverse() -> None
            renverse la liste """
        pass


    def contient(self, val):
        """ self.contient(val) -> bool
            renvoie True si la liste contient l'élément val,
            False sinon """
        pass

    def supprime_doublons(self):
        """ self.supprime_doublons() -> None
            supprime les doublons dans la liste """
        pass

l = Liste()
l.ajoute_fin(141)
l.ajoute_fin(142)
l.ajoute_fin(140)
l.ajoute_debut(1)
l.ajoute_apres(1433, 2)
l.supprime_premier()
print(l)
