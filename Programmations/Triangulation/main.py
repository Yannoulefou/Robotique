import numpy as np
import math
from scipy.optimize import fsolve


def sinus(x):
    return np.sin(math.radians(x))

def cosinus(x):
    return np.cos(math.radians(x))

"""
Donne les angles du triangle ABC
"""
def anglesTriangle(A, B, C):  
       
    a2 = math.dist(B, C)**2
    b2 = math.dist(A, C)**2 
    c2 = math.dist(A, B)**2   
    a = math.sqrt(a2);  
    b = math.sqrt(b2);  
    c = math.sqrt(c2);  
  
    alpha = math.acos((b2 + c2 - a2) / (2 * b * c));  
    betta = math.acos((a2 + c2 - b2) / (2 * a * c));  
    gamma = math.acos((a2 + b2 - c2) / (2 * a * b));  
    alpha = alpha * 180 / math.pi;  
    betta = betta * 180 / math.pi;  
    gamma = gamma * 180 / math.pi;  
  
    return alpha, alpha, gamma


"""
Donne l'angle de v par rapport à l'axe des abscisses
"""
def vectorToAngle(v):
    ang = math.acos(v[0]/math.dist((0,0),v)) * 180 / math.pi
    if math.asin(v[1]/math.dist((0,0),v)) < 0:
        return - ang
    return ang

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
AB = math.dist(COORD_BALISE_A,COORD_BALISE_B)
AC = math.dist(COORD_BALISE_A,COORD_BALISE_C)
BC = math.dist(COORD_BALISE_B,COORD_BALISE_C)
ABC,BAC,ACB = anglesTriangle(COORD_BALISE_A, COORD_BALISE_B, COORD_BALISE_C)

# Variables de tests
"""
Les angles sont en degrés
"""
alpha = 0
beta = 0
gamma = 0

# Fonction
def get_position(alpha, beta, gamma):
    #Calcule de CBR
    sclaire = AC*sinus(gamma)/(AB*sinus(beta))
    def f(x):
        return [sclaire*sinus(ACB + x[0] -180 +alpha)- sinus(ABC-x[0])]
    CBR = (fsolve(f, [45]))[0]

    #On en déduit CAR et ABR
    CAR = 360 - beta - alpha - CBR - ACB
    ABR = ABC - CBR
    
    #Calcule de l'angle AR et BR par rapport à l'abscisse avec x=(1,0) et y = B + x
    xAC = vectorToAngle((COORD_BALISE_C[0]-COORD_BALISE_A[0], COORD_BALISE_C[1]-COORD_BALISE_A[1]))
    xAR = xAC + CAR
    yBA = vectorToAngle((COORD_BALISE_A[0]-COORD_BALISE_B[0], COORD_BALISE_A[1]-COORD_BALISE_B[1]))
    yBR = yBA + ABR

    #Calcule du point d'intersection des droites (AR) et (BR) qui est R
    M = np.array([[cosinus(xAR), -cosinus(yBR)],
                  [sinus(xAR), -sinus(yBR)]])
    V = np.array([[COORD_BALISE_B[0]-COORD_BALISE_A[0]],
                  [COORD_BALISE_B[1]-COORD_BALISE_A[1]]])
    scalaire = np.matmul(np.linalg.inv(M),V)[0][0]

    return (scalaire*cosinus(xAR), scalaire*sinus(xAR))
    

# Test
alpha = 109.65
beta = 167.47
gamma = 82.87
print( math.dist( get_position(alpha, beta, gamma), (1000, 500) ) ) # doit être égal à (1000, 500) 
# Tu peux utiliser Geogebra si besoin
