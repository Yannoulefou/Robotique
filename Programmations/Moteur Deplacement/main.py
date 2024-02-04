from BaseDiff import BaseDiff, BaseDiffCalcul

base_diff = BaseDiffCalcul(x=225, y=225, angle=0)

# Ceci est un exemple de liste d'actions à effectuer pour le robot
liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 3525, 'pasD': 3525}), # Avancer tout droit (env. 1096mm diviser par 0.31)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 0, 'pasD': 281}), # Tourner à gauche à 145 °
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 2450, 'pasD': 2450 }), # Avancer tout droit
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

# Réalisation des actions
for fonction, kwargs in liste_actions:
    fonction(**kwargs) # On appelle la fonction avec les arguments
    print(f"Il a pour position {base_diff.x}, {base_diff.y} et pour angle {base_diff.angle}.")

# Résultats
print("Robot arrivé à destination ! :)")
print(f"Il a pour position {base_diff.x}, {base_diff.y} et pour angle {base_diff.angle}.")
