# import telemetrix
import math
import time

class BaseDiffCalcul:
    """
    Classe de base pour le calcul de la position du robot
    Cette classe sert de base pour les autres classes
    elle sert également à définir les constantes du robot
    et à effectuer des simulations en l'absence de la carte Arduino
    """
 
    RAYON = 750 # Rayon de la roue en mm
    LARGEUR = 350 # Largeur de l'essieu en mm
    LONGUEUR = 250 # Longueur du robot en mm

    LARGEUR_PLATEAU = 2000 # Largeur du plateau en mm
    LONGUEUR_PLATEAU = 3000 # Longueur du plateau en mm

    STEPS = 200 # Nombre de pas par tour du moteur

    def __init__(self, x=0, y=0, angle=0):
        self.x = x # Position en x
        self.y = y # Position en y
        self.angle = angle # Angle du robot (en radians, car les fonctions trigo prennent des radians sur numpy)

    def calculer_position(self, vitesseG, vitesseD, pasG, pasD):
        """
        Calculer la position du robot
        vitesseG : vitesse de la roue gauche en pas par seconde
        vitesseD : vitesse de la roue droite en pas par seconde
        pasG : nombre de pas de la roue gauche à effectuer
        pasD : nombre de pas de la roue droite à effectuer
        """
        # Calcul de la distance parcourue par chaque roue en mm
        arcG = -pasG * (self.RAYON * 2 * math.pi) / self.STEPS
        arcD = pasD * (self.RAYON * 2 * math.pi) / self.STEPS

        if arcG==arcD:
            distanceG,distanceD=arcG,arcD
        else:
            distanceG=2*self.LARGEUR*math.sin(arcG/(2*self.LARGEUR))
            distanceD=2*self.LARGEUR*math.sin(arcD/(2*self.LARGEUR))

        # Calcul de la différence de distances des roues
        delta_D = arcD + arcG

        # Changement d'angle en utilisant arcsin
        print(delta_D, self.LARGEUR, delta_D / self.LARGEUR)
        delta_theta = math.asin(delta_D / self.LARGEUR) #(trigonométrie)
        self.angle += delta_theta   

       # Calcul des déplacements en x et y du robot en utilisant pasG et pasD
        delta_x = (distanceG + distanceD) / 2 * math.cos(self.angle)
        delta_y = (distanceG + distanceD) / 2 * math.sin(self.angle)

        # Mise à jour de la position du robot
        self.x += delta_x
        self.y += delta_y

                

    def move(self, vitesseG, vitesseD, pasG, pasD):
        """
        Faire bouger le robot
        vitesseG : vitesse de la roue gauche en pas par seconde
        vitesseD : vitesse de la roue droite en pas par seconde
        pasG : nombre de pas de la roue gauche à effectuer
        pasD : nombre de pas de la roue droite à effectuer
        """
        self.calculer_position(vitesseG, vitesseD, pasG, pasD)


    def move_to_position(self, x_actuel, y_actuel, x_voulu, y_voulu):
        """
        Calculer le nombre de pas nécessaire pour que le robot aille d'une position (x,y) actuelle
        à une position (x,y) souhaitée
        On procède en 2 étapes : calcul des pas de chaque moteur pour que le robot s'oriente dans la bonne direction,
        puis calcul des pas de chaque moteur pour qu'il avance jusqu'aux positions voulues.
        """
        # Calculer la distance et l'angle entre les positions actuelles et souhaitées
        dx = x_voulu - x_actuel
        dy = y_voulu - y_actuel
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)  # Calcul de l'angle en radians

        # Calculer la rotation nécessaire pour orienter le robot vers la position souhaitée
        pas_tourner = angle * 550 / (2 * math.pi)  # 550 : tâtonné

        # Convertir la distance en pas pour chaque roue
        pas_avancer = (distance * self.STEPS) / (2 * math.pi * self.RAYON)

        # Renvoyer les valeurs de pas pour la rotation et pour la ligne droite
        return pas_tourner, pas_avancer


class BaseDiff(BaseDiffCalcul):
    """
    Classe de hérité de BaseDiffCalcul
    Cette classe ne fonctionne que avec une Arduino connecté
    """

    def __init__(self, board, x=0, y=0, angle=0, pinsG=[4, 5, 6, 7], pinsD=[8, 9, 10, 11]):
        super().__init__(x, y, angle)
        self.board = board # La carte Arduino

        # On définit les pins pour les moteurs
        self.motorG = self.board.set_pin_mode_stepper(4, *pinsG)
        self.motorD = self.board.set_pin_mode_stepper(4, *pinsD)
        self.board.stepper_set_acceleration(self.motorG, 1000)
        self.board.stepper_set_acceleration(self.motorD, 1000)

    def move(self, vitesseG, vitesseD, pasG, pasD):
        """
        Faire bouger le robot
        vitesseG : vitesse de la roue gauche en pas par seconde
        vitesseD : vitesse de la roue droite en pas par seconde
        pasG : nombre de pas de la roue gauche à effectuer
        pasD : nombre de pas de la roue droite à effectuer
        """
        # On définit la vitesse de chaque moteur
        self.board.stepper_set_max_speed(self.motorG, vitesseG)
        self.board.stepper_set_max_speed(self.motorD, vitesseD)

        # On envoie les instructions à la carte Arduino
        done = 0
        def incr_done(x):
            nonlocal done
            done += 1
        self.board.stepper_move(self.motorG, pasG)
        self.board.stepper_move(self.motorD, pasD)
        self.board.stepper_run(self.motorG, completion_callback=incr_done)
        self.board.stepper_run(self.motorD, completion_callback=incr_done)

        # On attend que les moteurs aient fini de bouger
        while done < 2:
            print(done)
            time.sleep(1)

        # On met à jour la position du robot
        BaseDiffCalcul.calculer_position(vitesseG, vitesseD, pasG, pasD)

    def ajuster_position(self, vitesseG, vitesseD, position_réelle) :
        """
        Le robot corrige sa position grâce aux données du gyroscope reçues dans position_réelle = (x, y, angle)
        Attention : les données sont très fausses pour le moment
        """
        if BaseDiffCalcul.x - position_réelle[0] > 30 or BaseDiffCalcul.y - position_réelle[1] > 30 or position_réelle[2] > 0.2 :
            pas_tourner, pas_avancer = BaseDiffCalcul.move_to_position(position_réelle[0], position_réelle[1], BaseDiffCalcul.x, Base.y)
            self.move(vitesseG, vitesseD, pas_tourner, - pas_tourner)
            self.move(vitesseG, vitesseD, pas_avancer, pas_avancer)

    def ajuster_angle(self, vitesseG, vitesseD, pasG, pasD, angle_réel) :
        """
        Après une rotation, le robot corrige sa direction grâce aux données du gyroscope reçues dans angle_réel
        """
        angle_voulu = (2*math.pi*pasD)/550  # pasG = 550 et pasD = -550 : pas pour tourner de 360° (tâtonné)
        erreur = angle_voulu - angle_réel
        if abs(erreur) > 0.2 :  # 0.2 est arbitraire, à calibrer
            pas_corr_D = erreur * 550 / (2*math.pi)
            self.move(vitesseG, vitesseD, -pas_corr_D, pas_corr_D)