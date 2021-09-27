from pile import Pile

p = Pile ()
p.empile('n')
p.empile('s')
p.empile('i')


## Exercice 2
def echange(p):
    x = p.depile()
    y = p.depile()
    p.empile(x)
    p.empile(y)

## Exercice 3
def inverse(p):
    assert p.taille() >= 2
    p1 = Pile()
    p2 = Pile()
    while not p.est_vide():
        x =p.depile()
        p1.empile(x)
        p2.empile(x)
    while not p2.est_vide():
        p.empile(p2.depile())
    return p1

## Exercice 4
def copie(p):
    return inverse(inverse(p))

## Exercice 5
### 1.
def fond(p):
    p1 = Pile()
    while p.taille() > 1:
        p1.empile(p.depile())
    f = p.depile()
    while not p1.est_vide():
        p.empile(p1.depile())
    return f
### 2.
def rotation(p):
    p1 = Pile()
    h = p.depile()
    while not p.est_vide():
        p1.empile(p.depile())
    p.empile(h)
    while not p1.est_vide():
        p.empile(p1.depile())

## Exercice 6
def test_parenthesage(s):
    fermants = (')', ']', '}')
    fermants_attendus = Pile()
    for c in s:
        if c == '(':
            fermants_attendus.empile(')')
        if c == '{':
            fermants_attendus.empile('}')
        if c == '[':
            fermants_attendus.empile(']')
        if c in fermants:
            if fermants_attendus.est_vide() or c != fermants_attendus.depile():
                return False
    return fermants_attendus.est_vide()


assert test_parenthesage ('(a)(b)(((c)(d)))') == True, 't1'
assert test_parenthesage ('([b]){((c))[d]}') == True, 't2'
assert test_parenthesage ('(') == False, 't3'
assert test_parenthesage ('(a))') == False, 't4'
assert test_parenthesage ('((a))}') == False, 't5'
assert test_parenthesage ('[[a]') == False, 't6'
assert test_parenthesage ('[(a])') == False, 't7'
assert test_parenthesage ('{((a)})') == False, 't8'
print('Tests réussis.')
