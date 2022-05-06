################## Import des librairies ##############################################################
import tkinter as tk
import numpy as np


################## Définition des variables générales #################################################

# 1 px = 0,0264583333 cm et 1 cm = 37,79527559055 px
width_fenetre, height_fenetre = 1000, 700
x0_mirage, x_fin_mirage = width_fenetre / 2 - 500, width_fenetre / 2 + 500
ht_max_mirage = 500

n_init = 1.0 #indice de la 1ère couche
val_grad = 0.1 #gradient d'indice
i_init = np.radians(45)  # test avec angle d'incidence = 45 °


################## Définition des fonctions ###########################################################

def get_couleur_couche(r, g, b):
    """ Retourne une couleur à partir de ses composantes r, g, b entre 0 et 255"""
    return '#{:02x}{:02x}{:02x}'.format(r, g, b) 


def apparition_mirage():
    """Fait apparaître les couches d'air selon leur indice optique"""
    for i in range(nb_couches):
        y0_couche = height_fenetre - i * ht_max_mirage / nb_couches
        y_fin_couche = height_fenetre - (i+1) * ht_max_mirage / nb_couches
        liste_couleur = np.linspace(0, 100, nb_couches)
        couleur_couche = get_couleur_couche(100 + int(liste_couleur[i]), 100 + int(liste_couleur[i]), 150 + int(liste_couleur[i]))
        canvas_discret.create_rectangle((x0_mirage, y0_couche),\
            (x_fin_mirage, y_fin_couche), width = 0, fill = couleur_couche, activefill="thistle4")

        # point (x1,y1) pas inclus dans le rectangle !

def get_nb_couches(var_couches):
    global nb_couches
    nb_couches = int(var_couches)
    apparition_mirage()
    return nb_couches

def get_val_gradient(var_gradient):
    global val_grad
    val_grad = float(var_gradient)
    #appel fonction qui implique le changement de gradient
    print(val_grad)


def calcul_position():
    """Renvoie une liste imbriquée des couples de coordonnées (x,y) \
        pour les points à l'interface de chaque couche"""
    global i_init
    height_couche = ht_max_mirage / nb_couches
    x_i, y_i = 0, height_fenetre
    coordonnees = [[x_i, y_i]]

    for i in range(1, nb_couches + 1):
        n_i = n_init + i * val_grad #indice de la couche i

        coordonnees.append([])        
        x_i +=  height_couche * np.tan(i_init)    
        coordonnees[i].append(x_i) 

        i_i = np.arcsin(n_init * np.sin(i_init) / n_i)
        i_init = i_i
        
        y_i -= height_couche
        coordonnees[i].append(y_i)

    return coordonnees


def trace_rayon():
    """Trace les rayons réfractés à l'aide d'une itération sur la fonction de calcul des positions"""
    liste_coordonnees = calcul_position()
    for i in range(nb_couches):
        canvas_discret.create_line(liste_coordonnees[i], liste_coordonnees[i+1], width = 3, activefill= "red")

################## Création de l'interface Tkinter ####################################################

menu_mod_discret = tk.Tk()
menu_mod_discret.title("Modélisation discrète interactive")

### Fenêtre d'affichage du mirage :
canvas_discret = tk.Canvas(menu_mod_discret, width = width_fenetre, height = height_fenetre, bg = "gray85")
canvas_discret.grid(row=0, column=1)

### Curseurs :
slider_couches = tk.Scale(menu_mod_discret, orient="vertical", from_= 0, to=100,\
        resolution=1, tickinterval=5, length=height_fenetre, command=get_nb_couches, cursor="heart",\
        label="Nombre de couches", font=("Comic Sans MS", 8, "italic"))
slider_couches.grid(row=0, column=0)

slider_gradient = tk.Scale(menu_mod_discret, orient="vertical", from_= 0, to=5,\
        resolution=0.1, tickinterval=1, length=height_fenetre / 2, command=get_val_gradient, cursor="heart",\
        label="Valeur du gradient", font=("Comic Sans MS", 8, "italic"))
slider_gradient.grid(row=0, column=2)

### Tracé de rayon :
bouton_trace = tk.Button(menu_mod_discret, text="Afficher les rayons", font=("Comic Sans MS", 8, "italic"), \
    command=trace_rayon)
bouton_trace.grid(row=0, rowspan=2, column=2)



menu_mod_discret.mainloop()