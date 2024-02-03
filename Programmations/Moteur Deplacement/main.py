from BaseDiff import BaseDiff, BaseDiffCalcul

base_diff = BaseDiffCalcul(x=225, y=225, angle=0)

# Ceci est un exemple de liste d'actions à effectuer pour le robot
liste_actions = [ # Liste des actions à effectuer dans un couple (fonctions, arguments)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': 950, 'pasD': 950}), # Avancer tout droit (env. 300mm)
    (base_diff.move, {'vitesseG': 700, 'vitesseD': 700, 'pasG': -950, 'pasD': -950}), # Reculer tout droit (env. 300mm)
    (base_diff.move, {'vitesseG': 350, 'vitesseD': 350, 'pasG': -500, 'pasD': -500}) # Tourner à gauche
]

# Réalisation des actions
for fonction, kwargs in liste_actions:
    fonction(**kwargs) # On appelle la fonction avec les arguments

# Résultats
print("Robot arrivé à destination ! :)")
print(f"Il a pour position {base_diff.x}, {base_diff.y} et pour angle {base_diff.angle}.")
