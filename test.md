Projet Mirage


Idée générale

L’objectif de ce projet est de créer un interface sur Python grâce au module Tkinter, qui va permettre de modéliser la trajectoire d’un faisceau lumineux émis par un point d’une source.
On considérera, en première approche, un gradient de température constant, dont la valeur pourrait être choisie par l’utilisateur. On choisit, pour cette réalisation (modèle discret), d’appliquer la loi de Snell-Descartes sur un nombre fini (à choisir par l’utilisateur ?? ) de couches d’indice optique variant donc aussi constamment. Cette approche permet une meilleure appréhension du problème pour le public non initié.
Si on connaît coord du point et l’angle d’incidence, on applique SD, on trouve coord du 2e

On pourra ensuite envisager une modélisation continue du phénomène en implémentant l’équation de trajectoire du faisceau.

 A FAIRE:        
-	 Interface Tkinter (débutée)
-	Fonction qui trouve les coordonnées du point de “rencontre” faisceau-mirage
-	Fonction qui  trouve  les coordonnées du point suivant au niveau de l’interface entre deux couches successivement
-	…

https://femto-physique.fr/optique/principe-de-fermat.php

ORAL : un peu plus de théorie

INTRO : choix du pgme, pas trop de théorie, cahier des charges, explication code
COMMENCER PAR CAS DISCRET (cas continu si assez de tps) !
↓
1 boucle pour 1 interface
-	Ne pas se placer du pov user : partir du code en dur PUIS implémenter sur Tk
-	Angles, indice, coord points


Considérer le point max du image et se placer dans la situation où le pt min est placé sur l’axe optique

-      	Réaliser une modélisation discrète à n couches d’air de densités différentes
