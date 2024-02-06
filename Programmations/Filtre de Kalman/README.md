# Les étapes
 - Comprendre le modèle 
 - Essayer de le mettre en place sur un modèle exemple : https://github.com/emmanuel-battesti/swarm-rescue/tree/main/src/swarm_rescue/examples
 - Essayer de comprendre les sources d'erreurs de la triangulation et les mesurer
 - Intégrer les erreurs pour l'estimation de la position

# Ressources
https://www.youtube.com/watch?v=IFeCIbljreY : Une vidéo très simple permettant de comprendre l'utilité du filtre de Kalman.

https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html : Un module python que j'ai déjà utilisé au sein d'un autre projet et que je trouve facile à prendre en main.

https://automaticaddison.com/extended-kalman-filter-ekf-with-python-code-example/ Une implémentation simple modèle #xt+1 = xt + v cos(theta)
#yt+1 = yt + v sin(theta) 
#theta_t+1 = theta_t + omega

https://atsushisakai.github.io/PythonRobotics/modules/slam/ekf_slam/ekf_slam.html#introduction Autre implémentation

https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python Des implémentations plus complexes ici
