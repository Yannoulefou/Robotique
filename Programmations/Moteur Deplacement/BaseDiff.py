# import telemetrix
import math

class BaseDiffCalcul:
    """
    Classe de base pour le calcul de la position du robot
    Cette classe sert de base pour les autres classes
    elle sert également à définir les constantes du robot
    et à effectuer des simulations en l'absence de la carte Arduino
    """

    RAYON = 100 # Rayon de la roue en mm
    LARGEUR = 200 # Largeur de l'essieu en mm
    LONGUEUR = 300 # Longueur du robot en mm

    LARGEUR_PLATEAU = 2000 # Largeur du plateau en mm
    LONGUEUR_PLATEAU = 3000 # Longueur du plateau en mm

    STEPS = 200 # Nombre de pas par tour du moteur

    def __init__(self, x=0, y=0, angle=0):
        self.x = x # Position en x
        self.y = y # Position en y
        self.angle = angle # Angle du robot (en degrés ou radians ? à toi de voir Yassine)

    def calculer_position(self, vitesseG, vitesseD, pasG, pasD):
        """
        Calculer la position du robot
        vitesseG : vitesse de la roue gauche en pas par seconde
        vitesseD : vitesse de la roue droite en pas par seconde
        pasG : nombre de pas de la roue gauche à effectuer
        pasD : nombre de pas de la roue droite à effectuer
        """
        # Calcul de la distance parcourue par chaque roue en mm
        distanceG = pasG * (self.RAYON * 2 * math.pi) / self.STEPS
        distanceD = pasD * (self.RAYON * 2 * math.pi) / self.STEPS

    def move(self, vitesseG, vitesseD, pasG, pasD):
        """
        Faire bouger le robot
        vitesseG : vitesse de la roue gauche en pas par seconde
        vitesseD : vitesse de la roue droite en pas par seconde
        pasG : nombre de pas de la roue gauche à effectuer
        pasD : nombre de pas de la roue droite à effectuer
        """
        self.calculer_position(vitesseG, vitesseD, pasG, pasD)


class BaseDiff(BaseDiffCalcul):
    """
    Classe de hérité de BaseDiffCalcul
    Cette classe ne fonctionne que avec une Arduino connecté
    """

    def __init__(self, board, x=0, y=0, angle=0, pinsG=[4, 5, 6, 7], pinsD=[8, 9, 10, 11]):
        super().__init__(x, y, angle)
        self.board = board # La carte Arduino

        # On définit les pins pour les moteurs
        self.motorG = self.board.set_pin_mode_stepper(interface=4, *pinsG)
        self.motorD = self.board.set_pin_mode_stepper(interface=4, *pinsD)
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
        self.board.stepper_move(self.motorG, pasG)
        self.board.stepper_move(self.motorD, pasD)
        self.board.stepper_run(self.motorG)
        self.board.stepper_run(self.motorD)

        # On attend que les moteurs aient fini de bouger
        while self.board.stepper_is_running(self.motorG) or self.board.stepper_is_running(self.motorD):
            pass

        # On met à jour la position du robot
        self.calculer_position(vitesseG, vitesseD, pasG, pasD)


