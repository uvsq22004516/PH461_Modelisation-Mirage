################## Informations sur le groupe #######################

# L2 Double-Licence MPSI
# BEAUSSANT Alberic     < alberic.beaussant@ens.uvsq.fr >
# CHAMPENOIS Gabriel    < gabriel.champenois@ens.uvsq.fr >
# DEDINGER Marc         < marc.dedinger@ens.uvsq.fr >

# https://github.com/uvsq22004516/PH461_Modelisation-Mirage


################## Import des librairies ###########################################################################
import numpy as np
import math as ma
import tkinter as tk

################## Définition des variables globales / constantes : ################################################

width_fenetre, height_fenetre = 900, 700                                    # constantes
x0_mirage, x_fin_mirage = width_fenetre / 2 - 500, width_fenetre / 2 + 500  # constantes
ht_max_mirage = 500                                                         # constante

segments_rayon = [] # variable globale de type liste 
#                     permettant de stocker les segments successifs du tracé (cette variable est globale 
#                     pour permettre de supprimer les segments du tracé précédent lors d'un nouveau tracé)

segments_normales = [] # variable globale de type liste 
#                        permettant de stocker les normales aux interfaces entre couches (cette variable est globale 
#                        pour permettre de supprimer les segments du tracé précédent lors d'un nouveau tracé)
####################################################################################################################
######## FONCTIONS DE MODELISATION DISCRETE ########################################################################

def get_couleur_couche (r, g, b) :
    """ Retourne une couleur à partir de ses composantes r, g, b entre 0 et 255"""
    return '#{:02x}{:02x}{:02x}'.format(r, g, b) 

def apparition_mirage () :
    """Fait apparaître les couches d'air selon leur indice optique"""
    nb_couches = int (slider_couches.get ())
    for i in range (nb_couches):
        y0_couche = height_fenetre - i * ht_max_mirage / nb_couches
        y_fin_couche = height_fenetre - (i+1) * ht_max_mirage / nb_couches
        liste_couleur = np.linspace (0, 100, nb_couches)
        couleur_couche = get_couleur_couche (100 + int (liste_couleur [i]), 100 + int (liste_couleur [i]), \
            150 + int (liste_couleur [i]))
        canvas_discret.create_rectangle ((x0_mirage, y0_couche),\
            (x_fin_mirage, y_fin_couche), width = 0, fill = couleur_couche, activefill = "thistle4")

def get_nb_couches (var_couches) :
    """Permet la sélection d'un nombre de couches d'air pour les afficher"""
    nb_couches = int (var_couches)
    apparition_mirage ()
    return nb_couches

def valider_indices () :
    """Si les indices optiques choisis sont cohérents avec les bornes imposées, la fonction renvoie \
        une liste contenant autant d'indices optiques que le nombre de couches \
        et régulièrement espacés (gradient constant)"""
    global segments_rayon, segments_normales

    nb_couches = int ( slider_couches.get () )

    indice_bas = float (saisie_indice_bas.get ())
    indice_haut = float (saisie_indice_haut.get ())

    if (indice_bas >= 1.00027 and indice_bas <= 1.00031) and (indice_haut >= 1.00027 and indice_haut <= 1.00031) :
        liste_indices = np.linspace(indice_bas, indice_haut, nb_couches)
        existence_liste_indices = True
      
    elif indice_bas <= 1.00027 or indice_bas >= 1.00031 or indice_haut <= 1.00027 or indice_haut >= 1.00031:
        liste_indices = None
        indice_bas = None
        indice_haut = None
        existence_liste_indices = False
    return liste_indices, nb_couches, segments_rayon, segments_normales, existence_liste_indices

def get_position_objet ():
    """Permet la sélection de l'altitude de l'objet""" 
    y_reel_objet = float ( slider_position_objet.get () )
    return y_reel_objet

def choix_position () :
    """Fonction qui, en cliquant sur le bouton intitulé {3. Choisir la position de l'objet}, permet d'afficher \
        le curseur pour le choix de la position de l'objet (pour une observation plus intéressante l'intervalle \
        varie selon le type de mirage) ou un message lorsque le choix des indices n'est pas effectué"""
    global slider_position_objet
    liste_indices = valider_indices() [0]
    existence_liste_indices = valider_indices() [4]

    if existence_liste_indices == False : 
        txt_choix_position = tk.Label (menu_mod_discret, \
            text = "Choisir des indices optiques \n avant de pouvoir bouger l'objet ! ", \
            font = ("Comic Sans MS", 8, "bold", "italic"), fg = "thistle4")
        txt_choix_position.grid(row = 0, rowspan = 2, column = 2)
        slider_position_objet = None
        menu_mod_discret.after(3000, txt_choix_position.destroy)

    elif existence_liste_indices == True : 
        bouton_position.grid_remove()
        test_type = "pas de mirage"
        if liste_indices [0] < liste_indices [1]:     # mirage chaud / inférieur
            if test_type == "mirage froid":
                slider_position_objet.destroy
            test_type = "mirage chaud"
            slider_position_objet = tk.Scale (menu_mod_discret, command = get_position_objet, orient = "vertical", \
                from_= ht_max_mirage // 2, to = ht_max_mirage, resolution = 1, tickinterval = 50, \
                length = height_fenetre / 3, cursor = "heart", label = "3. Position de l'objet", font = ("Comic Sans MS", 8, "bold", "italic"))
            slider_position_objet.grid (row = 0, column = 2)

        elif liste_indices [0] > liste_indices [1]:   # mirage froid / supérieur
            if test_type == "mirage chaud":
                slider_position_objet.destroy
            test_type = "mirage froid"
            slider_position_objet = tk.Scale (menu_mod_discret, command = get_position_objet, orient = "vertical", \
                from_= 0, to = ht_max_mirage // 2, resolution = 1, tickinterval = 50, length = height_fenetre / 3, \
                cursor = "heart", label = "3. Position de l'objet", font = ("Comic Sans MS", 8, "bold", "italic"))
            slider_position_objet.grid (row = 0, column = 2)

    return slider_position_objet


def calcul_angle_incidence () :
    """Renvoie une liste des angles d'incidence aux normales par \
        application de la loi de Snell-Descartes"""
    liste_angle_incidence = []
    liste_indices = valider_indices () [0]    
    nb_couches = valider_indices () [1]

    incidence_i = np.radians (int ( slider_incidence_init.get () ) )
    liste_angle_incidence.append (incidence_i)

    for i in range (1, nb_couches) :
        indice_couche_precedente = liste_indices [i - 1]                  # indice de la couche i - 1       
        indice_couche_i = liste_indices [i]                               # indice de la couche i
        incidence_i = np.arcsin ( indice_couche_precedente \
            * np.sin (liste_angle_incidence [i - 1]) / indice_couche_i ) 
        liste_angle_incidence.append (incidence_i)

    return liste_angle_incidence

def calcul_position () :
    """Renvoie une liste imbriquée des couples de coordonnées (x,y) \
        pour les points à l'interface de chaque couche"""
    liste_coordonnees = []

    nb_couches = valider_indices () [1]
    y_reel_objet = get_position_objet()
    position_init = height_fenetre - y_reel_objet
    height_couche = ht_max_mirage / nb_couches

    x_i, y_i = 0, position_init 
    liste_coordonnees.append ([])
    liste_coordonnees [0].append (x_i)
    liste_coordonnees [0].append (y_i)  

    liste_indice = valider_indices() [0]
    liste_angle_incidence = calcul_angle_incidence()
    condition_trace = height_fenetre - ht_max_mirage # variable pour la condition sur y
    #                                                  qui stoppe le tracé si non vérifiée

    # premier calcul hors de la boucle itérative au cas où l'objet ne serait pas aux coordonées (0,0):    
    y_i -= (y_reel_objet // height_couche + 1) * height_couche - y_reel_objet
    x_i += (position_init - y_i) * np.tan( liste_angle_incidence [0] )
    if y_i >= condition_trace :
        liste_coordonnees.append ( [] )    
        liste_coordonnees [1].append (x_i)
        liste_coordonnees [1].append (y_i)

    for i in range (2, nb_couches+1): 
        y_i -= height_couche       
        x_i += (height_fenetre - y_i) * np.tan ( liste_angle_incidence [i - 1] )    
        if y_i >= condition_trace :
            liste_coordonnees.append ( [] )
            liste_coordonnees [i].append (x_i)
            liste_coordonnees [i].append (y_i)

    return liste_coordonnees, height_couche

def trace_rayon (event):
    """Trace les rayons réfractés et les normales aux interfaces (si moins de 30 couches \
        pour une question de lisibilité) à l'aide d'une itération sur la fonction \
        de calcul des positions et efface le tracé précédent s'il existe"""
    global segments_rayon, segments_normales
    
    nb_couches = valider_indices () [1]
    height_couche = calcul_position () [1]
    liste_coordonnees = calcul_position () [0]

    if len (segments_rayon) != 0:
        for i in range  ( len (segments_rayon) ):
            canvas_discret.delete (segments_rayon [i]) 
        segments_rayon = []
    if len (segments_normales) != 0:
        for i in range( len (segments_normales) ):
            canvas_discret.delete (segments_normales [i]) 
        segments_normales = []

    for i in range (nb_couches):
        segments_rayon.append (canvas_discret.create_line (liste_coordonnees [i], liste_coordonnees [i+1], \
            width = 1, activefill = "red", joinstyle = "round", capstyle = "round"))
        if nb_couches <= 30 and i <= nb_couches - 2 :
            segments_normales.append (canvas_discret.create_line ((liste_coordonnees [i+1] [0], \
                liste_coordonnees [i+1] [1] + height_couche / 2), (liste_coordonnees [i+1] [0], \
                liste_coordonnees [i+1] [1] - height_couche / 2), fill = "red", dash = (int (height_couche) // 10,)))
        elif nb_couches <= 30 and i == nb_couches - 1 :
            segments_normales.append (canvas_discret.create_line ((liste_coordonnees [i+1] [0], \
                liste_coordonnees [i+1] [1] + height_couche / 2), (liste_coordonnees [i+1] [0], \
                liste_coordonnees [i+1] [1]), fill = "red", dash = (int (height_couche) // 10,)))
        
    return segments_rayon, segments_normales


####################################################################################################################
############### Définition et placement des widgets : ##############################################################

menu_mod_discret = tk.Tk ()
menu_mod_discret.title ("Modélisation discrète interactive")

# Fenêtre d'affichage du mirage :
canvas_discret = tk.Canvas (menu_mod_discret, width = width_fenetre, height = height_fenetre, bg = "gray85")
canvas_discret.grid (row = 0, rowspan = 4, column = 1)


## Curseur pour le nombre de couches
slider_couches = tk.Scale (menu_mod_discret, orient = "vertical", from_ = 0, to = 100,\
    resolution = 1, tickinterval = 10, length = height_fenetre / 3, command = get_nb_couches, cursor = "heart",\
    label = "1. Nombre de couches", font = ("Comic Sans MS", 8, "bold", "italic"))
slider_couches.grid (row = 0, column = 0)

# Intervalle d'indices optiques :
# Choix de l'indice optique de la première couche 
txt_choix_indice_bas = tk.Label (menu_mod_discret, text = "Indice de la première couche :", \
    font = ("Comic Sans MS", 8, "bold", "italic"), fg = "thistle4")
txt_choix_indice_bas.grid (row = 1, column = 0)
saisie_indice_bas = tk.Entry (menu_mod_discret, font = ("Comic Sans MS", 8))
saisie_indice_bas.insert(0, 1.00031)
saisie_indice_bas.grid (row = 1, rowspan = 2, column = 0)

# Choix de l'indice optique de la dernière couche
txt_choix_indice_haut = tk.Label (menu_mod_discret, text = "Indice de la dernière couche \n(< première couche car la modélisation\n du mirage chaude ne fonctionne pas) :", \
    font = ("Comic Sans MS", 8, "bold", "italic"), fg = "thistle4")
txt_choix_indice_haut.grid (row = 2, column = 0)
saisie_indice_haut = tk.Entry (menu_mod_discret, font = ("Comic Sans MS", 8))
saisie_indice_haut.insert(0, 1.00027)
saisie_indice_haut.grid (row = 2, rowspan = 2, column = 0)

# Pour préciser l'intervalle de choix des indices optiques 
txt_range_indices = tk.Label (menu_mod_discret, text = "2. Choisir des indices entre \n 1.00027 et 1.00031 !", \
        font = ("Comic Sans MS", 8, "bold", "italic"))
txt_range_indices.grid (row = 0, rowspan = 4, column = 0)

# Bouton pour valider la saisie
bouton_indices = tk.Button (menu_mod_discret, text = "Valider", font = ("Comic Sans MS", 8, "bold", "italic"),\
    command = valider_indices)
bouton_indices.grid (row = 3, rowspan = 3, column = 0)


## Bouton pour afficher le choix de position de l'objet :
bouton_position = tk.Button (menu_mod_discret, text = "3. Choisir la position de l'objet", font = ("Comic Sans MS", 8, "bold", "italic"),\
    command = choix_position)
bouton_position.grid (row = 0, column = 2)


## Curseur pour l'angle d'incidence sur le premier dioptre
slider_incidence_init = tk.Scale (menu_mod_discret, orient = "vertical", from_ = 0, to = 45,\
    resolution = 1, tickinterval = 5, length = height_fenetre / 3, cursor = "heart",\
    label = "4. Angle d'incidence initial", font = ("Comic Sans MS", 8, "bold", "italic"))
slider_incidence_init.grid (row = 1, rowspan = 2, column = 2)

## Afficher le tracé de rayons en cliquant sur le canvas_discret:
canvas_discret.bind ("<Button-1>", trace_rayon)
# Message:
canvas_discret.create_text ((width_fenetre / 2, (height_fenetre - ht_max_mirage) / 2), \
    text = "Afficher le rayon", font = ("Comic Sans MS", 15))

menu_mod_discret.mainloop ()