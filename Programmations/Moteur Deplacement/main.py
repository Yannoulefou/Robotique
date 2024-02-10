from BaseDiff import BaseDiff, BaseDiffCalcul
import time

# Simulation ou connecté à une Arduino
is_simulation = False

if is_simulation:
    base_diff = BaseDiffCalcul(x=225, y=225, angle=0)
else:
    import sys
    import time

    from telemetrix import telemetrix

    board = telemetrix.Telemetrix()
    base_diff = BaseDiff(board=board, x=225, y=225, angle=0, pinsG=[4, 5, 6, 7], pinsD=[8, 9, 10, 11]   )

# Ceci est un exemple de liste d'actions à effectuer pour le robot
"""
liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 850, 'pasD': 850}), # Avancer tout droit (env. 1096mm diviser par 0.31)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 0, 'pasD': 281}), # Tourner à gauche à 145 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 850, 'pasD': 850 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 0, 'pasD': 175 }), #Tourner à gauche à 90 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2430, 'pasD': 2430 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 0, 'pasD': 281 }), # Tourner à gauche à 145 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 3525, 'pasD': 3525 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 88, 'pasD': 0 }), # Tourner à droite à 45 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2440, 'pasD': 2440 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 175, 'pasD': 0 }), #Tourner à droite à 90 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2430, 'pasD': 2430 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 268, 'pasD': 0 }), #Tourner à droite à 138 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2713, 'pasD': 2713 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 88, 'pasD': 0 }), #Tourner à droite à 45 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2713, 'pasD': 2713 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 0, 'pasD': 88 }), # Tourner à gauche à 45 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 707, 'pasD': 707 }) # Avancer tout droit
]
"""
# Ceci est un exemple de liste d'actions à effectuer pour le robot
liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 200, 'pasD': 0 }), # 45 °
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 700, 'pasD': 700}), # Avancer tout droit (env. 1096mm diviser par 0.31)
    (base_diff.move, {'vitesseG': 200, 'vitesseD': 200, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 500, 'pasD': 500 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': -600, 'pasD': -600 }), # Reculer tout droit
     (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': -400, 'pasD': 400}), # Tourner 
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
     (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 250, 'pasD': -250}), # Tourner 
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': -1200, 'pasD': -1200 }), # Reculer tout droit
    (base_diff.move, {'vitesseG': 200, 'vitesseD': 200, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': 400, 'vitesseD': 400, 'pasG': 700, 'pasD': 700 }), # Avancer tout droit
]
v = 600

liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 200, 'pasD': 0 }), # 45 °
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 700, 'pasD': 700}), # Avancer tout droit (env. 1096mm diviser par 0.31)
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 500, 'pasD': 500 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -600, 'pasD': -600 }), # Reculer tout droit
     (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -400, 'pasD': 400}), # Tourner 
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
     (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 250, 'pasD': -250}), # Tourner 
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 600, 'pasD': 600 }), # Avancer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -1200, 'pasD': -1200 }), # Reculer tout droit
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': -550, 'pasD': 550}), # Demi tour
    (base_diff.move, {'vitesseG': v, 'vitesseD': v, 'pasG': 700, 'pasD': 700 }), # Avancer tout droit
]

# Réalisation des actions
for fonction, kwargs in liste_actions:
    fonction(**kwargs) # On appelle la fonction avec les arguments
    time.sleep(0.5) # On attend 1 seconde
    print(f"Il a pour position {base_diff.x}, {base_diff.y} et pour angle {base_diff.angle}.")

# Résultats
print("Robot arrivé à destination ! :)")
print(f"Il a pour position {base_diff.x}, {base_diff.y} et pour angle {base_diff.angle}.")

if not is_simulation:
    board.shutdown() # On éteint la carte Arduino
