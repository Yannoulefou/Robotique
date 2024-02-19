"""Test du module threading qui permet de faire tourner plusieurs fonction en même temps"""
import threading
import time

# On crée des fonctions de test, qui marchent sans connexion à l'Arduino

# Variable partagée pour indiquer si la fonction action est terminée
action_termine = threading.Event()

# Variable partagée pour stocker la valeur finale de l'angle
angle = None

# Fonction de test 1
def calcul_angle(arg) :
    global angle
    angle = 0
    while not action_termine.is_set():  # Boucler tant que la fonction action n'est pas terminée
        print("angle", angle)
        angle += 1
        time.sleep(arg)

# Fonction de test 2
def action(arg) :
    for i in range(5) :
        print("action", i)
        time.sleep(arg)
    action_termine.set()  # Indiquer que la fonction angle est terminée


# Créer le thread pour angle et le démarrer
thread_angle = threading.Thread(target=calcul_angle, args=(0.5,))
thread_angle.start()

# Créer le thread pour action et le démarrer
thread_action = threading.Thread(target=action, args=(0.5,))
thread_action.start()

# Attendre que le thread d'action se termine
thread_action.join()

# Après que le thread d'action s'est terminé, récupérer la valeur finale de l'angle (6 normalement)
print("Valeur finale de l'angle :", angle)


""" On teste si des variables globales peuvent être appelées et/ou modifiées depuis un autre fichier (test3.py)
from test3 import var_globale
def exemple() :
    global var_globale
    var_globale=0


print(var_globale)
exemple()
print(var_globale)


def exemple2() :
    global angle
    angle = 0
"""