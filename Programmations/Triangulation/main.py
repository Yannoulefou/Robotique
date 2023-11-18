import numpy as np
import math

"""
La fonction calcul position est censé donner la position du robot
"""

# Constantes CF.Robotique/Documents/Présentation/Eurobot2024.pdf (page9 balise équipe bleue)
"""
x est l'axe vers la droite
y est l'axe vers le bas
l'unité de distance est en millimètre
"""
COORD_BALISE_A = (0, 0)
COORD_BALISE_B = (0, 2000)
COORD_BALISE_C = (3000, 1000)

# Variables de tests
"""
A toi de choisir si on travail avec angle ou radian
(leur somme fait 1 tour complet)
"""
alpha = 0
beta = 0
gamma = 0

# Fonction
def get_position(alpha, beta, gamma):
    # si possible, une résolution matricielle serait plus élégante et plus facile à réutiliser
    position = (0, 0)
    return position

# Test
alpha = 109.65
beta = 167.47
gamma = 82.87
get_position(alpha, beta, gamma) # doit être égal à (1000, 500) 
# Tu peux utiliser Geogebra si besoin


