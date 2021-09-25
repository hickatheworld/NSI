#------------------------------------#
# DM 1 - ****** ****** - Terminale 6  
#------------------------------------#

## Exercice 1 
print('=== Exercice 1 ===')

def vue_sur_la_mer(lst):
    ont_vue = []
    for i in range(len(lst) - 1):
        # On n'effectue pas de tour de boucle pour le dernier élément de la liste
        # Car dans ce cas, lst[i+1:] vaut [] et max([]) renvoie une erreur.
        if lst[i] > max(lst[i+1:]): # Si aucun élément à droite de lst[i] n'est plus grand que lst[i], ce dernier à vue sur la mer.
            ont_vue.append(lst[i])
    ont_vue.append(lst[-1]) # Le dernier élément de la liste a forcément vue sur la mer
    return ont_vue

print(vue_sur_la_mer([5, 12, 8, 9, 5, 2, 3]))

## Exercice 2
print('=== Exercice 2 ===')

def recherche(texte, mot): 
    N = len(mot)
    indexes = []
    for i in range(len(texte)):
        if texte[i:i+N] == mot:
            indexes.append(i)
    return indexes

assert recherche('abcab', 'ab') == [0 , 3]
assert recherche('abc'*3 , 'ab') == [0 , 3 , 6]
assert recherche('ba'*4 , 'ab') == [1 , 3 , 5]
assert recherche('abcd'*2 , 'ad') == []
assert recherche('abcd'*2 , 'da') == [3]
assert recherche('ab'*4 , 'abab') == [0 , 2 , 4]
print('Tous les tests ont réussi.')
## Exercice 3
print('=== Exercice 3 ===')

### 1. a)
def charger_fichier(fichier):
    f = open(fichier, 'r', encoding='utf-8')
    lst = []
    for ligne in f:
        lst.append(ligne[:-1])
    return lst

dico = charger_fichier('dico.txt')

### 1. b)
print(f'Le fichier contient {len(dico)} mots')

### 2.
def mot_dans_dico(mot, dico):
    debut = 0
    fin = len(dico)-1
    while debut <= fin:
        M = (debut + fin)//2
        m = dico[M]
        if mot == m:
            return True
        elif mot < m:
            fin = M-1
        else:
            debut = M+1
    return False

mots = charger_fichier('mots.txt')

print('Mots mystère: ')
for mot in mots:
    if not mot_dans_dico(mot, dico):
        print(mot)