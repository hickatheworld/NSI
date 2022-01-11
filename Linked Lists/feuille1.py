class Maillon :

    def __init__(self, val):
        """ Maillon(obj)
            renvoie un maillon contenant l'Ã©lÃ©ment val """
        self.val = val
        self.suiv = None


class Liste :

    def __init__(self):
        """ Liste()
            renvoie une liste vide """
        self.tete = None

    def __repr__(self):
        """ repr(self) -> str
            renvoie une reprÃ©sentation de la liste """
        if self.est_vide():
            return "liste vide"

        s = "liste : "
        maillon = self.tete
        while maillon != None :
            s += repr(maillon.val)+" -> "
            maillon = maillon.suiv
        return s+" None"

    def est_vide(self):
        """ self.est_vide() -> bool
            renvoie True si la liste est vide, False sinon """
        return self.tete == None

    def taille(self):
        """ self.taille() -> int
            renvoie le nombre de maillons de la liste """
        m = self.tete
        c = 0
        while m != None:
            c+=1
            m = m.suiv
        return c

    def ajoute_debut(self, val):
        """ self.ajoute_debut(obj) -> None
            ajoute un nouveau maillon au dÃ©but de la liste """
        t = self.tete
        self.tete = Maillon(val)
        self.tete.suiv = t

    def ajoute_fin(self, val):
        """ self.ajoute_fin(obj) -> None
            ajoute un nouveau maillon Ã  la fin de la liste """
        self.ajoute_apres(val, self.taille()-1)

    def ajoute_apres(self, val, n):
        """ self.ajoute_a_la_fin(obj) -> None
            ajoute un nouveau maillon aprÃ¨s le n-iÃ¨me maillon """
        assert n < self.taille(), "IndexError: list index out of range"
        if self.taille() == 0:
            return self.ajoute_debut(val)
        m = self.tete
        for i in range(n):
            m = m.suiv
        m1 = m.suiv
        nm = Maillon(val)
        m.suiv = nm
        nm.suiv = m1



    def supprime_premier(self):
        """ self.supprime_premier() -> Maillon
            supprime et renvoie le premier maillon de la liste """
        assert not self.est_vide(), "déjà vide"
        v = self.tete
        self.tete = self.tete.suiv
        return v

    def supprime_dernier(self):
        """ self.supprime_dernier() -> Maillon
            supprime et renvoie le dernier maillon de la liste """
        assert not self.est_vide(),"déjà vide"
        m = self.tete
        if self.tete.suiv == None:
            t = self.tete
            self.tete = None
            return t
        while m.suiv.suiv!= None:
            m = m.suiv
        m.suiv = None

    def supprime_apres(self, n):
        """ self.supprime_dernier() -> Maillon
            supprime et renvoie le n-iÃ¨me maillon de la liste """
        assert self.tete != None and n < self.taille()-1
        m = self.tete
        for i in range(n):
            m = m.suiv
        m.suiv = m.suiv.suiv


    def concatene(self, lst):
        """ self.concatene(Liste) -> None
            ajoute les Ã©lÃ©ments de lst Ã  la fin de la liste """
        m = lst.tete
        while m != None:
            self.ajoute_fin(m.val)
            m = m.suiv

    def renverse(self):
        """ self.renverse() -> None
            renverse la liste """


    def contient(self, val):
        """ self.contient(val) -> bool
            renvoie True si la liste contient l'Ã©lÃ©ment val,
            False sinon """
        pass

    def supprime_doublons(self):
        """ self.supprime_doublons() -> None
            supprime les doublons dans la liste """
        pass

# help(Liste)



l = Liste()
l.ajoute_debut(5)
l.ajoute_debut(4)
l.ajoute_debut(3)
print(l)
l.supprime_apres(1)
print(l)
