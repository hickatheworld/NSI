##############
# Exercice 1 #
##############

def explose(s, sep):
    """ Renvoie la liste des mots délimités par sep dans s. """
    lst = []
    mot = ""
    for c in s:
        if c in sep:
            if len(mot) > 0:
                lst.append(mot)
            mot = ""
            continue
        mot+=c
    return lst
    
s = "Que j'aime à faire apprendre ce nombre utile aux sages"
print(explose(s, " "))

s = "Hey, you - what are you doing here!?"
print(explose(s, " ,-!?"))

##############
# Exercice 2 #
##############

data = []
f = open("accidents-2019.csv", encoding="utf-8")
f.readline() # passe l'entête
for line in f:
    entry = line[:-1].split(";") # la syntaxe line[:-1] permet de supprimer 
    # le dernier caractère de line qui est un saut de ligne (\n)
    data.append(entry)
f.close()

print(data[0])
    
def question_1(data):
    """ Renvoie le nombre accidents recensés en 2019. """
    return len(data)

def question_2(data):
    """ Renvoie le nombre accidents recensés 
        dans les Bouches-du-Rhône en 2019. """
    c = 0
    for row in data:
        if row[6] == '13':
            c+=1

    return c

def question_3(data):
    """ Renvoie le nombre d'accidents survenus au mois de juillet 2019, 
        en plein jour, hors agglomération, 
        dans des conditions atmosphériques normales. """
    
    c = 0
    for row in data:
        if row[2] == '7' and row[5] == '1' and row[8] == '1' and row[10] == '1':
            c+=1

    return c



def question_4(data):
    """ Renvoie le pourcentage des accidents survenus entre vingt heures 
        et six heures du matin, parmi tous les accidents survenus en 2019. """
    c = 0
    for row in data:
        h = int(row[4][:2])
        if h >= 20 or h < 6:
            c+=1
    return c/len(data) * 100
    
def question_5(data):
    """ Renvoie le numéro du département qui a enregistré le plus 
        d'accidents corporels en 2019. """
    d = {}
    for row in data:
        dep = row[6]
        if dep in d:
            d[dep]+=1
        else:
            d[dep] = 1
    return max(d, key=d.get)

print(question_1(data))
print(question_2(data))
print(question_3(data))
print(question_4(data))
print(question_5(data))