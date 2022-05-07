################## Import des librairies ##############################################################
import numpy as np
import tkinter as tk

################## Définition des variables globales / constantes : ################################################

width_fenetre, height_fenetre = 900, 700
x0_mirage, x_fin_mirage = width_fenetre / 2 - 500, width_fenetre / 2 + 500
ht_max_mirage = 500

n_init = 1.0 #indice de la 1ère couche

###################################################
######## FONCTIONS DE MODELISATION DISCRETE #######

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


def get_nb_couches(var_couches):
    global nb_couches
    nb_couches = int(var_couches)
    apparition_mirage()
    return nb_couches


def get_incidence_init(var_inc_init):
    global i_init
    i_init = np.radians(int(var_inc_init))
    return i_init


def get_val_gradient():
    """Renvoie la valeur du gradient saisie"""
    global val_grad, exist_txt_erreur_grad
    a = float(saisie_grad.get())
    if a >= -0.05 and a <= 0.05:
        if exist_txt_erreur_grad == True:
            txt_erreur_grad.grid_remove()
        val_grad = float(saisie_grad.get())
    elif a <= -0.05 or a >= 0.05:
        val_grad = None
        txt_erreur_grad.grid(row=2, rowspan = 2, column=0)
        exist_txt_erreur_grad = True
    return val_grad


def calcul_position():
    """Renvoie une liste imbriquée des couples de coordonnées (x,y) \
        pour les points à l'interface de chaque couche"""
    global i_init
    height_couche = ht_max_mirage / nb_couches
    x_i, y_i = 0, height_fenetre 
    coordonnees = [[x_i, y_i]]
    incidence_iter = i_init
    i = 1                                            #indice implémenté au cours du tracé 
    condition_trace = height_fenetre - ht_max_mirage #variable pour la condition sur y \
    #                                                qui stoppe le tracé si non vérifiée

    while y_i > condition_trace and i <= nb_couches: 
        n_i = n_init + i * val_grad                  #indice de la couche i

        coordonnees.append([])        
        x_i +=  height_couche * np.tan(incidence_iter)    
        coordonnees[i].append(x_i) 

        i_i = np.arcsin(n_init * np.sin(incidence_iter) / n_i)
        incidence_iter = i_i
        
        y_i -= height_couche
        coordonnees[i].append(y_i)
        i += 1

    return coordonnees


def trace_rayon(event):
    """Trace les rayons réfractés à l'aide d'une itération sur la fonction de calcul des positions"""
    liste_coordonnees = calcul_position()
    for i in range(nb_couches):
        canvas_discret.create_line(liste_coordonnees[i], liste_coordonnees[i+1], width = 3, activefill= "thistle4", \
            joinstyle="round", capstyle="round")  


####################################################################################################################
############### Définition et placement des widgets : ##############################################################

menu_mod_discret = tk.Tk()
menu_mod_discret.title("Modélisation discrète interactive")

### Fenêtre d'affichage du mirage :
canvas_discret = tk.Canvas(menu_mod_discret, width = width_fenetre, height = height_fenetre, bg = "gray85")
canvas_discret.grid(row=0, rowspan=4, column=1)
#Permet, en cliquant sur le canvas_discret, d'afficher le tracé de rayons:
canvas_discret.bind("<Button-1>", trace_rayon)
#Message:
canvas_discret.create_text((width_fenetre/2, (height_fenetre-ht_max_mirage)/2), \
    text="Afficher le rayon", font=("Comic Sans MS", 15, "bold"))


### Curseurs :
slider_couches = tk.Scale(menu_mod_discret, orient="vertical", from_= 0, to=100,\
    resolution=1, tickinterval=10, length=height_fenetre/3, command=get_nb_couches, cursor="heart",\
    label="Nombre de couches", font=("Comic Sans MS", 8, "italic"))
slider_couches.grid(row=0, column=0)

slider_incidence_init = tk.Scale(menu_mod_discret, orient="vertical", from_= 0, to=45,\
    resolution=1, tickinterval=5, length=height_fenetre/3, command=get_incidence_init, cursor="heart",\
    label="Angle d'incidence initial", font=("Comic Sans MS", 8, "italic"))
slider_incidence_init.grid(row=0, column=2)


txt_choix_grad = tk.Label(menu_mod_discret, text="Choisir un gradient \n d'indice (float entre -0.05 et 0.05)", \
    font=("Comic Sans MS", 8, "bold"))
txt_choix_grad.grid(row=1, column=0)

# si la valeur de gradient n'est pas cohérente 
exist_txt_erreur_grad = False
txt_erreur_grad = tk.Label(menu_mod_discret, text="Choisir un gradient d'indice entre -0.05 et 0.05 !", \
        font=("Comic Sans MS", 8, "bold"), fg="red")

saisie_grad = tk.Entry(menu_mod_discret, font=("Comic Sans MS", 8, "bold"))
saisie_grad.grid(row=1, rowspan=2, column=0)

valider_grad = tk.Button(menu_mod_discret, text="Valider", font=("Comic Sans MS", 8, "italic"),\
    command=get_val_gradient)
valider_grad.grid(row=1, rowspan=3, column=0)

### Tracé de rayon :
#bouton_trace = tk.Button(menu_mod_discret, text="Afficher les rayons", font=("Comic Sans MS", 8, "bold"), \
#    command=trace_rayon)
#bouton_trace.grid(row=1, column=2)

menu_mod_discret.mainloop()