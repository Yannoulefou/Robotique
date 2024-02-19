""" On teste si des variables globales peuvent être appelées et/ou modifiées depuis un autre fichier """

# Test 1 : la var_globale est modifiée dans un autre fichier, par une fonction définie dans cet autre fichier
var_globale = None # voir dans fichier test.py : on modifie var_globale avec la fonction exemple()

"""
# Test 2 : la fonction est appelée depuis un autre fichier
from test import exemple
print(var_globale)
exemple()
print(var_globale)
# erreur : import circulaire car test.py importe var_globale
"""

# Test 3 : la var_globale et la fonction sont appelées depuis un autre fichier
from test import exemple2, angle
print(angle)
exemple2()
print(angle)
# ça ne marche pas : la variable globale angle est inchangée

# CONCLUSION : il faut que la variable globale rotation utilisée dans main_avec_gyro soit définie dans main_avec_gyro et la fonction calculer_rotation aussi