
import math as m
import numpy as np

#Définition de variables pour test

alpha = 30
alpha = np.radians(alpha)

n1 = 1.1
n2 = 1.01

beta = 0

#Nombre de couches et hauteur

hauteur_tot = 600
nb_couche = 3


def calcul_angle_refl(): 

    beta = m.asin((n1*m.sin(alpha))/n2)
    return beta
    return alpha

#Coordonnées du point de départ

pos_depart = [100, 100]
pos_fin = [0,0]
hauteur_couche = hauteur_tot/nb_couche
coords_tot = []


def position_point():
    alpha = 31
    for i in range(nb_couche):
        a = hauteur_couche/m.tan(alpha)
        beta = m.asin((n1*m.sin(alpha))/n2)
        alpha = beta
        pos_fin[0] = pos_depart[0] + a
        pos_fin[1] = pos_depart[1] + hauteur_couche*(i+1)
        coords_tot.append(pos_fin[0])
        coords_tot.append(pos_fin[1])
        coords_tot.append('')

    print(coords_tot)


calcul_angle_refl()
position_point()