import cv2 as cv
from cv2 import aruco
import numpy as np

# Reading image
# img = cv.imread('plantes.jpg')
# img = cv.imread('panneaux.jpg')
# img = cv.imread('photo.jpg')
# img = cv.imread('photo2.jpg')
img = cv.imread('photo3.png')
# img = cv.imread('photo4.jpg')
# img = cv.imread('photo5.jpg')
# img = cv.imread('photo6.jpg')
# img = cv.imread('photo7.jpg')
# img = cv.imread('photo8.jpg')
# img = cv.imread('photo9.jpg')
# img = cv.imread('photo10.jpg')

# Defining lists
centres = []
z_rot = []

# Checking the image with each prelaoded Libraries
dictionary = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)
marker_corners, markers_ID, reject = detector.detectMarkers(img)
print(marker_corners, markers_ID)


    
# Calculating centre and angle of each marker
for dv in marker_corners:
	for c0,c1,c2,c3 in dv:
		mx = (c0[0]+c1[0]+c2[0]+c3[0])/4
		my = (c0[1]+c1[1]+c2[1]+c3[1])/4
		c = [mx,my]
		centres.append(c)
		vector = c0 - c
		angle = np.arctan2(vector[1], vector[0])
		angle *= 180/np.pi
		z_rot.append(abs(angle))
            
# Calculating angle of each marker
print(centres)
print(z_rot)

# Updating image to show the values and data found
aruco.drawDetectedMarkers(img, marker_corners, markers_ID, (0, 255, 0))

for centre in centres:
    cv.circle(img, (int(centre[0]), int(centre[1])), 5,(255,0,255), -1)

cv.imshow("img", img)

cv.waitKey(0)

