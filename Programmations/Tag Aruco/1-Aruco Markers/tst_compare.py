import cv2 as cv
from cv2 import aruco

img = cv.imread('arc1.png')

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

param_marker = aruco.DetectorParameters()

detector = aruco.ArucoDetector(marker_dict, param_marker)

marker_corners, markers_ID, reject = detector.detectMarkers(img)

frame_markers = aruco.drawDetectedMarkers(img.copy(), marker_corners, markers_ID)

cv.imshow("img",img)

print(marker_corners, markers_ID)

cv.imshow("marked", frame_markers)

cv.waitKey(0)