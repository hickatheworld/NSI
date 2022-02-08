# Question 1 

def recherche_dico(mot, dico):
	deb = 0
	fin = len(dico)
	while deb <= fin:
		med = (deb + fin) // 2
		if dico[med] == mot:
			return True
		elif dico[med] < mot:
			deb = med + 1
		else:
			fin = med - 1
	return False
# Question 2
def indice_prefixe(prefixe, dico):
	deb = 0
	fin = len(dico)
	n = len(prefixe)
	while deb <= fin:
		med = (deb + fin) // 2
		if dico[med][:n] == prefixe:
			return med
		elif dico[med][:n] < prefixe:
			deb = med + 1
		else:
			fin = med - 1
	return -1

def recherche_prefixe(prefixe, dico):
	lst = []
	n = len(prefixe)
	i = indice_prefixe(prefixe, dico)
	j = 0
	descending = True
	while True:
		if dico[i+j][:n] == prefixe:
			lst.append(dico[i+j])
			j = j - 1 if descending else j + 1
		else:
			if descending:
				descending = False
				j = 1
			else:
				break
	return lst

def distance(m1, m2):
	if m1 == '':
		return len(m2)
	elif m2 == '':
		return len(m1)
	s1 = m1[1:]
	s2 = m2[1:]
	if m1[0] == m2[0]:
		return distance(s1, s2)
	else:
		return min(distance(m1, s2) + 1, distance(s1, m2) + 1, distance(s1, s2) + 1)

def correction(mot, dico):
	if mot in dico:
		return mot
	res = None
	minimum = len(dico)
	nearest = recherche_prefixe(mot[:3], dico)
	for el in nearest:
		dist = distance(mot, el)
		if dist < minimum:
			res = el
			minimum = dist
	return res

dico = []
f = open('liste_francais.txt', 'r')
for l in f:
	dico.append(l[:-1])

dico.sort()

print(correction('mangér', dico))