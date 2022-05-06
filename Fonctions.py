import math as m
import numpy as np

#tous les prints mis dans le code servent juste à tester le code et voir le retour

hauteur_tot = 1000 #hauteur du canvas en pixels
n = 10 #nombre de couches (marche avec 13 max, au delà le module math bug, je ne sais pas pourquoi)
n_init = 1.02 #indice de la 1ère couche
n2 = n_init #initialisation
grad = 0.1 #gradient d'indice
hauteur = hauteur_tot/n
beta = 0 #initialisation
positions = [] #initialisation


def calcul_position():
    x = 0
    y = 0
    alpha = 21
    alpha = np.radians(alpha)
    theta = m.asin(n_init/(n_init+grad))
    for i in range(n):
        n2 = n_init + grad*i
        print(n2, "indice")
        print(theta, "theta")
        positions.append([])
        positions[i].append(x)
        positions[i].append(y)
        x += hauteur//m.tan(alpha)        
        beta = m.asin(n_init*m.sin(alpha)/n2)
        alpha = beta
        if alpha <= theta:
            y += hauteur
        else:
            y -= hauteur
        print(alpha, "alpha")
        print("")

    print(positions)

calcul_position()