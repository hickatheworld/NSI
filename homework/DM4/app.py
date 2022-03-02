import pygame, os
import shutil, subprocess
from PIL import Image
pygame.init()

# Constantes
WIDTH = 500
HEIGHT = 500
ACCEPTED_FORMATS = ['jpg', 'jpeg', 'png']

# Ressources
drop_icon = pygame.image.load(os.path.join('.', 'drop_icon.png'))
roboto = pygame.font.Font(os.path.join('.', 'Roboto.ttf'), 25)
roboto_small = pygame.font.Font(os.path.join('.', 'Roboto.ttf'), 18)
roboto_xs = pygame.font.Font(os.path.join('.', 'Roboto.ttf'), 14)

# Fenêtre
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hidden Image Data Finder')

# Fonctions
def manage_events(home=False):
    """
    Traite les événements pygame.
    """
    global mode
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        if home and e.type == pygame.DROPFILE: # On n'accepte le glisser-déposer que sur l'écran d'accueil
            if check_file(e.file):
                show_hidden_data(e.file)
            else:
                show_home('Format de fichier non pris en charge.')
        if home and e.type == pygame.KEYDOWN and e.key == pygame.K_m: # On n'accepte le changement de mode que sur l'écran d'accueil
            mode = 'Image' if mode == 'Texte' else 'Texte'
            show_home() # L'affichage est mis à jour pour indiquer le changement de mode

def clear_screen():
    """
    Réinitialise l'affichage.
    """
    # Fond
    window.fill((50, 50, 50))
    # Titre
    title = roboto.render('Hidden Image Data Finder', True, (255, 255, 255))
    title_size = title.get_size()
    window.blit(title, (WIDTH / 2 - title_size[0] / 2, 10))
    pygame.draw.rect(window, (100, 100, 100), (0, 50, WIDTH, 1))
    pygame.display.update()

def show_home(error=''):
    """
    Affiche l'écran d'accueil.
    """
    clear_screen()
    # Icône
    window.blit(drop_icon, (WIDTH/2 - drop_icon.get_width()/2, HEIGHT/2 - drop_icon.get_height()/2))
    # Texte indicatif
    info_surface = roboto.render('Glissez votre image ici', True, (255, 255, 255))
    info_size = info_surface.get_size()
    window.blit(info_surface, (WIDTH/2 - info_size[0]/2, HEIGHT/2 + drop_icon.get_height()/2 - info_size[1] + 20))
    # Indicateur de mode:
    mode_surface = roboto_small.render('Mode: ' + mode, True, (255, 255, 255))
    mode_size = mode_surface.get_size()
    window.blit(mode_surface, (WIDTH/2 - mode_size[0]/2, HEIGHT/2 + drop_icon.get_height()/2 - info_size[1] + 50))
    # Aide pour changer de mode
    help_surface = roboto_xs.render('Appuyez sur m pour changer de mode.', True, (255, 255, 255))
    help_size = help_surface.get_size()
    window.blit(help_surface, (WIDTH/2 - help_size[0]/2, HEIGHT - help_size[1] - 5))
    # Texte d'erreur
    if len(error) > 0:
        error_surface = roboto_small.render(error, True, (255, 50, 50))
        error_size = error_surface.get_size()
        window.blit(error_surface, (WIDTH/2 - error_size[0]/2, HEIGHT/2 - drop_icon.get_height()/2 - 20))
    pygame.display.update()

def check_file(filename):
    """
    Vérifie si le fichier est pris en charge.
    """
    return filename.split('.')[-1] in ACCEPTED_FORMATS

def get_back(v):
    """
    Récupère la valeur des bits de poids faible dans l'octet donné.
    """
	# front = v >> 4
    back = v & 0xF
    return back

def show_hidden_data(filename):
    """
    Récupère les pixels de l'image cachée et affiche la progression du traitement.
    """
    global mode
    # Affichage initial
    clear_screen()
    loading_label = roboto_small.render('Chargement...', True, (255, 255, 255))
    loading_label_size = loading_label.get_size()
    window.blit(loading_label, (WIDTH / 2 - loading_label_size[0] / 2, HEIGHT / 2 - loading_label_size[1] / 2 - 100))
    pygame.display.update()

    # On convertit l'image en RGB pour s'assurer de n'avoir toujours que 3 canaux de couleurs par pixel. Le canal alpha ne semble pas nécessaire.
    original = Image.open(filename).convert('RGB') 
    w, h = original.size
    result = Image.new('RGB', (w, h)) # Pour le mode Image
    txt = '' # Pour le mode Texte

    m = w * h # Nombre de pixels à traiter
    i = 0 # Nombre de pixels traités
    for x in range(w):
        # On traite les événements pygame dans cette boucle aussi pour éviter que la fenêtre ne gèle.
        manage_events()
        for y in range(h):
            r, g, b = original.getpixel((x, y))
            if mode == 'Image':
                result.putpixel((x, y), (get_back(r), get_back(g), get_back(b)))
            else:
                # Les bits rouges sont premiers dans la séquence de 12 bits, les bits verts suivent, et les bits bleus les derniers.
                # On doit donc les décaler pour avoir la valeur correcte.
                v = get_back(r) << 8 | get_back(g) << 4 | get_back(b)
                txt+= chr(v)
            i+=1
        # On met à jour la progression à chaque ligne de pixels traitée
        # Le faire pour chaque pixel ralentit trop le programme.
        # Barre de progression
        pygame.draw.rect(window, (210, 210, 210), (WIDTH / 2 - 150, HEIGHT / 2 - 50, 300, 50)) # Fond de la barre
        pygame.draw.rect(window, (255, 255, 255), (WIDTH / 2 - 150, HEIGHT / 2 - 50, i/m * 300, 50)) # Indicateur de progression
        # Pourcentage de progression
        percentage = roboto.render(str(round(i/m * 100)) + '%', True, (0, 0, 0))
        percentage_size = percentage.get_size()
        window.blit(percentage, (WIDTH / 2 - percentage_size[0] / 2, HEIGHT / 2 - percentage_size[1] / 2 - 25))
        pygame.display.update()
    
    # Affichage du résultat et retour à l'écran d'accueil
    show_home()
    if mode == 'Image':
        result.show()
    else:
        # Écriture du résultat dans un fichier texte
        textfile = filename.split('.')[0] + '.txt'
        f = open(textfile, 'w', encoding='utf-8')
        f.write(txt)
        f.close()
        # Ouverture du fichier texte dans l'éditeur de texte de l'OS
        if hasattr(os, "startfile"): # Windows 
            os.startfile(textfile)
        elif shutil.which("xdg-open"): # Linux
            subprocess.call(["xdg-open", textfile])
        elif "EDITOR" in os.environ: # Mac OS X
            subprocess.call([os.environ["EDITOR"], textfile])
        else: # En cas de problème
            print(txt)

# Boucle principale
# Deux modes possibles: Image -> trouve l'image cachée, Texte -> trouve le texte caché
mode = 'Image' 

show_home()
while True:
    manage_events(True)