import pygame
from pygame.locals import *
from random import randint
from math import sqrt

class Main :

    def __init__(self, tree, s, w, h):
        self.tree = tree
        
        # initialisation de pygame
        pygame.init()
        self.whs = (w, h, s)
        self.window = pygame.display.set_mode((w, h))
        #self.clock = pygame.time.Clock()
               
        # police de caractère
        df = pygame.font.get_default_font()
        self.font = pygame.font.Font(df, s)
            
        # maintien de la fenêtre
        self.hold()

    def draw(self):
        self.window.fill((0,0,0))
        self.tree.draw(self.window, self.font, self.whs)
        pygame.display.flip()
        
    def hold(self):
        self.draw()
        lock = True
        while lock :
            events_list = pygame.event.get()
            for event in events_list :
                if event.type == QUIT :
                    lock = False
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        lock = False
                    if event.key == K_l :
                        code = self.tree.latex(self.whs)
                        pyperclip.copy(code)
            
            #self.clock.tick(30)
            
        pygame.quit()


class DTree :

    def __init__(self, value):
        self.value = value
        self.children = []
        self.pos = (0, 0)
        
    def add_child(self, value):
        self.children.append(value)
        
    def get_children(self):
        return self.children
        
    def get_center(self, whs):
        w, h, s = whs
        x, y = self.pos
        x = w//2 + int(3*s*x)
        y = 2*s+4*s*y
        return x, y
        
    def draw(self, window, font, whs):
        w, h, s = whs
        
        p = self.get_center(whs)
        for child in self.get_children():
            q = child.get_center(whs)
            pygame.draw.line(window, (196, 196, 196), p, q, 2)

        pygame.draw.circle(window, (196, 196, 196), p, s)
        
        x, y = p
        text = font.render("%s"%self.value, True, (0, 0, 0))
        _, _, w, h = text.get_rect()
        window.blit(text, (x-w//2, y-h//2))
        
        for child in self.get_children():
            child.draw(window, font, whs)
            
    def latex(self, whs):
        lcode, box= self.latex_(whs)
        xmin, xmax, ymin, ymax = box
        xmin -= 1
        ymin -= 1
        xmax += 1
        ymax += 1
        code = "\psset{unit=.025cm,algebraic=true,dimen=middle,dotstyle=o"
        code += ",dotsize=3pt 0,linewidth=1pt,arrowsize=3pt 2,arrowinset=0.25}\n"
        code += "\\begin{pspicture*}(%s,%s)(%s,%s)\n"%(xmin, ymin, xmax, ymax)
        code += "\psframe(%s,%s)(%s,%s)\n"%(xmin, ymin, xmax, ymax)
        code += lcode
        code += "\end{pspicture*}"
        return code
        
    def latex_(self, whs, box=[]):
        w, h, s = whs

        x, y = self.get_center(whs)
        y = h-y
        
        if box :
            xmin = min(box[0], x-s)
            xmax = max(box[1], x+s)
            ymin = min(box[2], y-s)
            ymax = max(box[3], y+s)
            box = [xmin, xmax, ymin, ymax]
        else :
            box = [x-s, x+s, y-s, y+s]
        
        code = "%% Node %s\n"%(self.value)
        code += "\pscircle(%s, %s){%s}\n"%(x, y, s)
        code += "\\rput(%s, %s){%s}\n"%(x, y, self.value)
        
        for child in self.get_children():
            x, y = self.get_center(whs)
            x1, y1 = child.get_center(whs)

            pq = sqrt( (x1-x)**2 + (y1-y)**2 )
            dx = s/pq*(x1-x)
            dy = s/pq*(y1-y)

            x, y = x+dx, h-(y+dy)
            x1, y1 = x1-dx, h-(y1-dy)

            code += "\psline(%s, %s)(%s, %s)\n"%(x, y, x1, y1)

        
        for child in self.get_children():
            ccode, box = child.latex_(whs, box)
            code += ccode

        return code, box

  
    def get_levels(self, l=0, d={}):
        level = l+1
        if d.get(level) is None :
            d[level] = 1
        else :
            d[level] += 1
        for child in self.get_children():
            child.get_levels(level, d)
        return d

    def get_width(self):
        d = self.get_levels(0, {})
        return max([v for v in d.values()])
            
    def compute(self, x=0, y=0):
        self.pos = (x, y)

        children = self.get_children()        
        n = len(children)

        widthes = [child.get_width() for child in children]
        wt = sum(widthes)
        x -= wt/2

        for idx in range(n):
            child = children[idx]
            w = widthes[idx]
            x += w/2
            child.compute(x, y+1)
            x += w/2
       
def get_tree(tree):
    t = DTree(tree.get_value())
    for c in tree.get_children():
        t.add_child(get_tree(c))
    return t
        
def display(tree, s=15, w=800, h=600):
    dtree = get_tree(tree)
    dtree.compute()
    Main(dtree, s, w, h)
    
