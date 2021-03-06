from displayer import display
from random import randint

class Node:

    def __init__(self, value):
        self.value = value
        self.children = []
        
    def get_value(self):
        """ self.get_value() -> obj
            Renvoie la valeur associée à ce noeud.
            (Méthode utilisée par la fonction display) """
        return self.value
        
    def get_children(self):
        """ self.get_value() -> list
            Renvoie la liste des enfants de ce noeud.
            (Méthode utilisée par la fonction display) """
        return self.children

    def size(self):
        c = 1
        for child in self.children:
            c+=child.size()
        return c

    def height(self):
        h = 0
        for c in self.children:
            h = max(h, c.height())
        return h + 1
    
    def arity(self, current_max=0):
        if len(self.children) == 0:
            return current_max
        max_of_children = max([c.arity(max(current_max, len(self.children))) for c in self.children]) 
        return max(current_max, max_of_children)

    def get_values(self):
        lst = [self.value]
        for c in self.children:
            lst.extend(c.get_values())
        return lst

    def remove_leaves(self):
        i = 0
        while i < len(self.children):
            c = self.children[i]
            if len(c.children) == 0:
                self.children.pop(i)
            else:
                c.remove_leaves()
                i+=1

    def insert(self, n, arity=None):
        if arity == None:
            arity = self.arity()
        if len(self.children) == arity:
            for c in self.children:
                if len(c.children) < arity:
                    return c.insert(n, arity)
            if len(self.children) > 0:
                return self.children[0].insert(n)
        self.children.append(Node(n))

    def niveau(self, n):
        assert n <= self.height() 
        lst = []
        if n==0:
            return [self.value]
        if n-1==0:
            return [c.value for c in self.children]
        for c in self.children:
            lst.extend(c.niveau(n-1))
        return lst

    def rightest_leaf(self):
        if len(self.children) == 0:
            return self
        return self.children[-1].rightest_leaf()


def get_random_tree(node=Node("R"), depth=3):
    """ Renvoie un arbre "aléatoire" de hauteur depth. """
    if depth==0:
        return node
    for i in range(randint(0, 3)):
        etiq = chr(randint(65, 90))
        new_node = Node(etiq)
        child = get_random_tree(new_node, depth-1)
        node.children.append(child)
    return node

root = get_random_tree()
display(root, 20)